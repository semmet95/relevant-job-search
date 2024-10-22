from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

import time
from urllib.parse import urljoin

glassdoor_base_url = "https://www.glassdoor.co.in"

service = Service('geckodriver/geckodriver')
firefox_options = Options()
firefox_profile_path = "/home/amit/.mozilla/firefox/0wnsc6b7.default-release-1703934675999"
firefox_options.set_preference("profile", firefox_profile_path)

driver = webdriver.Firefox(service=service, options=firefox_options)
driver.maximize_window()
driver.get("https://www.glassdoor.co.in")
time.sleep(60)

# Manual:: login

driver.get("https://www.glassdoor.co.in/Job/pune-india-jobs-SRCH_IL.0,10_IC2856202.htm?minRating=4.0&fromAge=1")
time.sleep(10)

# click on the "show more jobs button until its gone"
while True:
    try:
        body_element = driver.find_element(By.TAG_NAME, 'body')  # Select the body element
        body_element.send_keys(Keys.ESCAPE)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        load_more_button = driver.find_element(By.CSS_SELECTOR, 'button[data-test="load-more"]')
        load_more_button.click()
        time.sleep(5)
    except NoSuchElementException:
        break

job_listings = driver.find_element(By.XPATH, '//ul[@aria-label="Jobs List"]')
job_arr = job_listings.find_elements(By.TAG_NAME, 'li')

job_links_all = []

for job in job_arr:
    try:
        a_element_css = job.find_element(By.CSS_SELECTOR, 'a[data-test="job-title"]')
        job_links_all.append(a_element_css.get_attribute("href"))
    except NoSuchElementException:
        continue 

# iterate over individual job links
company_links_all = []
for job_link in job_links_all:
    driver.get(job_link)
    time.sleep(10)
    company_element = driver.find_element(By.XPATH, "//a[contains(@class, 'EmployerProfile_profileContainer')]")
    company_link = company_element.get_attribute("href")
    
    if not company_link.startswith(glassdoor_base_url):
        company_link = urljoin(glassdoor_base_url, company_link)
    
    company_links_all.append(company_element.get_attribute("href"))

time.sleep(180)
driver.quit()
