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
   git clone https://github.com/PriyanshuSinghShorthillsAI/File_extraction2.py
   cd File_extraction2.py
   pip install -r requirements.txt
