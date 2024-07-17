import os
import requests

# Set the directory where the finished videos are located
finished_dir = '/Users/olivertalcoth/Oliver Filer/Art Monitor Script/PosterToVideo/finished'
pisignage_api_url = 'http://192.168.1.53:8000/api/playlists'
username = 'pi'
password = 'pi'

# Get a list of all files in the finished directory
files_in_finished_dir = [f for f in os.listdir(finished_dir) if os.path.isfile(os.path.join(finished_dir, f))]

# Iterate over each file in the finished directory
for filename_with_extension in files_in_finished_dir:
    # Extract the filename without extension
    filename = os.path.splitext(filename_with_extension)[0]
    
    # Add .mp4 extension to the filename
    filename_with_extension = filename + ".mp4"
    
    # Get the full path of the video file
    video_path = os.path.join(finished_dir, filename_with_extension)
    
    # Check if the file is a video file
    if filename_with_extension.endswith('.mp4'):
        # Add the file to its respective playlist with the desired duration
        payload = {
            "name": filename,
            "version": 4,
            "assets": [
                {
                    "filename": filename_with_extension,  # Use the modified filename
                    "duration": 86400,  # 24 hours in seconds
                    "isVideo": True,
                    "selected": True,
                    "option": {
                        "main": True
                    }
                }
            ]
        }
        response = requests.post(f"{pisignage_api_url}/{filename}", json=payload, auth=(username, password))
        
        # Check if the file was successfully added to the playlist
        if response.status_code == 200:
            print(f"File '{filename_with_extension}' added to playlist '{filename}' with duration 24 hours.")
        else:
            print(f"Failed to add file '{filename_with_extension}' to playlist '{filename}'.")
    else:
        print(f"File '{filename_with_extension}' is not a video file. Skipping...")

print("Processing complete.")
