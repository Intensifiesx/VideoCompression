import os
import subprocess
import sys

def resource_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, './ffmpeg/ffmpeg') # gets ffmpeg as a bundle (running executable)
    return os.path.join(os.path.abspath("."), './ffmpeg/ffmpeg') # gets ffmpeg as a directory (running script)

def compressVidUsingFFMPEG(input_file, output_file):
    # Tried using HEVC codec but it was not supported by other platforms
    # Tried using H.264 codec but it was not as efficient as HEVC
    # Issue about VP9 is that it is slow to encode
    # Command to compress video using VP9 codec
    # Alex: changed to mpeg4 which is not as slow as VP9, but some files get larger after compression
    # Alex: changed back to vp9 because mpeg4 barely compresses most of the time, but also encountered an issue with vp9 barely compressing for a 10 min video
    cmd = [
        resource_path(),
        '-i', input_file,               # Input file
        '-c:v', 'libvpx-vp9',           # vp9 codec
        '-b:v', '1M',                   # Target bitrate for video
        '-c:a', 'libopus',              # Opus audio codec
        output_file                     # Output file
    ]
    subprocess.run(cmd)

# Execution Check
if __name__ == "__main__":
    input_path = os.path.join(os.getcwd(), 'Input')
    output_path = os.path.join(os.getcwd(), 'Output')

    # Creates input and output folders
    for directory in [input_path, output_path]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created.")

    input = [os.path.join(input_path, file) for file in os.listdir(input_path)]

    for video in input:
        file_name = os.path.splitext(os.path.basename(video))[0]
        inputSize = os.path.getsize(video) / (1024 * 1024)

        output = os.path.join(output_path, file_name + '_COMPRESSED.mp4')
        compressVidUsingFFMPEG(video, output)

        outputSize = os.path.getsize(output) / (1024 * 1024)

        print(f"Input file size: {inputSize:.2f} MB")
        print(f"Output file size: {outputSize:.2f} MB")
        print(f"Compression ratio: {inputSize / outputSize:.2f}")