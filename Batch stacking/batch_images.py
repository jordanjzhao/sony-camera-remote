import os
import shutil

############################################
# Date: Aug. 5, 2024
# TestSequentialStackTIF v1.0
#
# Script to batch x sequential .tif images
# as part of a large format multi-row panorama
# for testing purposes
# 
# 
# Author: Jordan Zhao
#
############################################

# Directories
input_directory = os.path.expanduser('~/Desktop/lens_corrected')
output_directory = os.path.expanduser('~/Desktop/process')
processed_directory = os.path.expanduser('~/Desktop/processed_batches')
stacked_results_directory = os.path.expanduser('~/Desktop/stacked_results')

# Build output directories
os.makedirs(output_directory, exist_ok=True)
os.makedirs(processed_directory, exist_ok=True)
os.makedirs(stacked_results_directory, exist_ok=True)

# List of input files
files = sorted([f for f in os.listdir(input_directory) if f.endswith('.tif')])

# Stack batch size
batch_size = 10

# Build subdirectories and move files
commands = []
for i in range(0, len(files), batch_size):
    batch = files[i:i+batch_size]
    batch_dir_name = f'batch_{i // batch_size + 1:03d}'
    batch_dir = os.path.join(output_directory, batch_dir_name)
    lights_dir = os.path.join(batch_dir, 'lights')  # Subdirectory for images required for Siril processing
    processed_batch_dir = os.path.join(processed_directory, batch_dir_name)
    stacked_result_file = os.path.join(stacked_results_directory, f'stacked_{batch_dir_name}.fit')
    
    os.makedirs(batch_dir, exist_ok=True)
    os.makedirs(lights_dir, exist_ok=True)
    os.makedirs(processed_batch_dir, exist_ok=True)
    
    print(f"Creating batch directory: {batch_dir}")
    print(f"Creating processed batch directory: {processed_batch_dir}")
    
    for file in batch:
        src = os.path.join(input_directory, file)
        dest = os.path.join(lights_dir, file)
        print(f"Moving {src} to {dest}")
        shutil.move(src, dest)
    
    commands.append(f"cd {batch_dir}")
    commands.append(f"cd lights")
    commands.append(f"convert light -out={processed_batch_dir}")
    commands.append(f"cd {processed_batch_dir}")
    # calibrate
    commands.append(f"calibrate light -debayer")
    # align images
    commands.append(f"register pp_light")
    commands.append(f"stack r_pp_light rej 3 3 -norm=addscale -output_norm -out={stacked_results_directory}/{batch_dir_name}_stacked")

# Write Siril commands to text file
commands_file = os.path.expanduser('~/Desktop/siril_commands.txt')
with open(commands_file, 'w') as f:
    for command in commands:
        f.write(command + '\n')

print(f"Commands written to {commands_file}")

for i in range(0, len(files), batch_size):
    batch_dir = os.path.join(output_directory, f'batch_{i // batch_size + 1:03d}')
    print(f'Directory created: {batch_dir}')

