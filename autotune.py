import subprocess
from get_profile import get_profile
import os
from definitions import ROOT_DIR
from data_processing.get_recommendations import get_recommendations
import json
from datetime import datetime as dt
import pandas as pd
from urllib.parse import urlparse
from definitions import UPLOAD_FOLDER, home, PROFILE_FILES, recommendations_file_path
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
		command2 = "rm {}".format(recommendations_file_path)
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
			print("dumped json file")
			print(file_path)
			print(UPLOAD_FOLDER+file_name)
			command3 = "oref0-upload-profile {} {} {} --switch=true".format(UPLOAD_FOLDER+file_name, nightscout, token)
			subprocess.call(command3, shell=True)
			# command4 = "rm "+file_path
			# subprocess.call(command4, shell=True)
			# self.clean_up()
			return True
		except Exception as e:
			logging.error(e)
			return False

if __name__ == "__main__":
	a = Autotune()
	a.upload(
		"https://tig-diab.herokuapp.com",
		[{'Parameter': 'ISF[mg/dL/U]', 'Pump': '45.00', 'Autotune': '45.05', 'DaysMissing': None},
		 {'Parameter': 'ISF[mmol/L/U]', 'Pump': '2.50', 'Autotune': '2.50', 'DaysMissing': None},
		 {'Parameter': 'CarbRatio[g/U]', 'Pump': '12.00', 'Autotune': '10.70', 'DaysMissing': None},
		 {'Parameter': 'Basals[U/hr]', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '00:00', 'Pump': '0.51', 'Autotune': '0.63', 'DaysMissing': '1'},
		 {'Parameter': '00:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '01:00', 'Pump': '0.58', 'Autotune': '0.66', 'DaysMissing': '1'},
		 {'Parameter': '01:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '02:00', 'Pump': '0.60', 'Autotune': '0.68', 'DaysMissing': '2'},
		 {'Parameter': '02:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '03:00', 'Pump': '0.61', 'Autotune': '0.70', 'DaysMissing': '2'},
		 {'Parameter': '03:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '04:00', 'Pump': '0.61', 'Autotune': '0.72', 'DaysMissing': '1'},
		 {'Parameter': '04:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '05:00', 'Pump': '0.62', 'Autotune': '0.72', 'DaysMissing': '1'},
		 {'Parameter': '05:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '06:00', 'Pump': '0.62', 'Autotune': '0.72', 'DaysMissing': '1'},
		 {'Parameter': '06:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '07:00', 'Pump': '0.62', 'Autotune': '0.72', 'DaysMissing': '1'},
		 {'Parameter': '07:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '08:00', 'Pump': '0.61', 'Autotune': '0.70', 'DaysMissing': '0'},
		 {'Parameter': '08:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '09:00', 'Pump': '0.59', 'Autotune': '0.68', 'DaysMissing': '0'},
		 {'Parameter': '09:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '10:00', 'Pump': '0.56', 'Autotune': '0.64', 'DaysMissing': '0'},
		 {'Parameter': '10:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '11:00', 'Pump': '0.52', 'Autotune': '0.60', 'DaysMissing': '1'},
		 {'Parameter': '11:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '12:00', 'Pump': '0.48', 'Autotune': '0.57', 'DaysMissing': '1'},
		 {'Parameter': '12:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '13:00', 'Pump': '0.44', 'Autotune': '0.54', 'DaysMissing': '1'},
		 {'Parameter': '13:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '14:00', 'Pump': '0.41', 'Autotune': '0.51', 'DaysMissing': '1'},
		 {'Parameter': '14:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '15:00', 'Pump': '0.40', 'Autotune': '0.49', 'DaysMissing': '2'},
		 {'Parameter': '15:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '16:00', 'Pump': '0.40', 'Autotune': '0.47', 'DaysMissing': '2'},
		 {'Parameter': '16:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '17:00', 'Pump': '0.41', 'Autotune': '0.46', 'DaysMissing': '2'},
		 {'Parameter': '17:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '18:00', 'Pump': '0.42', 'Autotune': '0.46', 'DaysMissing': '1'},
		 {'Parameter': '18:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '19:00', 'Pump': '0.42', 'Autotune': '0.47', 'DaysMissing': '2'},
		 {'Parameter': '19:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '20:00', 'Pump': '0.43', 'Autotune': '0.49', 'DaysMissing': '2'},
		 {'Parameter': '20:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '21:00', 'Pump': '0.44', 'Autotune': '0.51', 'DaysMissing': '3'},
		 {'Parameter': '21:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '22:00', 'Pump': '0.45', 'Autotune': '0.53', 'DaysMissing': '3'},
		 {'Parameter': '22:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''},
		 {'Parameter': '23:00', 'Pump': '0.46', 'Autotune': '0.54', 'DaysMissing': '3'},
		 {'Parameter': '23:30', 'Pump': '', 'Autotune': '', 'DaysMissing': ''}]
	, None)