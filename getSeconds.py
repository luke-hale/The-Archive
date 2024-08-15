import requests
import isodate
import time

API_KEY = 'AIzaSyDz8NDIi16k1XzYBZSts9TfSXNCYaS19e4'

# List of video IDs
video_ids = ["nfAqTSjMBJk", "mMaBVfIedFw"]

# URL template
url_template = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}'

# Get the current timestamp
current_time = int(time.time())

# To store video info
video_data = {"1": {}}

# Loop over the video IDs and get the details
for idx, video_id in enumerate(video_ids, start=1):
    url = url_template.format(video_id, API_KEY)
    response = requests.get(url)
    data = response.json()

    if 'items' in data and data['items']:
        # Extract video duration in ISO 8601 format
        duration_iso = data['items'][0]['contentDetails']['duration']
        duration_seconds = int(isodate.parse_duration(duration_iso).total_seconds())

        # Build video details with current time as playAt
        video_data["1"][str(idx)] = {
            "id": video_id,
            "playAt": current_time,
            "duration": duration_seconds
        }

        # Update current_time to account for video duration
        current_time += duration_seconds

# Print the result
print(video_data)

