from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

# Step 1: Set the path to GeckoDriver (make sure to adjust this path to your geckodriver)
service = Service('geckodriver/geckodriver')

# Step 2: Set up options to use your existing Firefox profile
firefox_options = Options()

# Replace with the actual path to your Firefox profile
firefox_profile_path = "/home/amit/.mozilla/firefox/0wnsc6b7.default-release-1703934675999"
firefox_options.set_preference("profile", firefox_profile_path)

driver = webdriver.Firefox(service=service, options=firefox_options)
driver.maximize_window()
driver.get("https://www.glassdoor.co.in")
time.sleep(120)

driver.get("https://www.glassdoor.co.in/Job/pune-india-jobs-SRCH_IL.0,10_IC2856202.htm?minRating=4.0&fromAge=7")
time.sleep(180)

# Step 5: Close the browser
driver.quit()
