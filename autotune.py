import subprocess
from get_profile import get_profile
import os
from definitions import ROOT_DIR
from data_processing.get_recommendations import get_recommendations
import json
from datetime import datetime as dt
import pandas as pd
from urllib.parse import urlparse
from definitions import UPLOAD_FOLDER, home, PROFILE_FILES
from file_management import checkdir
from log import logging

# AUTOTUNE CLASS
class Autotune:
	# URL VALIDATOR
	# https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
	def url_validator(self, x):
		try:
			result = urlparse(x)
			return all([result.scheme, result.netloc])
		except Exception as e:
			logging.error(e)
			return False

	# CLEAN UP FILES
	def clean_up(self):
		directory = "myopenaps/settings"
		directory = os.path.join(os.path.expanduser('~'), directory)
		for profile_file in PROFILE_FILES:
			os.path.join(directory, profile_file)
			command = "rm "+profile_file
			subprocess.call(command, shell=True)
		recommendations_file_path = "myopenaps/autotune/autotune_recommendations.log"
		recommendations_file = os.path.join(os.path.expanduser('~'), recommendations_file_path)
		command2 = "rm {}".format(recommendations_file)
		subprocess.call(command2, shell=True)

	# GET PROFILE
	def get(self, nightscout, token=None, insulin_type="rapid-acting"):
		profile = get_profile(nightscout, insulin_type, token=token)
		print("nightscout profile succesfully retreived")
		d = profile
		carb_ratio = d["carb_ratios"]["schedule"][0]["ratio"]
		sensitivity = d["isfProfile"]["sensitivities"][0]["sensitivity"]
		df_basals = pd.DataFrame.from_dict(d["basalprofile"])
		df_basals = df_basals.drop(["i", "minutes"], axis=1)
		df_basals["start"] = df_basals["start"].str.slice(stop=-3)
		df_basals = df_basals.rename(columns={"start": "Time", "rate": "Rate"})
		df_non_basals = pd.DataFrame(data={'ISF [mg/dL/U]': [sensitivity], 'ISF [mmol/L/U]': [sensitivity/18],  'Carbratio (gr/U)': [carb_ratio]})
		return df_basals, df_non_basals, profile

	# GET RECOMMENDATIONS
	def run(self, nightscout, start_date, end_date, uam=False, directory="myopenaps"):
		try:
			if not 'end_date':
				end_date = dt.utcnow().date().strftime("%Y-%m-%d")
			myopenaps = os.path.join(os.path.expanduser('~'), directory)
			checkdir(myopenaps)
			print("starting autotune run")
			if uam:
				command2 = "oref0-autotune --dir={} --ns-host={} --start-date={}  --end-date={}  --categorize-uam-as-basal=true > logfile.txt".format(
					myopenaps, nightscout, start_date, end_date, )
			else:
				command2 = "oref0-autotune --dir={} --ns-host={} --start-date={}  --end-date={}  > logfile.txt".format(myopenaps, nightscout, start_date, end_date,)
			subprocess.call(command2, shell=True)
			os.chdir(ROOT_DIR)
			print("getting recommendations")
			df_recommendations = get_recommendations()
			return df_recommendations
		except Exception as e:
			logging.error(e)
			return None


	# CREATE ADJUSTED PROFILE BASED ON USERINPUT
	def create_adjusted_profile(self, autotune_recomm, old_profile):
		# initiate variables
		l = autotune_recomm
		d = old_profile

		# extract sensitivity and carbratio from autotune recommendations dictionary and insert in old profile
		for i in l:
			if "ISF[mg/dL/U]" in str(i["Parameter"]):
				sensitivity = i["Autotune"]
			if "CarbRatio" in str(i["Parameter"]):
				carb_ratio = i["Autotune"]

		d["carb_ratios"]["schedule"][0]["ratio"] = round(float(carb_ratio), 1)
		d["carb_ratio"] = round(float(carb_ratio), 1)
		d["isfProfile"]["sensitivities"][0]["sensitivity"] = round((float(sensitivity) / 18), 1)

		# extract basal value from autotune recommendations dictionary into list "m"
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

		# save list in old profile basalprofile,thereby creating a profile with new basal rates
		d["basalprofile"] = m

		return d


	# UPLOAD TO NIGTHSCOUT AND ACTIVATE
	def upload(self, nightscout, profile, token):
		try:
			file_name = "/profile_2_upload.json"
			file_path = os.path.join(ROOT_DIR+UPLOAD_FOLDER + file_name)
			with open(file_path, 'w', encoding='utf-8') as f:
				json.dump(profile, f, ensure_ascii=False, indent=4)
			command3 = "oref0-upload-profile {} {} {} --switch=true".format(UPLOAD_FOLDER+file_name, nightscout, token)
			subprocess.call(command3, shell=True)
			command4 = "rm "+file_path
			subprocess.call(command4, shell=True)
			self.clean_up()
			return True
		except Exception as e:
			logging.error(e)
			return False


