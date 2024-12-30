import os
import csv
from bs4 import BeautifulSoup

# Configuration
FOLDER_PATH = "parliament_members_html"  # Folder containing the HTML files
OUTPUT_CSV = "assets_and_names_extracted.csv"  # Output CSV file

# Prepare CSV file
with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Filename", "Extracted Name", "Extracted Assets"])  # Write CSV header

    # Iterate through all HTML files in the folder
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".html"):  # Only process HTML files
            file_path = os.path.join(FOLDER_PATH, filename)
            print(f"Processing file: {filename}")

            try:
                # Read the HTML file
                with open(file_path, "r", encoding="utf-8") as file:
                    soup = BeautifulSoup(file, "html.parser")

                # Locate the name
                extracted_name = "Not found"
                name_tag = soup.find("div", id="displayName", class_="ciec-profilepage-title")
                if name_tag:
                    extracted_name = name_tag.get_text(strip=True)

                # Locate the "Assets" header
                extracted_assets = "Not found"
                assets_header = soup.find("div", class_="ciec-profilepage-subHeader", string="Assets")
                if assets_header:
                    assets_section = assets_header.find_parent("div", class_="ciec-profilepage-section")
                    extracted_assets = assets_section.get_text(separator=" ", strip=True)

                # Write the extracted data to the CSV
                writer.writerow([filename, extracted_name, extracted_assets])
                print(f"Extracted Name: {extracted_name}")
                print(f"Extracted Assets: {extracted_assets}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                writer.writerow([filename, "Error", "Error"])

print(f"Data extraction completed. Results saved to {OUTPUT_CSV}")
