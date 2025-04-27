#======Libraries======
import sys
import os
import subprocess
from datetime import datetime, date
import shutil

os.system(f'pip install -r requirements.txt --no-deps')

import imageio_ffmpeg as iio_ffmpeg

#======Function Definitions======
def resourcePath():
    """Locates the FFmpeg file resource."""
    ffmpeg_path = iio_ffmpeg.get_ffmpeg_exe()
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ffmpeg_path)
    return ffmpeg_path

def getGPUAccelerationFlags():
    """Detects available GPU acceleration options and returns appropriate FFmpeg flags."""
    try:
        # Check NVIDIA CUDA (most common)
        subprocess.run([resourcePath(), '-hide_banner', '-encoders'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {
            'codec': 'h264_nvenc',
            'flags': ['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda']
        }
    except:
        try:
            # Check AMD AMF
            return {
                'codec': 'h264_amf',
                'flags': []
            }
        except:
            try:
                # Check Intel QuickSync
                return {
                    'codec': 'h264_qsv',
                    'flags': ['-hwaccel', 'qsv']
                }
            except:
                # Fallback to CPU
                return {
                    'codec': 'libvpx-vp9',
                    'flags': []
                }

def compressVidUsingFFMPEG(input_file, output_file):
    """
    Uses FFmpeg to compress a video file.
    High-quality compression with efficient file size reduction.

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
    gpu_config = getGPUAccelerationFlags()
    
    base_cmd = [
        resourcePath(),
        '-n',                          # Overwrite output
        '-hwaccel', 'auto',            # Auto GPU detection
        '-i', input_file,              # Input file
        '-movflags', '+faststart',     # Web optimization
        '-pix_fmt', 'yuv420p',        # Standard format
        '-vsync', '0'                 # No duplicate frames
    ]

    # GPU-specific optimized settings
    if gpu_config['codec'] == 'h264_nvenc':  # NVIDIA
        cmd = base_cmd + [
            '-c:v', 'h264_nvenc',
            '-preset', 'p6',           # Quality-focused preset
            '-rc', 'vbr',              # Smart variable bitrate
            '-cq', '28',               # Quality level (28=good balance)
            '-b:v', '0',               # Let CQ control bitrate
            '-spatial-aq', '1',
            '-temporal-aq', '1',
            '-qmin', '24',             # Min quality threshold
            '-qmax', '32'              # Max quality threshold
        ]
    elif gpu_config['codec'] == 'h264_amf':  # AMD
        cmd = base_cmd + [
            '-c:v', 'h264_amf',
            '-quality', 'balanced',
            '-rc', 'vbr_quality',
            '-qp_i', '26',
            '-qp_p', '28',
            '-qp_b', '30',
            '-preanalysis', 'true'
        ]
    else:  # Intel QuickSync
        cmd = base_cmd + [
            '-c:v', 'h264_qsv',
            '-global_quality', '28',
            '-look_ahead', '1'
        ]

    # Audio settings (efficient compression)
    cmd.extend([
        '-c:a', 'aac',
        '-b:a', '96k',                 # Slightly lower audio bitrate
        '-ar', '44100',                # Standard sampling rate
        output_file
    ])

    print("Executing:", ' '.join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error compressing {input_file}: {e}")
        raise
    
#======Execution Check======
if __name__ == "__main__":
    # Executable
    inputPath = os.path.join(os.getcwd(), 'Input')
    outputPath = os.path.join(os.getcwd(), 'Output')
    initPaths = False

    totalInputSize = 0
    totalOutputSize = 0
    totalVideos = 0

    # Creates input and output folders
    for directory in [inputPath, outputPath]:
        if not os.path.exists(directory):
            initPaths = True
            os.makedirs(directory)
            print(f"Directory '{directory}' created.")

    input = [os.path.join(inputPath, file) for file in os.listdir(inputPath)]
    log = os.path.join(os.getcwd(), 'log.txt')

    with open(log, 'a') as logFile:
        logFile.write("================================================\n")
        logFile.write(f"Compression Log ({date.today()})\n")

    for video in input:
        fileName = os.path.splitext(os.path.basename(video))[0]
        inputSize = os.path.getsize(video) / (1024 * 1024)  # Size in MB
        
        output = os.path.join(outputPath, fileName + '_COMPRESSED.mp4')
        compressVidUsingFFMPEG(video, output)
        outputSize = os.path.getsize(output) / (1024 * 1024)
        
        # Calculate compression metrics
        sizeReduction = inputSize - outputSize
        compressionRatio = inputSize / max(outputSize, 0.001)  # Prevent division by zero
        percentReduction = (sizeReduction / inputSize) * 100 if inputSize > 0 else 0

        # Update totals
        totalInputSize += inputSize
        totalOutputSize += outputSize
        totalVideos += 1

        # Enhanced logging
        with open(log, 'a') as logFile:
            logFile.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {fileName}\n")
            
            # Handle negative compression (output larger than input)
            if outputSize >= inputSize:
                logFile.write(f"\t[WARNING]: Compression ratio - {compressionRatio:.2} is less than 1. Removing output file and replacing with uncompressed.\n")
                os.remove(output)
                shutil.copy2(video, output)  # Preserve original with correct metadata
                outputSize = inputSize
                sizeReduction = 0.0
                percentReduction = 0.0

            logFile.write(f"\tVideo #{totalVideos} of {len(input)}\n")
            logFile.write(f"\tInput: {inputSize:.2f}MB\n")
            logFile.write(f"\tOutput: {outputSize:.2f}MB\n")
            logFile.write(f"\tSaved: {sizeReduction:.2f}MB ({percentReduction:.1f}%)\n")

    # Write footer after all videos are processed
    with open(log, 'a') as logFile:
        logFile.write("------------------------------------------------\n")
        logFile.write(f"Batch completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        logFile.write(f"Total input size: {totalInputSize:.2f} MB\n")
        logFile.write(f"Total output size: {totalOutputSize:.2f} MB\n")
        logFile.write(f"Saved: {totalInputSize - totalOutputSize:.2f} MB\n")
        logFile.write(f"Total videos processed: {totalVideos}\n")
        logFile.write("================================================\n\n\n")

    if hasattr(sys, '_MEIPASS'):
        os.system("pause") # Pauses for executable

