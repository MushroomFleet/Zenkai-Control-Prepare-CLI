# Zenkai Control Prepare

A dataset creation system for preparing control datasets by organizing and renaming files from various source folders.

## Overview

Zenkai Control Prepare is a tool designed to create control datasets by:

1. Creating a new timestamped dataset folder
2. Copying images and prompts directly
3. Copying and renaming depth maps (with "_D" suffix)
4. Copying and renaming pose maps (with "_P" suffix)
5. Copying and renaming canny edge maps (with "_C" suffix)

This tool simplifies the process of organizing control conditioning data for machine learning projects.

## Installation

### Prerequisites

- Python 3.6 or higher
- Windows operating system (for batch files)

### Setup

1. Clone or download this repository
2. Run the installation script:

```
install.bat
```

This will:
- Create a virtual environment
- Install all required dependencies

## Configuration

The system uses a JSON configuration file to define paths. Edit `config.json` to match your folder structure:

```json
{
  "base_path": "C:/path/to/your/data",
  "folders": {
    "images": "images",
    "prompts": "prompts",
    "depth": "depth",
    "pose": "pose",
    "canny": "canny"
  },
  "output_folder": "datasets"
}
```

### Configuration Options

- `base_path`: The root directory containing all your source folders
- `folders`: Relative paths to each type of data folder
  - `images`: Folder containing original images
  - `prompts`: Folder containing prompt files
  - `depth`: Folder containing depth maps
  - `pose`: Folder containing pose maps
  - `canny`: Folder containing canny edge maps
- `output_folder`: Name of the directory where datasets will be created

## Usage

1. Edit the `config.json` file to point to your data folders
2. Run the application:

```
run.bat
```

3. The system will:
   - Create a new dataset folder with timestamp (e.g., `dataset_20250405_181500`)
   - Copy all files from the specified folders
   - Rename depth, pose, and canny files with appropriate suffixes
   - Display progress and completion information

### Command Line Options

You can specify a different configuration file using the `-c` or `--config` option:

```
python main.py -c custom_config.json
```

## Example Folder Structure

Before:
```
C:/my_data/
├── images/
│   ├── img001.png
│   ├── img002.png
├── prompts/
│   ├── img001.txt
│   ├── img002.txt
├── depth/
│   ├── img001.png
│   ├── img002.png
├── pose/
│   ├── img001.png
│   ├── img002.png
├── canny/
│   ├── img001.png
│   ├── img002.png
```

After running Zenkai Control Prepare:
```
C:/my_data/
├── datasets/
│   ├── dataset_20250405_181500/
│   │   ├── img001.png        (from images/)
│   │   ├── img002.png        (from images/)
│   │   ├── img001.txt        (from prompts/)
│   │   ├── img002.txt        (from prompts/)
│   │   ├── img001_D.png      (from depth/)
│   │   ├── img002_D.png      (from depth/)
│   │   ├── img001_P.png      (from pose/)
│   │   ├── img002_P.png      (from pose/)
│   │   ├── img001_C.png      (from canny/)
│   │   ├── img002_C.png      (from canny/)
```

## Troubleshooting

- If you encounter a "File not found" error, check your configuration paths
- Ensure you have proper permissions to read from source folders and write to the output folder
- For any issues with the virtual environment, try deleting the `venv` folder and running `install.bat` again
