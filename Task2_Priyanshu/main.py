from scraper import AmazonScraper
from dotenv import load_dotenv
import os
load_dotenv()

def get_asin_input():
    while True:
        user_input = input("Enter up to 20 ASINs separated by commas: ")
        # Split the input string into a list and strip whitespace
        asins = [asin.strip() for asin in user_input.split(',')]
        # Check if the number of ASINs is within the limit
        if len(asins) > 100:
            print("Please enter no more than 100 ASINs.")
        else:
            return asins

if __name__ == "__main__":
    # Define your SAS URL and container name here
    sas_url = os.getenv("SAS_URL")
    container_name = os.getenv("CONTAINER_NAME")
    sas_token = os.getenv("SAS_TOKEN")
    ASINs = get_asin_input()
    scraper = AmazonScraper(sas_url, container_name, sas_token)
    scraper.scrape_products(ASINs)
    scraper.list_blobs_in_task_folder()