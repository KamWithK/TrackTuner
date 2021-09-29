import os
import json
import subprocess

class ChannelManager:
    def __init__(self, video_paths, subtitle_paths) -> None:
        self.video_paths = video_paths
        self.subtitle_paths = subtitle_paths

        self.subtitle_info = []

        for file in video_paths:
            self.get_subtitle_information(self.get_tracks(file), file)

    def get_tracks(self, file):
        return json.loads(
            subprocess.check_output([
                "mkvmerge",
                "--identification-format", "json",
                "--identify",
                file
            ])
        )["tracks"]

    def get_subtitle_information(self, tracks, file):
        # Only keep SubStationAlpha subtitles
        # Log each tracks name and language (where available)
        valid_track = lambda track: track["type"] == "subtitles" and track["codec"] == "SubStationAlpha"
        get_key_info = lambda track: {
                "id": track["id"],
                "track_name": track["properties"]["track_name"] if "track_name" in track["properties"] else "",
                "language": track["properties"]["language"] if "language" in track["properties"] else ""
            }
        filtered_tracks = list(map(get_key_info, filter(valid_track, tracks)))

        # Group if all subtitle tracks are identical
        for index, (video_files, info) in enumerate(self.subtitle_info):
            if info == filtered_tracks:
                self.subtitle_info[index] = [video_files + [file], info]
                return

        # Create a group for this set of subtitle tracks if none were identical
        self.subtitle_info += [[[file], filtered_tracks]]

    def resync_subtitle(self, file, subtitle_channel):
        # Extract old subtitle
        extracted_subtitle = f"{file[:-4]}.extracted.ass"
        subprocess.run([
            "mkvextract",
            "tracks",
            file,
            f"{subtitle_channel}:{extracted_subtitle}"
        ])

        # Resync the mistimed subtitle based on the chosen (extracted) one
        mistimed_subtitle = self.subtitle_paths[self.video_paths.index(file)]
        output_subtitle = mistimed_subtitle
        
        subprocess.run([
            "alass.bat",
            extracted_subtitle,
            mistimed_subtitle,
            output_subtitle
        ])

        # Remove extracted subtitle
        os.remove(extracted_subtitle)

        return output_subtitle

    def filter_streams(self, audio_filter, subtitle_filter):
        for video_path in self.video_paths:
            subprocess.run([
                "mkvmerge",
                "-o", ".Filtered." + video_path,
                "-a", audio_filter,
                "-s", subtitle_filter,
                video_path
            ])

            os.replace(".Filtered." + video_path, video_path)
