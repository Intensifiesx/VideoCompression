#======Libraries======
import sys
import os

# Prevents script from being executed directly (allows run.bat and executable)
if (not "--from-batch" in sys.argv) and (not hasattr(sys, '_MEIPASS')):
    print("Please do not run this Python script directly. Use 'run.bat' to use this script.")
    os.system("pause")
    sys.exit(1)

import subprocess
import fnmatch
import imageio_ffmpeg as iio_ffmpeg
# import ffmpeg

#======Function Definitions======
def resource_path():
    """
    Locates the FFmpeg file resource.

    Parameters:
    None

    Returns:
    string: file path
    """
    if hasattr(sys, '_MEIPASS'):
        # gets ffmpeg as a bundle (running executable)
        directory_path = os.path.join(sys._MEIPASS, 'imageio_ffmpeg', 'binaries')
    else:
        # gets ffmpeg as a directory (running script)
        directory_path = os.path.join(os.path.abspath("."), os.pardir, 'Lib', 'site-packages', 'imageio_ffmpeg', 'binaries')

    files_in_directory = os.listdir(directory_path)
    pattern = 'ffmpeg-win64-v*.exe'
    matching_files = fnmatch.filter(files_in_directory, pattern)
    matching_file_path = os.path.join(directory_path, matching_files[0])
    return matching_file_path

def compressVidUsingFFMPEG(input_file, output_file):
    """
    Uses FFmpeg to compress a video file.

    Parameters:
    input_file string: input file path
    output_file string: output file path

    Returns:
    None
    """
    # Tried using HEVC codec but it was not supported by other platforms
    # Tried using H.264 codec but it was not as efficient as HEVC
    # Issue about VP9 is that it is slow to encode
    # Command to compress video using VP9 codec
    # Alex: changed to mpeg4 which is not as slow as VP9, but some files get larger after compression
    # Alex: changed back to vp9 because mpeg4 barely compresses most of the time, but also encountered an issue with vp9 barely compressing for a 10 min video
    # NEW WAY:
        # ffmpeg.input(input_file).output(output_file, vcodec='libvpx-vp9', b='1M', acodec='libopus').run(cmd=iio_ffmpeg.get_ffmpeg_exe())
    cmd = [
        resource_path(),
        '-i', input_file,               # Input file
        '-c:v', 'libvpx-vp9',           # vp9 codec
        '-b:v', '1M',                   # Target bitrate for video
        '-c:a', 'libopus',              # Opus audio codec
        '-b:a', '128k',                 # Target bitrate for Opus audio (example: 128 kbps)
        '-strict', '-2',
        output_file                     # Output file
    ]
    subprocess.run(cmd)
    
#======Execution Check======
if __name__ == "__main__":
    # Executable
    if hasattr(sys, '_MEIPASS'):
        inputPath = os.path.join(os.getcwd(), 'Input')
        outputPath = os.path.join(os.getcwd(), 'Output')
    # Script
    else:
        inputPath = os.path.join(os.getcwd(), '../../Input')
        outputPath = os.path.join(os.getcwd(), '../../Output')
    initPaths = False

    # Creates input and output folders
    for directory in [inputPath, outputPath]:
        if not os.path.exists(directory):
            initPaths = True
            os.makedirs(directory)
            print(f"Directory '{directory}' created.")

    if initPaths:
        print("Please add video files to the 'Input' folder and run the script again.")
        if hasattr(sys, '_MEIPASS'):
            os.system("pause") # Pauses for executable
        sys.exit()

    input = [os.path.join(inputPath, file) for file in os.listdir(inputPath)]

    for video in input:
        file_name = os.path.splitext(os.path.basename(video))[0]
        inputSize = os.path.getsize(video) / (1024 * 1024)

        output = os.path.join(outputPath, file_name + '_COMPRESSED.mp4')
        compressVidUsingFFMPEG(video, output)

        outputSize = os.path.getsize(output) / (1024 * 1024)

        print(f"Input file size: {inputSize:.2f} MB")
        print(f"Output file size: {outputSize:.2f} MB")
        print(f"Compression ratio: {inputSize / outputSize:.2f}")
        
    print("Compression complete.")

    if hasattr(sys, '_MEIPASS'):
        os.system("pause") # Pauses for executable
