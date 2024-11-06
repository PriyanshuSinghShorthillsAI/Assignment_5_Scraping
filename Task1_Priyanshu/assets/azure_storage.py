import os
from azure.storage.blob import BlobServiceClient, BlobClient
from dotenv import load_dotenv
 
load_dotenv()
 
class AzureBlobManager:
    def __init__(self):
        self.azure_base_url = os.getenv("SAS_URL")  # Base URL for Azure Blob Storage
        self.sas_token = os.getenv("SAS_TOKEN")  # SAS token for authentication
        if not self.azure_base_url or not self.sas_token:
            raise ValueError("Both azure_sas_url and azure_sas_token must be set as environment variables.")
        
        # Create the BlobServiceClient using the SAS URL
        self.service_url = f"{self.azure_base_url}?{self.sas_token}"
        self.blob_service_client = BlobServiceClient(account_url=self.service_url)
 
    def get_blob_sas_url(self, blob_name):
        """Construct the full URL for a blob including the SAS token."""
        return f"{self.azure_base_url}/{blob_name}?{self.sas_token}"
    
    def upload_file_to_blob(self, file_path, blob_name):
        """Upload a file to Azure Blob Storage."""
        try:
            blob_url = self.get_blob_sas_url(blob_name)
            blob_client = BlobClient.from_blob_url(blob_url=blob_url)
            
            # Upload the file
            with open(file_path, 'rb') as data:
                blob_client.upload_blob(data, overwrite=True)  # Overwrite if the blob exists
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Failed to upload {blob_name}. Error: {str(e)}")
    
    def list_blobs(self):
        """List all blobs in all containers."""
        try:
            containers = self.blob_service_client.list_containers()
            for container in containers:
                print(f"Container: {container.name}")
                container_client = self.blob_service_client.get_container_client(container.name)
                
                blobs = container_client.list_blobs()
                for blob in blobs:
                    print(f"  Blob: {blob.name}")
        except Exception as e:
            print(f"Failed to list blobs. Error: {str(e)}")
 
    def delete_blob(self, blob_name, container_name):
        """Delete a blob from the specified container."""
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            container_client.delete_blob(blob_name)
            print(f"Successfully deleted blob: {blob_name} from container: {container_name}.")
        except Exception as e:
            print(f"Failed to delete blob {blob_name}. Error: {str(e)}")