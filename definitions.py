import os
import sys
from dotenv import load_dotenv
from dash import html
load_dotenv()


# PATHS
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
assets_path = os.getcwd() + '/assets'
UPLOAD_FOLDER = '/uploads'
home=os.path.expanduser('~')
PROFILE_FILES = ['autotune.json', 'profile.json', 'pumpprofile.json']
recommendations_file_path = "myopenaps/autotune/autotune_recommendations.log"
recommendations_file_path = os.path.join(os.path.expanduser('~'), recommendations_file_path)
new_profile_file_path = "new_profile.csv"
new_profile_file_path = os.path.join(os.path.expanduser('~'), new_profile_file_path)

# DEV ENVIRONMENT
if os.environ.get("ENV") == "development":
    development = True
else:
    development = False

# LINKS
github_url = 'https://github.com/KelvinKramp/Autotune123'
github_link = html.A("GitHub", href=github_url, target="_blank", style={'color': 'black'})
link1 = html.A("Savitzky-Golay filters", href='https://www.delftstack.com/howto/python/smooth-data-in-python/#use-the-numpy-convolve-method-to-smooth-data-in-python', target="_blank")
link2 = html.A("writes", href='https://diatribe.org/rules-engagement-basal-insulin-adjustment-or-avoiding-basal-blunders', target="_blank")
link3 = html.A("late in the evening to the night", href='https://www.psychologyinaction.org/psychology-in-action-1/2020/6/11/diurnal-patterns-of-cortisol', target="_blank")
link4 = html.A(" in this picture", href='https://diatribe.org/sites/default/files/images/tab-5.JPG', target="_blank")
link5 = html.A(" not set up properly", href='https://diatribe.org/rules-engagement-basal-insulin-adjustment-or-avoiding-basal-blunders', target="_blank")
text_links = [link1, link2, link3, link4, link5]

