import os
import json
import shutil
import datetime
from pathlib import Path
import argparse
import sys
from tqdm import tqdm

def load_config(config_path):
    """
    Load configuration from a JSON file.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in configuration file '{config_path}'.")
        sys.exit(1)

def create_dataset_folder(config):
    """
    Create a new dataset folder with timestamp.
    
    Args:
        config (dict): Configuration dictionary
        
    Returns:
        str: Path to the created dataset folder
    """
    base_path = config.get("base_path", ".")
    output_folder = config.get("output_folder", "datasets")
    
    # Create the output directory if it doesn't exist
    output_path = Path(base_path) / output_folder
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Create a new dataset folder with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dataset_folder = output_path / f"dataset_{timestamp}"
    dataset_folder.mkdir(exist_ok=True)
    
    print(f"Created dataset folder: {dataset_folder}")
    return dataset_folder

def handle_prompt_files(prompts_dir, images_dir):
    """
    Check if there's only one text file in the prompts directory.
    If so, duplicate it to match all image filenames.
    
    Args:
        prompts_dir (Path): Directory containing prompt files
        images_dir (Path): Directory containing image files
        
    Returns:
        bool: True if files were processed, False otherwise
    """
    if not prompts_dir.exists() or not images_dir.exists():
        print(f"Warning: Either prompts directory '{prompts_dir}' or images directory '{images_dir}' does not exist.")
        return False
    
    # Find all text files in the prompts directory
    txt_files = list(prompts_dir.glob('*.txt'))
    
    # If there's only one text file, proceed with duplication
    if len(txt_files) == 1:
        single_txt_file = txt_files[0]
        
        # Get all image files
        image_files = list(images_dir.glob('*.*'))
        if not image_files:
            print("Warning: No image files found to duplicate prompts for.")
            return False
        
        print(f"Found single text file '{single_txt_file.name}'. Duplicating for {len(image_files)} images...")
        
        # Read the content of the single text file
        try:
            with open(single_txt_file, 'r', encoding='utf-8') as f:
                txt_content = f.read()
        except Exception as e:
            print(f"Error reading text file '{single_txt_file}': {e}")
            return False
        
        # Create a copy for each image file
        for image_file in tqdm(image_files, desc="Duplicating prompt file"):
            # Get the base filename without extension
            image_name = os.path.splitext(image_file.name)[0]
            # Create a new text file with the same name as the image
            new_txt_file = prompts_dir / f"{image_name}.txt"
            
            try:
                with open(new_txt_file, 'w', encoding='utf-8') as f:
                    f.write(txt_content)
            except Exception as e:
                print(f"Error creating duplicate text file '{new_txt_file}': {e}")
        
        print(f"Successfully duplicated prompt file for {len(image_files)} images.")
        return True
    
    # If there are multiple text files, do nothing
    elif len(txt_files) > 1:
        print(f"Found {len(txt_files)} text files in prompts directory. Skipping duplication step.")
    else:
        print("No text files found in prompts directory.")
    
    return False

def copy_files(source_dir, target_dir, suffix=None):
    """
    Copy files from source directory to target directory,
    optionally appending a suffix to the filename.
    
    Args:
        source_dir (Path): Source directory
        target_dir (Path): Target directory
        suffix (str, optional): Suffix to append to filenames
        
    Returns:
        int: Number of files copied
    """
    if not source_dir.exists():
        print(f"Warning: Source directory '{source_dir}' does not exist.")
        return 0
    
    files = list(source_dir.glob('*.*'))
    copied = 0
    
    for file in tqdm(files, desc=f"Copying from {source_dir.name}"):
        if suffix:
            # Get file name and extension
            name, ext = os.path.splitext(file.name)
            new_name = f"{name}{suffix}{ext}"
            target_path = target_dir / new_name
        else:
            target_path = target_dir / file.name
        
        try:
            shutil.copy2(file, target_path)
            copied += 1
        except Exception as e:
            print(f"Error copying {file}: {e}")
    
    return copied

def process_dataset(config):
    """
    Process the dataset according to the configuration.
    
    Args:
        config (dict): Configuration dictionary
        
    Returns:
        Path: Path to the created dataset
    """
    base_path = Path(config.get("base_path", "."))
    folders = config.get("folders", {})
    
    # Create dataset folder
    dataset_folder = create_dataset_folder(config)
    
    # Copy files from each folder with appropriate suffix
    total_files = 0
    
    # 1. Copy images (no suffix)
    images_dir = base_path / folders.get("images", "images")
    total_files += copy_files(images_dir, dataset_folder)
    
    # 2. Handle prompt files special case
    prompts_dir = base_path / folders.get("prompts", "prompts")
    handle_prompt_files(prompts_dir, images_dir)
    
    # Copy prompts (no suffix)
    total_files += copy_files(prompts_dir, dataset_folder)
    
    # 3. Copy mask files with _M suffix
    mask_dir = base_path / folders.get("mask", "mask")
    total_files += copy_files(mask_dir, dataset_folder, suffix="_M")
    
    # 4. Copy depth files with _D suffix
    depth_dir = base_path / folders.get("depth", "depth")
    total_files += copy_files(depth_dir, dataset_folder, suffix="_D")
    
    # 5. Copy pose files with _P suffix
    pose_dir = base_path / folders.get("pose", "pose")
    total_files += copy_files(pose_dir, dataset_folder, suffix="_P")
    
    # 6. Copy canny files with _C suffix
    canny_dir = base_path / folders.get("canny", "canny")
    total_files += copy_files(canny_dir, dataset_folder, suffix="_C")
    
    print(f"\nDataset creation complete. Total files processed: {total_files}")
    print(f"Dataset location: {dataset_folder}")
    
    return dataset_folder

def main():
    """Main function to run the Zenkai Control Prepare system."""
    parser = argparse.ArgumentParser(description="Zenkai Control Prepare - Dataset Creation System")
    parser.add_argument("-c", "--config", default="config.json", help="Path to configuration file")
    args = parser.parse_args()
    
    print("Zenkai Control Prepare - Dataset Creation System")
    print("=" * 50)
    
    # Load configuration
    config = load_config(args.config)
    
    # Process dataset
    process_dataset(config)

if __name__ == "__main__":
    main()
