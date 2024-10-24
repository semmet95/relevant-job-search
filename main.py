import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

import time
from urllib.parse import urljoin

glassdoor_base_url = "https://www.glassdoor.co.in"
job_search_urls = [
    "https://www.glassdoor.co.in/Job/pune-india-jobs-SRCH_IL.0,10_IC2856202.htm?minRating=4.0&fromAge=3&jobTypeIndeed=CF3CP&cityId=2856202",
    "https://www.glassdoor.co.in/Job/hyderabad-india-jobs-SRCH_IL.0,15_IC2865319.htm?jobTypeIndeed=CF3CP&minRating=4.0&fromAge=3&cityId=2865319"
]
relevant_positions = ['senior software engineer', 'senior development engineer', 'senior software developer']
expected_min_salary = 40

checked_companies = set()

service = Service('geckodriver/geckodriver')
firefox_options = Options()
firefox_profile_path = "/home/amit/.mozilla/firefox/0wnsc6b7.default-release-1703934675999"
firefox_options.set_preference("profile", firefox_profile_path)

driver = webdriver.Firefox(service=service, options=firefox_options)
driver.maximize_window()
driver.get("https://www.glassdoor.co.in")
time.sleep(20)
driver.set_script_timeout(60)
driver.set_page_load_timeout(60)

# Manual:: login

for search_url in job_search_urls:
    driver.get(search_url)
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
        
        if company_link in checked_companies:
            continue

        checked_companies.add(company_link)

        driver.get(company_link)
        time.sleep(20)

        # get the salary div
        salary_div = driver.find_element(By.XPATH, "//div[@id='salaries' and @data-test='ei-nav-salaries-link']")
        salary_div.click()
        time.sleep(30)

        # get the current url and update it
        salary_url = driver.current_url

        index_of_htm = salary_url.find(".htm")
        if index_of_htm == -1:
            print("could not update url:: ", salary_url)
            continue
        
        page_num = 1
        while True:
            salary_url_new = salary_url[:index_of_htm] + "_IP" + str(page_num) + salary_url[index_of_htm:]
            page_num = page_num + 1
            driver.refresh()
            time.sleep(10)
            driver.get(salary_url_new)
            time.sleep(20)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            table_element = None
            try:
                table_element = driver.find_element(By.XPATH, "//table[contains(@class, 'salarylist_salary-table')]")
            except NoSuchElementException:
                print("no salaries found for company: ", company_link)
                break

            tbody_element = table_element.find_element(By.XPATH, "//tbody")
            row_count = len(tbody_element.find_elements(By.TAG_NAME, "tr"))

            if row_count <= 1:
                break
            
            rows = tbody_element.find_elements(By.TAG_NAME, "tr")[1:]
            role_found = False
            for row in rows:
                job_details = row.text.split("\n")
                job_title = job_details[0]

                if job_title.lower() in relevant_positions:
                    role_found = True
                    max_salary = int(re.search(r'\d+', job_details[2].split("-")[1]).group())

                    if max_salary >= expected_min_salary:
                        print("max salary: ", max_salary, " for role: ", job_title, " in comapny:")
                        print(driver.current_url)
                        with open("artifacts/company-list.txt", "w") as file:
                            for company in checked_companies:
                                file.write(f"{company}\n")
                    
                    break

            if role_found:
                break
            
            time.sleep(20)
    


driver.quit()