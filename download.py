import os
import re
import json
import urllib.request
import csv
import datetime
import time
import argparse

# Download data from the Chronicling America website
def download_data(url, page, timeout_sec=200):
    try:
        with urllib.request.urlopen(f'{url}&rows=10&format=json&page={page}', timeout=timeout_sec) as response:
            return json.loads(response.read().decode('utf8'))
    except urllib.error.URLError as e:
        print(f"Error downloading data: {e}")
        return None
    
# Process json data into txt file
def process_item(p, writer, directory):
    if 'ocr_eng' in p:
        edition = re.search('(?<=\/ed-)(.*)(?=\/seq-)', p['id']).group(1)
        sequence = re.search('(?<=\/seq-)(.*)(?=\/)', p['id']).group(1)
            
        # Create a base file name using the date, title, edition, and sequence
        base_file_name = f"{p['date']}_{p['title']}_{edition}_{sequence}"

        # Sanitize the file name to remove non-alphanumeric characters, except underscores
        base_file_name_without_dot = base_file_name.replace('.', '_')
        sanitized_file_name = re.sub('[^a-zA-Z0-9_]', '', base_file_name_without_dot)

        # Ensure the sanitized file name is not empty
        if not sanitized_file_name.strip():
            sanitized_file_name = "default_name"

        # Append the .txt extension
        file_name = sanitized_file_name + ".txt"
        file_path = os.path.join(directory, file_name)

        # Generate .txt file
        with open(file_path, "w", encoding='utf8') as file:
            file.write(p['ocr_eng'])

        city, county, state = (p.get(key, [''])[0] for key in ['city', 'county', 'state'])
        writer.writerow([file_path, p['title'], p['date'], p['edition'], p['page'], p['sequence'], city, county, state, f"https://chroniclingamerica.loc.gov{p['id']}"])


def main():
    # Ask user for input url
    chronam_url = input("Paste in the URL for the Chronicling America search results you want to download: ")
    # Extract year from URL
    match = re.search(r'date1=(\d{4})', chronam_url)

    if not match:
        print("Year not found in URL.")
        return
    year = match.group(1)

    # Create directories
    year_directory = os.path.join(year)
    ocr_texts_dir = os.path.join(year_directory, 'ocr_texts')
    if not os.path.exists(ocr_texts_dir):
        os.makedirs(ocr_texts_dir)

    # CSV and metadata file paths
    metadata_csv_path = os.path.join(year_directory, 'metadata.csv')
    readme_path = os.path.join(year_directory, 'readme.txt')

    page = 1
     # Stop at page 100 (2,000 items) of results sorted by relevance
    end_page = 101
    text_counter = 0

    # Write csv file
    with open(metadata_csv_path, 'a', encoding='utf8') as metadata_file:
        csv_writer = csv.writer(metadata_file, delimiter=',')
        csv_writer.writerow(['file', 'title', 'date', 'edition', 'page', 'sequence', 'city', 'county', 'state', 'page_url'])
        while page < end_page:
            data = download_data(chronam_url, page)
            if not data or 'items' not in data or data['endIndex'] >= data['totalItems']:
                break
            # CSV update
            for item in data['items']:
                process_item(item, csv_writer, ocr_texts_dir)
                text_counter += 1 if 'ocr_eng' in item else 0
            # Print progress in CLI
            print(f"Progress: {page}/100")
            page += 1
            time.sleep(5)

    # Write readme file
    with open(readme_path, 'w') as readme:
        readme.write(f"Downloaded: {datetime.datetime.now()}\n\nNum of results: {data['totalItems']} newspaper pages—{text_counter} of those pages had OCR files.\n\nSearch URL: {chronam_url}\n\nSearch results in JSON: {chronam_url}&format=json\n\n")
        search = chronam_url.split("&")
        readme.write("===Search terms===\n" + search[0].split("?")[1] + '\n')
        for term in search[1:]:
            readme.write(term + '\n')
        readme.write("\n===Compiled with===\nChroniclingAmericaNLP ")

    print("Download complete")

if __name__ == "__main__":
    main()
