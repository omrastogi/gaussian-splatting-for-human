'''
/path/to/your/
│
├── database.db  # COLMAP database (will be created/used by the script)
│
├── images/      # Base directory for all image groups
│   ├── group1/  # Images from camera group 1
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   │
│   ├── group2/  # Images from camera group 2
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   │
│   └── ...      # More groups as needed
│
└── output/      # Directory where COLMAP outputs the reconstruction
    ├── cameras.bin
    ├── images.bin
    ├── points3D.bin
    └── ...

'''

import os
import subprocess

# Define paths
database_path = "/path/to/your/database.db"
image_base_path = "/path/to/your/images"
output_path = "/path/to/your/output"

# Define your camera groups with their specific intrinsic parameters
# Example: {"group_folder_name": ("CAMERA_MODEL", "focal_length,px,py,...")}
camera_groups = {
    "group1": ("SIMPLE_PINHOLE", "focal_length,px,py"),
    "group2": ("RADIAL", "focal_length,px,py,k1,k2"),
    # Add more groups as needed
}

# Function to run COLMAP commands
def run_colmap_command(command):
    print("Running command: ", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running command: ", result.stderr)
    else:
        print("Command output: ", result.stdout)

# Feature extraction for each group
for group, (model, params) in camera_groups.items():
    image_path = os.path.join(image_base_path, group)
    run_colmap_command([
        "colmap", "feature_extractor",
        "--database_path", database_path,
        "--image_path", image_path,
        "--ImageReader.camera_model", model,
        "--ImageReader.camera_params", params,
    ])

# Feature matching across all groups
run_colmap_command([
    "colmap", "exhaustive_matcher",
    "--database_path", database_path,
])

# Running the mapper to create the SfM model
run_colmap_command([
    "colmap", "mapper",
    "--database_path", database_path,
    "--image_path", image_base_path,
    "--output_path", output_path,
])

print("SfM pipeline completed.")
