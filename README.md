# Court Document & Amazon Product Scraper

## Overview
This project contains two web scraping tasks:
1. **Task 1**: Scraping US Federal District Court decisions from [Justia](https://law.justia.com/cases/) and saving case details and documents to Azure Blob Storage.
2. **Task 2**: Scraping product details and customer reviews from Amazon for a list of ASINs.

Both scrapers are designed to handle missing data, organize files efficiently, and upload results to Azure Blob Storage. The project follows object-oriented programming principles to modularize each component.

## Task 1: US Federal District Court Document Scraper

### Objective
Automate the extraction, storage, and organization of US Federal District court decision documents. Store extracted data in CSV/Excel files and document files (PDF/DOCX) in Azure Blob Storage.

### Prerequisites
- Python 3.x
- Required packages (see `requirements.txt`)
- Access to Azure Blob Storage (including a SAS URL)

### Features
1. **Data Extraction**: Scrapes details for each court case, including:
   - **Case Title**
   - **Date**
   - **Docket Number**
   - **Year**
   - **District**
   - **Division**
   - **Summary**
   - **Description**
   - **Link to Document**
2. **Data Handling**: Handles missing information and errors to keep the scraping process stable.
3. **Data Storage**:
   - Saves scraped details into a CSV or Excel file.
   - Stores case documents (PDF or DOCX format) in a structured path within Azure Blob Storage.
   - Generates Presigned Read URLs for easy access and sharing.
4. **File Management**: Lists all files within the Azure Blob Storage folder for easy retrieval.

### Directory Structure
- `{your_name}/task_1/US District Court/{district}/{year}/{file_name}.pdf`

### Usage
1. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/PriyanshuSinghShorthillsAI/Assignment_5_Scraping
   cd File_extraction2.py
   pip install -r requirements.txt


   # Amazon Product Data Scraper

## Overview
This project automates the extraction of product details and customer reviews from Amazon product pages. The scraper takes a list of ASINs (Amazon Standard Identification Numbers) as input and collects product and review information. The data is stored locally and uploaded to Azure Blob Storage, making it easily accessible and shareable.

## Prerequisites
- Python 3.x
- Required packages (see `requirements.txt`)
- Access to Azure Blob Storage (including a SAS URL for uploading data)

## Objective
Scrape essential information from Amazon product pages and their reviews for a specified list of ASINs. The tool should extract a minimum of 20 products and collect detailed reviews for each product.

## Features
1. **Product Information Extraction**:
   - **Product Name**: Title of the product.
   - **Product Images**: All images associated with the product.
   - **Rating**: Average customer rating (out of 5).
   - **Total Reviews Count**: Total number of customer reviews.
   - **Price**: Current price and any discounts (if available).
   - **"About this item"**: Summary of key product features.

2. **Review Data Extraction**:
   - **Rating**: Rating given by each reviewer.
   - **Date of Review**: Date when the review was posted.
   - **Reviewer's Region/Country**: Region or country of the reviewer (if available).
   - **Review Title**: Title of the review.
   - **Review Text**: Full text of the review.
   - **Feature-wise Review Count**: Positive and negative counts for each feature (e.g., Ease of Use, Durability).

3. **Data Storage**:
   - **Local Storage**: Saves data and images locally.
   - **Azure Blob Storage**: Uploads product images and JSON data to a structured folder in Azure Blob Storage for organized access and management.

### Directory Structure on Azure Blob Storage
Data is saved in the following structure:
- `{your_name}/task_2/{ASIN}/{data_file.json}`
- `{your_name}/task_2/{ASIN}/images/`

## Usage
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/PriyanshuSinghShorthillsAI/Assignment_5_Scraping
   cd Task2_Priyanshu

