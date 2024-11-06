from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
load_dotenv()
 
class CaseScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.base_url = os.getenv("BASE_URL")
        self.titles = []
        self.dates = []
        self.docket_numbers = []
        self.descriptions = []
        self.document_links = []
        self.year_names = []
        self.district_names = []
 
    def navigate_to_federal_court(self):
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(3)
        try:
            federal_court = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/strong[3]/a")
                )
            )
            self.base_url = federal_court.get_attribute("href")
            federal_court.click()
        except Exception as e:
            print(f"Error clicking federal court link: {e}")
            self.driver.quit()
 
    def scrape_district_cases(self, districts, years):
        district_list_object = self.driver.find_elements(
            By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[2]/ul/li"
        )
        district_list = [di.text.lower() for di in district_list_object]
 
        for district in districts:
            if district.strip() in district_list:
                try:
                    district_path = self.base_url + district.strip().replace(' ','-') + "/"
                    self.driver.get(district_path)
                    self.driver.implicitly_wait(5)
 
                    year_list_object = self.driver.find_elements(
                        By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/ul/li"
                    )
                    year_list = [y.text for y in year_list_object]
 
                    for year in years:
                        year = year.strip()
                        if year in year_list:
                            self.scrape_cases_in_year(district, year, district_path)
                        else:
                            print(f"Year {year} not found for district {district}.")
                except Exception as e:
                    print(f"Error navigating to district: {e}")
            else:
                print(f"District {district} not found.")
 
    def scrape_cases_in_year(self, district, year, district_path):
        year_path = district_path + year + "/"
        self.driver.get(year_path)
 
        zones = self.driver.find_elements(
            By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[2]/ul/li"
        )
        number_of_zones = len(zones)
 
        if number_of_zones > 0:
            for i in range(0, number_of_zones):
                try:
                    zone_links = self.driver.find_elements(
                        By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[2]/ul/li/a"
                    )
                    zone_links[i].click()
                    self.driver.implicitly_wait(5)
 
                    divs = self.driver.find_elements(
                        By.CSS_SELECTOR, ".has-padding-content-block-30.-zb"
                    )
                    for div in divs[:3]:
                        self.scrape_case_details(div, district, year)
                    self.driver.back()
                except Exception as e:
                    print(f"Error navigating zones: {e}")
        else:
            print(f"No zones found for district {district} and year {year}.")
 
    def scrape_case_details(self, div, district, year):
        try:
            title_elem = div.find_element(By.CLASS_NAME, "case-name")
            docket_number = div.text.split()[-1]
            title = title_elem.text.strip()
            case_url = title_elem.get_attribute("href")
 
            date = ""
            details = div.find_elements(By.TAG_NAME, "span")
            for detail in details:
                if "Date:" in detail.text:
                    date = detail.text.replace("Date: ", "").strip()
 
            self.driver.get(case_url)
            case_description = self.driver.find_element(
                By.XPATH, "//div[@class='wrapper jcard has-padding-30 blocks']//p[1]"
            ).text.split(": ")[-1]
 
            try:
                link_to_document = self.driver.find_element(
                    By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div[3]/div/a"
                ).get_attribute("href")
            except Exception:
                link_to_document = "No document available"
 
            self.titles.append(title)
            self.dates.append(date)
            self.docket_numbers.append(docket_number)
            self.descriptions.append(case_description)
            self.document_links.append(link_to_document)
            self.year_names.append(year)
            self.district_names.append(district.strip())
 
            self.driver.back()
 
        except Exception as e:
            print(f"Error scraping case details: {e}")
            self.driver.back()
 
    def close(self):
        self.driver.quit()
        print("Browser closed.")