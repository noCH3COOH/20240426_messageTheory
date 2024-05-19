import os
import filecmp

src_directory = "src"
rebuild_directory = "rebuild"

def compare_directories(src_dir, rebuild_dir):
    try:
        # Ensure the directories exist
        if not os.path.exists(src_dir) or not os.path.exists(rebuild_dir):
            return "One or both directories do not exist."

        # Lists to hold the results
        identical_files = []
        different_files = []

        # Walk through the src directory
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                # Check if the file is a bmp file
                if file.endswith('.bmp'):
                    # Construct the expected rebuild file name
                    rebuild_file_name = f"{os.path.splitext(file)[0]}_rebuild{os.path.splitext(file)[1]}"
                    rebuild_file_path = os.path.join(rebuild_dir, rebuild_file_name)

                    # Check if the corresponding rebuild file exists
                    if os.path.exists(rebuild_file_path):
                        # Compare the files
                        if filecmp.cmp(os.path.join(root, file), rebuild_file_path, shallow=False):
                            identical_files.append(file)
                        else:
                            different_files.append(file)
                    else:
                        different_files.append(file)

        return identical_files, different_files
    except Exception as e:
        return str(e)

# Let's try running the function again with error handling
identical_files, different_files = compare_directories(src_directory, rebuild_directory)

print("Identical files:")
for file in identical_files:
    print(file)

print("\nDifferent files:")
for file in different_files:
    print(file)
