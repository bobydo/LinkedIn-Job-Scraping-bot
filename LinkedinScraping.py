import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from desc_extract import JobDescriptionExtractor
from db_services import DBServices

class LinkedinScraper:
    def __init__(self, chrome_driver_path, output_csv_path=None):
        self.chrome_driver_path = chrome_driver_path
        self.output_csv_path = output_csv_path
        self.driver = None
        self.job_data = None

    def save_to_sqlserver(self):
        if self.job_data is not None:
            db = DBServices()
            db.save_to_sqlserver(self.job_data)

    def setup_driver(self, url):
        s = Service(self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=s)
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(15)

    def scroll_page(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(5)  # Wait for new content to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def click_see_more(self, pause_time=10):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            try:
                element = WebDriverWait(self.driver, pause_time).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'See more jobs') or contains(., 'See more')]"))
                )
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                pass
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def extract_jobs(self):
        job_lists = self.driver.find_elements(By.XPATH, "//*[@id='main-content']/section[2]/ul/li")
        job_title_list = []
        company_name_list = []
        location_list = []
        date_time_list = []
        job_link_list = []
        requirements_list = []
        extractor = JobDescriptionExtractor()
        for job in job_lists:
            job_title = None
            company_name = None
            location = None
            date_time = None
            job_link = None
            try:
                job_title = job.find_element(By.CSS_SELECTOR, 'h3').get_attribute('innerText')
                company_name = job.find_element(By.CSS_SELECTOR, 'h4').get_attribute('innerText')
                location = job.find_element(By.CLASS_NAME, 'job-search-card__location').get_attribute('innerText')
                date_time = job.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')
                job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except Exception:
                pass
            job_title_list.append(job_title)
            company_name_list.append(company_name)
            location_list.append(location)
            date_time_list.append(date_time)
            job_link_list.append(job_link)
            # Extract page text from job link and save to Requirements
            if job_link:
                # Open job link in the current window
                self.driver.execute_script("window.open(arguments[0]);", job_link)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(5)  # Wait for page to load

                # Extract 'About the job' section
                print(f"[DEBUG] job_link before call = {job_link}")
                requirements_text = extractor.extract_about_the_job(self.driver, job_link=job_link)

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                requirements_text = ""
            requirements_list.append(requirements_text)
        self.job_data = pd.DataFrame({
            'Title': job_title_list,
            'Company': company_name_list,
            'Location': location_list,
            'Last_Posting_Date': date_time_list,
            'Link': job_link_list,
            'Requirements': requirements_list
        })
        time.sleep(2)  # Wait 2 seconds between jobs (adjust as needed)

    def clean_data(self):
        if self.job_data is not None:
            self.job_data = self.job_data.replace('\n', " ", regex=True)

    def save_to_csv(self):
        if self.job_data is not None:
            self.job_data.to_csv(self.output_csv_path, mode='a', index=False, header=not os.path.exists(self.output_csv_path))

    def close(self):
        if self.driver:
            self.driver.quit()

    def run(self, url):
        self.setup_driver(url)
        self.scroll_page()
        self.click_see_more()
        self.extract_jobs()
        self.clean_data()
        if self.output_csv_path:
            self.save_to_csv()
        self.save_to_sqlserver()
        self.close()
