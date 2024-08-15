import requests
import isodate
import json
from datetime import datetime, timezone
import time

# Print the current timestamp and readable time
current_timestamp = int(time.time())
print(f"Current Unix timestamp: {current_timestamp}")
readable_time = datetime.utcfromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S')
print(f"Readable time: {readable_time}")

API_KEY = 'AIzaSyBjy20Q9KWvIBEZ79RS8y1YwPuz94OHdMI'

# Arrays of video IDs for each channel
channel_videos = {
    "1": [
        "Zs10Bd2zh8U",
        "yYM1BjRvtvg",
        "uywtw7u7NFI",
        "0VgSLBDw_X8",
        "HdG77LX0nxg",
        "l-tocP55VE0",
        "dbiWH1xqeqQ",
        "-cQOwFq7KwU",
        "ZhwcHI8hSkM",
        "z13MXmyvGhs",
        "bnOiDvBOIiU",
        "03OdbVzaIV0",
        "uywtw7u7NFI",
        "MG0UAyM99ig",
        "RWCoW8mV8Ec"
    ],
    "2": [
        "b8m3dFcNuAQ",
        "K8hyzDJ4sLA",
        "faAg3YXpmBI",
        "DhCZLa5rbL4",
        "JgOG0j5KJsw",
        "TJOVNb_N8IE",
        "MIAJemmO-bg",
        "Alryavu9D5k",
        "v2ZtxEu5xxw",
        "vi3SQq1KjN4",
        "QpmEkKu9riA"
    ],
    "3": [
        "gDCOoJSeEc4",
        "mGAYd2_YMm0",
        "DavI7MWvq-0",
        "ErFr88-RY0I",
        "CTPqtI5NNjQ",
        "yaHCO0Ivp8U",
        "EHAJTnhpRtc",
        "pokWwET1pCU"
    ],
    "4": [
        "-RFunvF0mDw",
        "QrVbVJtIM9U"
    ]
}

# URL template
url_template = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}'

# To store video info
video_data = {}

# Number of loops for each channel
num_loops = 10

# Loop over each channel and video IDs
for channel, video_ids in channel_videos.items():
    current_time = int(datetime.now(timezone.utc).timestamp())  # Reset the current time for each channel
    video_data[channel] = {}
    total_duration_channel = 0  # To accumulate total duration for each channel
    video_count = 1  # Track video order

    # Loop over the videos for the current channel
    for loop in range(num_loops):  # Repeat the videos `num_loops` times
        for video_id in video_ids:
            url = url_template.format(video_id, API_KEY)
            response = requests.get(url)
            data = response.json()

            if 'items' in data and data['items']:
                # Extract video duration in ISO 8601 format
                duration_iso = data['items'][0]['contentDetails']['duration']
                duration_seconds = int(isodate.parse_duration(duration_iso).total_seconds())

                # Build video details with current time as playAt
                video_data[channel][str(video_count)] = {
                    "id": video_id,
                    "playAt": current_time,
                    "duration": duration_seconds
                }

                # Update current_time to account for video duration
                current_time += duration_seconds

                # Accumulate total duration for this channel
                total_duration_channel += duration_seconds
                video_count += 1  # Increment video order

    # Print the total duration for the current channel
    print(f"Total duration for channel {channel}: {total_duration_channel // 3600} hours, "
          f"{(total_duration_channel % 3600) // 60} minutes, {total_duration_channel % 60} seconds")

# Add the empty channels: 
for i in range(5, 13):
    video_data[str(i)] = {}

# Save the video data to a JSON file
with open('list.json', 'w') as json_file:
    json.dump(video_data, json_file, indent=4)

print("list.json has been saved.")