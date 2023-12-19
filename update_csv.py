import csv
import os
import argparse

def update_metadata_csv(csv_file_path, directory):
    # Collect all actual filenames in the directory
    actual_filenames = {file for file in os.listdir(directory) if file.endswith('.txt')}

    # Read existing data from CSV
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        csv_data = list(reader)

    # Update file paths in the CSV data
    for row in csv_data[1:]:  # Skip the header row
        # Extract only the filename part from the CSV row
        original_filename = os.path.basename(row[0])

        # Find a matching filename in the actual filenames
        for actual_filename in actual_filenames:
            if original_filename.split('.')[0] in actual_filename.split('.')[0]:
                # Update the filename in the CSV row with the full path
                row[0] = os.path.join(directory, actual_filename)
                break

    # Write updated data back to CSV
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)
        print(f"Updated metadata file: {csv_file_path}")

def main():
    parser = argparse.ArgumentParser(description='Update metadata.csv based on actual filenames in directory.')
    parser.add_argument('csv_file', help='Path to the metadata.csv file')
    parser.add_argument('directory', help='Path to the directory containing text files')
    args = parser.parse_args()

    update_metadata_csv(args.csv_file, args.directory)

if __name__ == '__main__':
    main()

