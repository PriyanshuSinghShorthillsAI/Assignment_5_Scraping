import os
import requests
import json

def save_images(asin, image_urls):
    os.makedirs("images", exist_ok=True)
    for index, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = os.path.join("images", f"{asin}_image_{index}.jpg")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Image saved: {file_path}")
        except Exception as e:
            print(f"Failed to save image from {url}: {e}")

def save_to_local(data, file_name):
    os.makedirs("json_data", exist_ok=True)
    file_path = os.path.join("json_data", file_name)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to: {file_path}")