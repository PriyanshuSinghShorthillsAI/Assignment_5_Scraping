import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Review:
    def __init__(self, driver, asin, min_reviews=20):
        self.driver = driver
        self.asin = asin
        self.min_reviews = min_reviews

    def get_reviews(self):
        reviews = []
        # Step 1: Navigate to the "See all reviews" page
        self.navigate_to_reviews_page()

        # Step 2: Collect reviews and handle pagination
        while len(reviews) < self.min_reviews:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            reviews += self.extract_reviews_from_page(soup)

            if not self.click_next_button():
                break  # No more pages to load

        return reviews

    def navigate_to_reviews_page(self):
        """Navigate to the Amazon reviews page for the given ASIN."""
        try:
            see_all_reviews_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@data-hook='see-all-reviews-link-foot']"))
            )
            see_all_reviews_link.click()

            # Wait for reviews to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-hook='review']"))
            )
            time.sleep(2)  # Allow time for the page to load

        except Exception as e:
            print(f"Error while navigating to reviews page for ASIN {self.asin}: {e}")

    def extract_reviews_from_page(self, soup):
        """Extract reviews from the current page's soup."""
        reviews = []
        review_elements = soup.find_all("div", {"data-hook": "review"})

        for review in review_elements:
            review_data = self.extract_review_data(review)
            if review_data:
                reviews.append(review_data)

        return reviews

    def extract_review_data(self, review):
        """Extract individual review details."""
        try:
            review_rating = review.find('span', {'class': 'a-icon-alt'}).get_text(strip=True) if review.find('span', {'class': 'a-icon-alt'}) else "N/A"
            review_date_element = review.find('span', {'data-hook': 'review-date'})
            if review_date_element:
                review_date_text = review_date_element.get_text(strip=True)
                parts = review_date_text.split(" on ")
                reviewer_region = parts[0].replace("Reviewed in ", "").strip() if len(parts) == 2 else "N/A"
                review_date = parts[1].strip() if len(parts) == 2 else review_date_text
            else:
                reviewer_region = "N/A"
                review_date = "N/A"

            review_title_element = review.find('a', {'data-hook': 'review-title'})
            review_title = review_title_element.get_text(strip=True).split('stars')[-1].strip() if review_title_element else "N/A"

            review_text_element = review.find('span', {'data-hook': 'review-body'})
            review_text = review_text_element.get_text(strip=True) if review_text_element else "N/A"

            return {
                "Rating": review_rating,
                "Date": review_date,
                "Region": reviewer_region,
                "Title": review_title,
                "Text": review_text
            }
        except Exception as e:
            print(f"Error extracting data from a review: {e}")
            return None

    def click_next_button(self):
        """Click the 'Next' button to load more reviews."""
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='a-last']//a"))
            )
            next_button.click()
            time.sleep(2)  # Allow time for the next page to load
            return True
        except Exception as e:
            print(f"Error clicking the next button for ASIN {self.asin}: {e}")
            return False