# Video Compression using Python and FFMPEG

This script uses the FFMPEG library to compress video files. It uses the VP9 codec for video and the Opus codec for audio.

## Prerequisites

- Python 3.10 or greater

## Script Usage

1. Clone the repository.
2. Run `run.bat` twice. Once to create the `venv` folder and again to generate the `/Input` and `/Output` directories.
3. Move uncompressed videos to the `/Input` directory.
4. Run `run.bat` to compress the videos. The compressed videos will be in the `Output/` directory.
5. Repeat steps 3-5 for subsequent sessions.

## Build Usage

1. Clone the repository.
2. Run `build_binaries.bat` once to create the `venv` folder.
3. Run `build_binaries.bat` again to compile `Compress.exe`.
4. Run `Compress.exe` in the `/dist` directory to generate the `/Input` and `/Output` directories.
5. Move uncompressed videos to the `/Input` directory.
6. Run `Compress.exe` to compress the videos. The compressed videos will be in the `Output/` directory.
7. Repeat steps 5-7 for subsequent sessions.
