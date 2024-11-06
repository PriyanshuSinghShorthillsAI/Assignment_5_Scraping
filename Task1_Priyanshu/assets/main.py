from case_scraping import CaseScraper
from storage import Storage
import pandas as pd
 
 
def main():
    # Input from user
    districts = input("Enter the Districts (comma-separated): ").lower().split(",")
    years = input("Enter the Years (comma-separated): ").split(",")
 
    # Initialize the scraper
    scraper = CaseScraper()
 
    try:
        scraper.navigate_to_federal_court()
        scraper.scrape_district_cases(districts, years)
 
        # Data to save
        data = {
            "Year": scraper.year_names,
            "District": scraper.district_names,
            "Title": scraper.titles,
            "Date": scraper.dates,
            "Docket Number": scraper.docket_numbers,
            "Description": scraper.descriptions,
            "Document Link": scraper.document_links,
        }
 
        # Save scraped data to CSV
        filename='scraped_data.csv'
        Storage.save_to_csv(data, filename)
 
        # Download documents
        for i, url in enumerate(scraper.document_links):
            presigned_url = Storage.download_document(
                url,
                scraper.docket_numbers[i],
                scraper.district_names[i],
                scraper.year_names[i],
            )
            
            # append the presigned url
            df = pd.read_csv(filename)
            df['Blob URL'] = presigned_url
            df.to_csv(filename, index=False)
            
    except Exception as e:
        print(f"General error: {e}")
 
    finally:
        scraper.close()
 
 
if __name__ == "__main__":
    main()