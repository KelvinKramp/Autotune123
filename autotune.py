import subprocess
from get_profile import get_profile
import os
from ROOT_DIR import ROOT_DIR, checkdir
from get_recommendations import get_recommendations
from correct_current_basals import correct_current_basals
import json
from datetime import datetime as dt
import pandas as pd
from urllib.parse import urlparse

# VARIABLES
UPLOAD_FOLDER = '/uploads'
home=os.path.expanduser('~')


# AUTOTUNE CLASS
class Autotune:
	# URL VALIDATOR
	# https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
	def url_validator(self, x):
		try:
			result = urlparse(x)
			return all([result.scheme, result.netloc])
		except:
			return False

	# GET PROFILE
	def get(self, nightscout):
		profile = get_profile(nightscout)
		print("nightscout profile succesfully retreived")
		print(profile)
		d = profile
		carb_ratio = d["carb_ratios"]["schedule"][0]["ratio"]
		sensitivity = d["isfProfile"]["sensitivities"][0]["sensitivity"]
		df_basals = pd.DataFrame.from_dict(d["basalprofile"])
		df_basals = df_basals.drop(["i", "minutes"], axis=1)
		df_basals["start"] = df_basals["start"].str.slice(stop=-3)
		df_basals = df_basals.rename(columns={"start": "Time", "rate": "Rate"})
		df_non_basals = pd.DataFrame(data={'Sensitivity (mg/dL)': [sensitivity], 'Carbratio (gr per unit insuline)': [carb_ratio]})
		return df_basals, df_non_basals, profile

	# GET RECOMMENDATIONS
	def run(self, nightscout, start_date, end_date, directory="myopenaps"):
		try:
			if not 'end_date':
				end_date = dt.utcnow().date().strftime("%Y-%m-%d")

			# *** I INCLUDED THIS PART WHEN TRYING TO RUN ON EPIPHMERIAL GCP, IF RUN ON LOCAL THIS IS NOT NECESSARY
			# BUT INSTEAD RUN https://openaps.readthedocs.io/en/latest/docs/Customize-Iterate/autotune.html from step 1c
			# command1 = "./install.sh"
			# os.chdir(ROOT_DIR)
			# subprocess.call(command1, shell=True)
			myopenaps = os.path.join(os.path.expanduser('~'), directory)
			checkdir(myopenaps)
			print("starting autotune run")
			command2 = "oref0-autotune --dir={} --ns-host={} --start-date={}  --end-date={}  > logfile.txt".format(myopenaps, nightscout, start_date, end_date,)
			subprocess.call(command2, shell=True)
			os.chdir(ROOT_DIR)
			print("new nightscout profile succesfully created and saved")
			df_recommendations = get_recommendations()
			return df_recommendations
		except Exception as e:
			print(e)
			return None


	# CREATE ADJUSTED PROFILE BASED ON USERINPUT
	def create_adjusted_profile(self, autotune_recomm, old_profile):
		# initiate variables
		l = autotune_recomm
		d = old_profile

		# extract sensitivity and carbratio from autotune recommendations dictionary
		for i in l:
			if "ISF" in str(i["Parameter"]):
				sensitivity = i["Autotune"]
			if "CarbRatio" in str(i["Parameter"]):
				carb_ratio = i["Autotune"]
		d["carb_ratios"]["schedule"][0]["ratio"] = round(float(carb_ratio), 1)
		d["carb_ratio"] = round(float(carb_ratio), 1)
		d["isfProfile"]["sensitivities"][0]["sensitivity"] = round((float(sensitivity) / 18), 1)

		# extract basal value from autotune recommendations dictionary
		ftr = [3600, 60, 1]
		m = []
		for i, j in enumerate(l):
			if any(c.isalpha() for c in j["Parameter"]):
				continue
			timestr = j["Parameter"]
			# convert time string to seconds
			# source https://stackoverflow.com/questions/10663720/how-to-convert-a-time-string-to-seconds
			sec = sum([a * b for a, b in zip(ftr, map(int, timestr.split(':')))])
			for k in range(0, 24):
				if (k * 3600) == sec:
					l = {'i': k, 'minutes': 60.0 * k, 'start': '{:02d}:00:00'.format(k),
						 'rate': "{:.2f}".format(float(j["Autotune"]))}
					m.append(l)
		d["basalprofile"] = m

		return d


	# UPLOAD TO NIGTHSCOUT AND ACTIVATE
	def upload(self, nightscout, profile, token):
		try:
			file_name = "/profile_2_upload.json"
			file_path = os.path.join(ROOT_DIR+UPLOAD_FOLDER + file_name)
			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(profile, f, ensure_ascii=False, indent=4)
			command3 = "oref0-upload-profile {} {} {} --switch".format(UPLOAD_FOLDER+file_name, nightscout, token)
			subprocess.call(command3, shell=True)
			command4 = "rm "+file_path
			subprocess.call(command4, shell=True)
			return True
		except Exception as e:
			print(e)
			return False


