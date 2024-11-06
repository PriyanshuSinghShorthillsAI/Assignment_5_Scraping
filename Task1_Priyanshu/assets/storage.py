import pandas as pd
import os
import requests
import time
 
from azure_storage import AzureBlobManager
 
class Storage(AzureBlobManager):
 
    @staticmethod
    def save_to_csv(data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
        azure_blob_manager = AzureBlobManager()
        azure_blob_manager.upload_file_to_blob(filename, f"Priyanshu/task_1/{filename}")
 
    @staticmethod
    def download_document(url, docket_number, district, year):
        azure_blob_manager = AzureBlobManager()
        if url == "No document available":
            return
        try:
            response = requests.get(url)
            file_name = f"{docket_number}_{int(time.time())}.pdf"
            file_path = f"./Output/{district}/{year}/{file_name}"
 
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
 
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Document saved to {file_path}")
            blob_name = f"Priyanshu/task_1/US_District_Court/{district}/{year}/{docket_number}.pdf"
            azure_blob_manager.upload_file_to_blob(file_path, blob_name)
            presigned_url = azure_blob_manager.get_blob_sas_url(blob_name)
            print(f"Document uploaded to Azure Blob Storage: {presigned_url}")
            return presigned_url
        except Exception as e:
            print(f"Error downloading document: {e}")