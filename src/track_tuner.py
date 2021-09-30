import os
import sys
import json

from channel_manager import ChannelManager

ends_with = lambda file, extensions: any(file.endswith(extension) for extension in extensions)

video_files = [file for file in os.listdir() if ends_with(file, [".mkv", ".mp4"])]
subtitle_files = [file for file in os.listdir() if ends_with(file, ["srt", "ssa", "ass", "idx"])]

if len(video_files) != len(subtitle_files):
    print("Uneven amount of media and subtitles")
    sys.exit()

channel_manager = ChannelManager(video_files, subtitle_files)
subtitle_selection = []

# Resync subtitles
# One group at a time
for files, channels in channel_manager.subtitle_info:
    # Only ask for subtitle channel if more than one are available
    if len(channels) > 1:
        print(json.dumps(channels, indent=4), "\n")
        subtitle_selection = input("Which subtitle channel would you like to sync to?\nInput a channel ID: ")
    else:
        subtitle_selection = channels[0]["id"]

    for file in files:
        channel_manager.resync_subtitle(file, subtitle_selection)

track_filter = input("""
If you would like to filter out irrelavent audio/subtitle tracks please add in a filter
By default only Japanese audio and English or Japanese subtitles will be kept
`N/No` to skip or anything to continue: 
""")
if track_filter not in ["N", "No"]:
    audio_filter = input("Audio Filter (default Japanese only): ")
    subtitle_filter = input("Subtitle Filter (default Japanese and English only): ")

    if audio_filter in ["", None]: audio_filter = "jpn"
    if subtitle_filter in ["", None]: subtitle_filter = "eng, jpn"

    channel_manager.filter_streams(audio_filter, subtitle_filter)
