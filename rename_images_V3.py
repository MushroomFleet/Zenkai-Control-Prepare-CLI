import os
import re

def rename_images_recursive(root_dir='.'):
    """
    Recursively scans directories starting from root_dir and renames image files
    by removing the '_XXXXX_' pattern from the END of filenames.
    """
    print(f"Starting the image renaming process from: {root_dir}")
    
    total_files_found = 0
    total_images_found = 0
    total_renamed = 0
    
    # Walk through all directories and subdirectories
    for current_dir, subdirs, files in os.walk(root_dir):
        print(f"\nProcessing directory: {current_dir}")
        total_files_found += len(files)
        
        # Filter for image files
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        total_images_found += len(image_files)
        
        print(f"Image files found in this directory: {len(image_files)}")
        
        # Process each image file
        for image_file in image_files:
            original_path = os.path.join(current_dir, image_file)
            print(f"Processing image file: {original_path}")
            
            # Split the filename and extension
            name_part, ext_part = os.path.splitext(image_file)
            
            # Remove the pattern like "__00001_" from the end of the filename
            # This will match double underscore followed by digits and trailing underscore
            # Or it will match the standard _XXXXX_ pattern
            new_name_part = re.sub(r'(__|_)\d+_+$', '', name_part)
            
            # Recombine the name and extension
            new_name = new_name_part + ext_part
            
            # Only rename if the pattern was found and changed
            if new_name != image_file:
                new_path = os.path.join(current_dir, new_name)
                try:
                    os.rename(original_path, new_path)
                    print(f"Successfully renamed: {image_file} -> {new_name}")
                    total_renamed += 1
                except Exception as e:
                    print(f"Error renaming {image_file}: {str(e)}")
            else:
                print(f"No pattern match found in: {image_file}")
    
    print(f"\nProcess completed.")
    print(f"Total files found: {total_files_found}")
    print(f"Total image files found: {total_images_found}")
    print(f"Total files renamed: {total_renamed}")

if __name__ == "__main__":
    import sys
    
    # Use command line argument as root directory if provided, otherwise use current directory
    root_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    rename_images_recursive(root_directory)
