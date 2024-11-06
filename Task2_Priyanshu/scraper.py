from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd
from azure.storage.blob import BlobServiceClient
from product import Product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
load_dotenv()

my_name = os.getenv("NAME")
print("name from env ", my_name)
class AmazonScraper:
    IMAGE_FOLDER = "images"
    JSON_FOLDER = "json_data"


class AmazonScraper:
    IMAGE_FOLDER = "images"
    JSON_FOLDER = "json_data"

    def __init__(self, sas_url, container_name, sas_token):
        # Initialize BlobServiceClient with base URL and SAS token as credential
        self.blob_service_client = BlobServiceClient(account_url=sas_url, credential=sas_token)
        self.container_name = container_name
        self.sas_token = sas_token 
        self.driver = self.setup_driver()

    def setup_driver(self):
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") 
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def scrape_products(self, asin_list):
        product_data_list = []

        for asin in asin_list:
            product = Product(asin, self.driver)
            product_data = product.fetch_product_data()
            if product_data:
                product_data_list.append(product_data)
                self.save_to_local(product_data, f"{asin}.json")
                self.save_images(asin, product_data["Product Image URLs"])
                
                # Upload JSON to blob and get the presigned URL
                blob_name = f"{my_name}/task_2/{asin}.json"
                presigned_url = self.upload_json_to_blob(blob_name, product_data, self.sas_token)

                # Store presigned URL in product data for Excel
                product_data["Blob JSON Path"] = presigned_url
                
                # Upload images to blob
                self.upload_images_to_blob(asin, product_data["Product Image URLs"])

        self.driver.quit()
        
        # Create Excel file with product details
        self.create_excel_file(product_data_list)

    def create_excel_file(self, product_data_list):
        excel_data = []
        for product in product_data_list:
            excel_data.append({
                "Product Name": product["Product Name"],
                "Product URL": product["Product URL"],
                "ASIN": product["ASIN"],
                "Blob JSON Path": product["Blob JSON Path"],  # Presigned URL for JSON
            })

        df = pd.DataFrame(excel_data)
        df.to_excel("product_data.xlsx", index=False)
        print("Excel file created: product_data.xlsx")

    def save_to_local(self, data, file_name):
        os.makedirs(self.JSON_FOLDER, exist_ok=True)
        file_path = os.path.join(self.JSON_FOLDER, file_name)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data saved to: {file_path}")

    def save_images(self, asin, image_urls):
        os.makedirs(self.IMAGE_FOLDER, exist_ok=True)
        for index, url in enumerate(image_urls):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    file_path = os.path.join(self.IMAGE_FOLDER, f"{asin}_image_{index}.jpg")
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Image saved: {file_path}")
                else:
                    print(f"Failed to fetch image from {url}: Status code {response.status_code}")
            except Exception as e:
                print(f"Failed to save image from {url}: {e}")

    def upload_json_to_blob(self, blob_name, data, sas_token):
        """Uploads a JSON file to Azure Blob Storage and returns its presigned URL."""
        try:
            # Convert the data to JSON string
            json_data = json.dumps(data, indent=4)
            
            # Create a blob client
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
            
            # Upload the JSON data
            blob_client.upload_blob(json_data, overwrite=True)  # Overwrite if the blob already exists
            print(f"JSON data uploaded to blob: {blob_name}")

            # Construct the presigned URL using the provided SAS token
            presigned_url = f"{blob_client.url}?{sas_token}"
            return presigned_url

        except Exception as e:
            print(f"Failed to upload JSON to blob {blob_name}: {e}")
            return None

    def upload_images_to_blob(self, asin, image_urls):
        for index, url in enumerate(image_urls):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    image_blob_name = f"{my_name}/task_2/images/{asin}_image_{index}.jpg"
                    self.upload_image_to_blob(image_blob_name, response.content)
                else:
                    print(f"Failed to fetch image from {url}: Status code {response.status_code}")
            except Exception as e:
                print(f"Failed to upload image from {url}: {e}")

    def upload_image_to_blob(self, blob_name, image_data):
        """Uploads an image to Azure Blob Storage."""
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
            blob_client.upload_blob(image_data, overwrite=True)
            print(f"Image uploaded to blob: {blob_name}")
        except Exception as e:
            print(f"Failed to upload image to blob {blob_name}: {e}")

    def list_blobs_in_task_folder(self):
        """Lists all blobs in the my_name/task_2 folder within the specified container."""
        try:
            # Create a container client
            container_client = self.blob_service_client.get_container_client(self.container_name)
            
            print(f"Blobs in {my_name}/task_2 folder:")
            
            # List all blobs in the "my_name/task_2" directory
            blob_list = container_client.list_blobs(name_starts_with=f"{my_name}/task_2/")
            
            for blob in blob_list:
                print(f"Blob name: {blob.name}")
                
        except Exception as e:
            print(f"Failed to list blobs in {my_name}/task_2: {e}")