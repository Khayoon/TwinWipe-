import os
import hashlib
import shutil
from PIL import Image

def calculate_image_hash(filepath):
    """Calculate a hash for each image file or none if an error"""
    try:
        with Image.open(filepath) as img:
            img = img.convert("RGB")
            image_data = img.tobytes()  # Get raw image data
            return hashlib.md5(image_data).hexdigest()  
    except (FileNotFoundError, IOError, OSError, ValueError) as e:  # Catch errors
        print(f"Error processing {filepath}: {e}")
        return None

def find_and_remove_duplicates(source_root_dir, target_root_dir):

    source_hashes = {}  # Dictionary of image hashes

    # Build a hash dictionary of all source images.
    print(f"Scanning source directory: {source_root_dir}")
    for source_dirpath, _, source_filenames in os.walk(source_root_dir):
        for source_filename in source_filenames:
            if source_filename.lower().endswith(".jpg"):
                source_filepath = os.path.join(source_dirpath, source_filename)
                image_hash = calculate_image_hash(source_filepath)
                if image_hash:
                    # Store the hash and the full file path.
                    source_hashes.setdefault(image_hash, []).append(source_filepath)



    # Check the target directory for duplicates.
    print(f"Scanning target directory for duplicates: {target_root_dir}")
    duplicates_removed = 0  # Keep track of the number of removed files
    for target_dirpath, _, target_filenames in os.walk(target_root_dir):
        for target_filename in target_filenames:
            if target_filename.lower().endswith(".jpg"):
                target_filepath = os.path.join(target_dirpath, target_filename)
                target_image_hash = calculate_image_hash(target_filepath)

                if target_image_hash and target_image_hash in source_hashes:
                    # Duplicate found!
                    print(f"Duplicate found: {target_filepath}")
                    print(f"  Matches source: {source_hashes[target_image_hash]}") # Show matching source files

                    try:
                        os.remove(target_filepath)
                        duplicates_removed += 1
                        print(f"  Removed: {target_filepath}")
                    except OSError as e:
                        print(f"  Error removing {target_filepath}: {e}")

    print(f"Duplicate removal process complete.  {duplicates_removed} files removed.")


def main():
    """write the folder path here."""

    source_folder = r"C:\examplepath"
    target_folder = r""  

    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        return
    if not os.path.exists(target_folder):
        print(f"Error: Target folder '{target_folder}' does not exist.")
        return

    find_and_remove_duplicates(source_folder, target_folder)

if __name__ == "__main__":
    main()
