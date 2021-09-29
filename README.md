# TrackTuner
Automatically retime subtitles and filter audio/subtitle channels
Useful for language learns or anyone who wants to resync subtitles or get rid of extraneous audio/subtitle channels easily!

## Instructions
Either move the executable to a folder with your media and run it or add TrackTunner to your path and launch it via the terminal.
After this TrackTunner will automatically analyse your media and (potentially) ask which subtitle track to use as a reference when retiming.
Afterwards you can opt in/out of removing any irrelavent audio/subbtitle tracks.

## Advantages
Numerous scripts have been created to realign subtitles over the years however most suffer from one of three flaws:
1. Require to be moved around from folder to folder even though the executable is large in size (sometimes around half a gig!)
2. Request you to manually decide between several subtitle tracks, often rejecting your choice forcing you to rerun from the beginning
3. Provide fault results or take too long to run

TrackTuner attempts to overcome these by being as light weight and easy to use as possible.
The program is designed to work with other tools (which are easily available and often already installed) allowing it to be under 10 mb, automatically filters out non-selectable subtitle options from prompts and when only a single option is available automatically runs with it without annoying the user.
Additionally inputs are grouped together to ensure selections have to be made as few times as possible whilst keeping the results of retiming accurate.

## Dependencies
TrackTuner requires [ffmpeg](https://ffmpeg.org/), [alass](https://github.com/kaegi/alass) and the [MKVToolNix](https://mkvtoolnix.download/) packages (mkvmerge and mkvextract) to be installed/in the system path.
