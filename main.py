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
    
    # 2. Copy prompts (no suffix)
    prompts_dir = base_path / folders.get("prompts", "prompts")
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
