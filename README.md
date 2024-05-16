# Video Compression using Python and FFMPEG

This script uses the FFMPEG library to compress video files. It uses the VP9 codec for video and the Opus codec for audio.

## Prerequisites

-   Python 3.10 or greater
-   FFMPEG
-   PyInstaller (for building executable)

## Script Usage

1. Clone the repository.
2. Download the FFMPEG library from [here](https://ffmpeg.org/download.html).
3. Extract the contents and place the `ffmpeg` executable in the `ffmpeg/` directory.
4. Run the `Compress.py` script once to generate the `Input/` and `Output/` directories.
5. Move uncompressed videos to the `Input/` directory.
6. Run `Compress.py` to compress the videos. The compressed videos will be in the `Output/` directory.

## Build Usage

1. Clone the repository.
2. Download the FFMPEG library from [here](https://ffmpeg.org/download.html).
3. Extract the contents and place the `ffmpeg` executable in the `ffmpeg/` directory.
4. Install PyInstaller from [here](https://pyinstaller.org/en/stable/).
5. Run this command to build the executable: `pyinstaller -F --add-data "./ffmpeg/*;./ffmpeg/" Compress.py`.
6. Run `Compress.exe` in the `dist/` directory.
