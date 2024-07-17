import os
import subprocess

# Set the input and output directories
input_dir = '/Users/olivertalcoth/Oliver Filer/Art Monitor Script/VideoToVideo/videos'
output_dir = '/Users/olivertalcoth/Oliver Filer/Art Monitor Script/VideoToVideo/finished'
pisignage_api_url = 'http://192.168.1.53:8000/api/playlists'
username = 'pi'
password = 'pi'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Iterate over the videos in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.mp4') or filename.endswith('.mov') or filename.endswith('.avi'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.mp4')
        playlist_name = os.path.splitext(filename)[0]

        # Convert the input video, scaled to 1080x1920, then padded if necessary, and flip vertically and horizontally
        subprocess.run([
            'ffmpeg', '-i', input_path, '-c:v', 'libx264', '-vf',
            'scale=1080:1920,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,vflip,hflip',
            '-b:v', '2M', '-bufsize', '4M', '-pix_fmt', 'yuv420p', '-f', 'mp4',
            output_path
        ], check=True)

        # Create the playlist using curl
        curl_command = f'curl -X POST "{pisignage_api_url}" -H "accept: application/json" -H "Content-Type: application/json" -d \'{{"file":"{playlist_name}"}}\' -u {username}:{password}'
        subprocess.run(curl_command, shell=True, check=True)

print("Processing complete.")