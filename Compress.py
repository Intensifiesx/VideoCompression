import os
import subprocess

def compressVidUsingFFMPEG(input_file, output_file):
    # Tried using HEVC codec but it was not supported by other platforms
    # Tried using H.264 codec but it was not as efficient as HEVC
    # Issue about VP9 is that it is slow to encode
    # Command to compress video using VP9 codec
    cmd = [
        'ffmpeg',
        '-i', input_file,               # Input file
        '-c:v', 'libvpx-vp9',           # VP9 codec
        '-b:v', '1M',                   # Target bitrate for video
        '-c:a', 'libopus',              # Opus audio codec
        output_file                     # Output file
    ]
    subprocess.run(cmd)

input = os.path.join(os.getcwd(), 'VIDEO.mp4')                  # CHANGE THIS TO YOUR INPUT FILE
output = os.path.join(os.getcwd(), 'VIDEO_COMPRESSED.mp4')       # CHANGE THIS TO YOUR OUTPUT FILE

inputSize = os.path.getsize(input) / (1024 * 1024)

compressVidUsingFFMPEG(input, output)

outputSize = os.path.getsize(output) / (1024 * 1024)

print(f"Input file size: {inputSize:.2f} MB")
print(f"Output file size: {outputSize:.2f} MB")
print(f"Compression ratio: {inputSize / outputSize:.2f}")
input("Press Enter to continue...")