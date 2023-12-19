import os
import argparse

def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.count('.') > 1:  # Check if there's more than one dot in the filename
                file_path = os.path.join(root, file)
                new_file_name = file.rsplit('.', 1)[0].replace('.', '_') + '.' + file.rsplit('.', 1)[1]
                new_file_path = os.path.join(root, new_file_name)
                os.rename(file_path, new_file_path)
                print(f"Renamed '{file}' to '{new_file_name}'")

def main():
    parser = argparse.ArgumentParser(description='Rename files by removing dots in filenames.')
    parser.add_argument('directory', help='Directory to search for files to rename')
    args = parser.parse_args()

    rename_files(args.directory)

if __name__ == '__main__':
    main()

'''
def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.count('.') > 1:  # Check if there's more than one dot in the filename
                # Split the filename from the extension
                file_name, file_extension = os.path.splitext(file)

                # Replace all dots in the filename part
                new_file_name = file_name.replace('.', '_') + file_extension

                # Full path for the original and new file
                file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, new_file_name)

                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed '{file}' to '{new_file_name}'")
'''