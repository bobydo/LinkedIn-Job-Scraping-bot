from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class JobDescriptionExtractor:
    def __init__(self):
        pass


    def extract_about_the_job(self, driver, timeout=10, job_link=None):
        """
        Opens the job_link in a new tab, waits for the page to load, clicks 'See more' if present,
        and extracts the 'About the job' section from the LinkedIn job page.
        """
        if not job_link:
            print("No job link provided.")
            return ""

        try:
            # Open new tab and switch to it
            driver.execute_script("window.open(arguments[0], '_blank');", job_link)
            driver.switch_to.window(driver.window_handles[-1])

            # Wait for the job page to load (looking for the heading as an indicator)
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//h1"))
            )
            time.sleep(3)  # Fallback wait if the expected element isn't found

            # Click 'See more' if present
            try:
                see_more_btn = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'See more')]"))
                )
                see_more_btn.click()
                print("Clicked 'See more' button. {job_link}") 
            except Exception:
                print("Could not click 'See more' button. {job_link}")
                pass  # Button may not be present or already expanded

            # Find the 'About the job' section
            about_section = None
            try:
                about_section = driver.find_element(By.XPATH, "//section[.//h2[contains(., 'About the job')]]")
            except Exception:
                pass

            # Capture the text
            about_text = about_section.text.strip() if about_section else ""
            if not about_text:
                print(f"No 'About the job' section found. {job_link}")
            else:
                print(f"Extracted 'About the job' section from {job_link}")
            # Close the tab and switch back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            return about_text

        except Exception as e:
            return f"Error extracting 'About the job': {e}"


    def print_job_link(self, about_section, job_link):
        if about_section:
            print(f"About the job section found from {job_link}")
        else:
            print(f"About the job section not found from {job_link}")