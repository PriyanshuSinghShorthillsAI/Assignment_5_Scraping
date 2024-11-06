import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from review import Review

class Product:
    def __init__(self, asin, driver):
        self.asin = asin
        self.driver = driver
        self.product_data = {
            "ASIN": asin,
            "Product Name": "N/A",
            "Product URL": f"https://www.amazon.in/dp/{asin}",
            "Product Image URLs": [],
            "Rating": "N/A",
            "Total reviews count": "N/A",
            "Price": "N/A",
            "Discount Percentage": "N/A",
            "About this item": "N/A",
            "Feature Insights": {},
            "Customer Reviews": []
        }

    def fetch_product_data(self):
        product_url = self.product_data["Product URL"]
        self.driver.get(product_url)
        
        time.sleep(2)  # Sleep to allow page to load
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        self.extract_product_info(soup)
        self.extract_reviews()
        
        return self.product_data

    def extract_product_info(self, soup):
        try:
            # Extracting product name
            product_name = soup.find(id='productTitle').get_text(strip=True) if soup.find(id='productTitle') else None
            if product_name:
                self.product_data["Product Name"] = product_name
            
            # Extracting all image URLs
            self.product_data["Product Image URLs"] = self.extract_image_urls(soup)

            # Extracting other product details
            self.product_data["Rating"] = self.extract_rating(soup)
            self.product_data["Total reviews count"] = self.extract_total_reviews(soup)
            self.product_data["Price"] = self.extract_price(soup)
            self.product_data["Discount Percentage"] = self.extract_discount_percentage(soup)
            self.product_data["About this item"] = self.extract_about_item(soup)
            self.product_data["Feature Insights"] = self.extract_feature_insights(soup)

        except Exception as e:
            print(f"Error extracting data for ASIN {self.asin}: {e}")

    def extract_image_urls(self, soup):
        images = []
        main_image = soup.find('img', {'id': 'landingImage'})
        if main_image:
            images.append(main_image['src'])

        thumbnail_elements = soup.find_all('li', class_="a-spacing-small item imageThumbnail a-declarative")
        for thumbnail in thumbnail_elements:
            img_tag = thumbnail.find('img')
            if img_tag and 'src' in img_tag.attrs:
                img_url = img_tag['src']
                if img_url not in images:
                    images.append(img_url)
        
        return images

    def extract_rating(self, soup):
        return soup.find('span', {'class': 'a-icon-alt'}).get_text(strip=True) if soup.find('span', {'class': 'a-icon-alt'}) else None

    def extract_total_reviews(self, soup):
        return soup.find('span', {'id': 'acrCustomerReviewText'}).get_text(strip=True) if soup.find('span', {'id': 'acrCustomerReviewText'}) else "N/A"

    def extract_price(self, soup):
        price_whole = soup.find('span', {'class': 'a-price-whole'}).get_text(strip=True) if soup.find('span', {'class': 'a-price-whole'}) else None
        price_fraction = soup.find('span', {'class': 'a-price-fraction'}).get_text(strip=True) if soup.find('span', {'class': 'a-price-fraction'}) else ""
        return f"{price_whole}{price_fraction}" if price_whole else "N/A"

    def extract_discount_percentage(self, soup):
        return soup.find('span', class_='savingsPercentage').get_text(strip=True) if soup.find('span', class_='savingsPercentage') else "N/A"

    def extract_about_item(self, soup):
        """Extract the 'About this item' text from the soup, handling 'See More' if it exists."""
        about_item = []

        # Attempt to click "Show More" if it exists
        try:
            show_more_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@data-action, 'a-expander-toggle') and contains(., 'Show More')]"))
            )
            show_more_button.click()
            
            # Wait for the content to load after clicking
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'feature-bullets'))  # Wait for 'feature-bullets' to ensure it has updated
            )
            
            # Re-fetch the page source after clicking "Show more"
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Extract bullet points from the 'feature-bullets' section
            bullet_points = soup.find('div', {'id': 'feature-bullets'})
            if bullet_points:
                items = bullet_points.find_all('li')
                about_item = [item.get_text(strip=True) for item in items]

        except Exception as e:
            print(f"No 'Show more' button found or clickable for ASIN {self.asin}: {e}")

        # Fallback: Try to extract bullet points without clicking
        if not about_item:
            bullet_points = soup.find('div', {'id': 'feature-bullets'})
            if bullet_points:
                items = bullet_points.find_all('li')
                about_item = [item.get_text(strip=True) for item in items]

        # Format the bullet points as a string with line breaks
        return '\n'.join(f"• {item}" for item in about_item) if about_item else "N/A"

    def extract_feature_insights(self, soup):
        feature_insights = {}
        insight_elements = soup.find_all("div", class_="_cr-product-insights_style_stat-info-box__1akN2")

        for insight in insight_elements:
            aspect_text = insight.find('span', class_='a-color-base').get_text(strip=True)
            positive_count = insight.find('span', class_='_cr-product-insights_style_text-positive__QRaJ2').get_text(strip=True)
            negative_count = insight.find('span', class_='_cr-product-insights_style_text-negative__zjq0Y').get_text(strip=True)

            if aspect_text:
                aspect_name = aspect_text.split('"')[1]
                feature_insights[aspect_name] = {
                    "Positive": positive_count,
                    "Negative": negative_count
                }
        
        return feature_insights

    def extract_reviews(self):
        review_extractor = Review(self.driver, self.asin)
        self.product_data["Customer Reviews"] = review_extractor.get_reviews()