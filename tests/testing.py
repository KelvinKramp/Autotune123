import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime as dt
import os
import datetime
from selenium.webdriver.chrome.service import Service
from definitions import ROOT_DIR, development
import json
from datetime import datetime as dt
from datetime import timedelta
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import glob
import pandas as pd
import tests.datetime_management as datetime_management

secrets_path = os.path.join(ROOT_DIR, "tests", "secrets.json")
with open(secrets_path) as f:
    secrets = json.load(f)
downloads_path = os.path.join(os.path.expanduser('~'), "Downloads")

# define sleep parameter
sleep_par_short = 0.1
sleep_par_long = 4

test_page = "http://www.autotune123.com/"
test_name = "test_name"
test_email = "test_email@email.com"
test_text = "THIS IS A TEST RUN"
keyword1 = ""
keyword2 = ""
keyword3 = ""


NS_URL = secrets["NS_URL"]
website_URL = secrets["website_URL"]
inputbox_NS_URL = "/html/body/div/div/div[2]/div[1]/div/div[1]/div[1]/input[1]"
load_profile_button = "/html/body/div/div/div[2]/div[1]/div/div[1]/div[4]/button"
run_button = "/html/body/div/div/div[2]/div[1]/div/div[2]/div/div[2]/button"
end_date_datepicker = "/html/body/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div/div/div/div/div[3]/input"
downloads_button = "/html/body/div/div/div[2]/div[1]/div/div[3]/div/div[1]/div[2]/div/div[4]/div[2]/button"

def get_latest_csv(min_treshold_time=5, max_treshold_time=0.1):
    print("CHECKING FOR CSV FILES FROM DOWNLOAD FOLDER")
    files = glob.glob(downloads_path + "/**/*", recursive = True)
    if not files:
        df = pd.DataFrame()
    else:
        latest_file = max(files, key=os.path.getctime)
        creation_time = datetime_management.modification_date(latest_file)
        current_time = datetime.datetime.now()
        # check if file is more recent than 2 minutes ago
        if (current_time.minute - min_treshold_time) < creation_time.minute < (current_time.minute + max_treshold_time) and ("csv" in str(latest_file)):
            print("LATEST CSV FILE CREATED SHORTER THAN", min_treshold_time,"MINUTES AGO, USING THIS CSV FILE")
            df = pd.read_csv(latest_file)
        else:
            print("NO SUITABLE CSV FILE FOUND")
            df = pd.DataFrame()
    return df


class TestFeedbackApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('SETTING UP TEST UNIT')
        global driver, wait

        # https://stackoverflow.com/questions/63783983/element-not-interactable-in-selenium-chrome-headless-mode
        if development:
            options = Options()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            # # options.add_argument("--headless")
            driver = webdriver.Chrome(ChromeDriverManager().install())
            # driver = webdriver.Chrome(options=options)
        else:
            chrome_options = Options()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            ser = Service(os.environ.get("CHROMEDRIVER_PATH"))
            driver = webdriver.Chrome(service=ser,
                                      options=chrome_options)
        wait = WebDriverWait(driver, 60)
        print("CONNECTION TO BROWSER SUCCESFULL")


    def test_a_step1_autotune123(self):
        time.sleep(2)
        # get website
        driver.get(website_URL)
        page_source = driver.page_source
        # print(page_source)
        self.assertTrue(keyword1 in page_source)

    def test_b_step2_autotune123(self):
        # fill in NS URL
        time.sleep(2)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, inputbox_NS_URL)))
        driver.find_element(By.XPATH, inputbox_NS_URL).clear()
        element = wait.until(EC.element_to_be_clickable((By.XPATH, inputbox_NS_URL)))
        driver.find_element(By.XPATH, inputbox_NS_URL).send_keys(NS_URL)
        driver.find_element(By.XPATH, load_profile_button).click()
        page_source = driver.page_source
        # print(page_source)
        self.assertTrue(keyword2 in page_source)
        # fill in date -> function not working -> TODO: changed enddate in initial date to day before today
        # date = dt.now().date() - timedelta(1)
        # date = date.strftime("%d-%m-%Y")
        # element = wait.until(EC.element_to_be_clickable((By.XPATH, end_date_datepicker)))
        # driver.find_element(By.XPATH, end_date_datepicker).clear()
        # driver.find_element(By.XPATH, end_date_datepicker).send_keys(date)

        # start autotune run
        time.sleep(2)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, run_button)))
        driver.find_element(By.XPATH, run_button).click()

    def test_c_step3_autotune123(self):
        element = wait.until(EC.element_to_be_clickable((By.XPATH, downloads_button)))
        page_source = driver.page_source
        # print(page_source)
        self.assertTrue(keyword1 in page_source)

    def test_d_step4_download_rec(self):
        # download recommendations
        element = wait.until(EC.element_to_be_clickable((By.XPATH, downloads_button)))
        driver.find_element(By.XPATH, downloads_button).click()
        # get csv from downloadsfolder and convert to pandas df
        time.sleep(2)
        df= get_latest_csv()
        print(df)
        self.assertTrue(len(df) > 10)

    @classmethod
    def tearDownClass(cls):
        driver.close()
        print('TEARING DOWN CLASS')


if __name__ == '__main__':
    unittest.main()