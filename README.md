# 🎬 Video Compression Tool with GPU Acceleration  
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue) ![FFmpeg](https://img.shields.io/badge/FFmpeg-5.0%2B-orange)

A high-performance video compression tool leveraging FFmpeg with automatic GPU acceleration for faster processing without sacrificing quality.  

## ✨ Features  
- **Smart Compression** - Automatically selects optimal settings based on your hardware  
- **GPU Acceleration** - Supports NVIDIA NVENC, AMD AMF, and Intel QuickSync  
- **Quality Preservation** - Maintains visual quality while reducing file sizes  
- **Batch Processing** - Compress multiple videos in one operation  
- **Detailed Logging** - Tracks compression ratios and savings  

## 🛠 Prerequisites  
- Python 3.10+  
- FFmpeg (will be automatically installed)  
- **For GPU acceleration**:  
  - NVIDIA: CUDA-enabled GPU with drivers  
  - AMD: Latest AMF drivers  
  - Intel: QuickSync-compatible CPU  

## 🚀 Installation  
```bash  
1. git clone https://github.com/Intensifiesx/VideoCompression.git
2. cd VideoCompression
3. Input videos into the `Input` folder.
3. Run the `run.bat` file to compress the videos.
4. View detailed logs in `log.txt`.
5. The compressed videos will be saved in the `Output` folder.
```

## 📝 Log Example
```
Compression Log (2025-04-26)
[2025-04-26 18:49:30] video1
	Video #762 of 765
	Input: 30.47MB
	Output: 8.33MB
	Saved: 22.14MB (72.7%)
[2025-04-26 18:50:37] video2
	[WARNING]: Compression ratio - 1.0 is less than 1. Removing output file and replacing with uncompressed.
	Video #1 of 765
	Input: 87.87MB
	Output: 87.87MB
	Saved: 0.00MB (0.0%)
[2025-04-26 18:50:38] video3
	Video #3 of 765
	Input: 40.59MB
	Output: 21.05MB
	Saved: 19.53MB (48.1%)
[2025-04-26 18:50:38] video4
	Video #4 of 765
	Input: 67.25MB
	Output: 17.53MB
	Saved: 49.72MB (73.9%)
....
....
[2025-04-26 19:10:56] video763
	Video #763 of 765
	Input: 10.64MB
	Output: 7.88MB
	Saved: 2.76MB (26.0%)
[2025-04-26 19:10:58] video764
	Video #764 of 765
	Input: 7.33MB
	Output: 7.19MB
	Saved: 0.14MB (1.9%)
[2025-04-26 19:11:03] video765
	[WARNING]: Compression ratio - 0.67 is less than 1. Removing output file and replacing with uncompressed.
	Video #765 of 765
	Input: 8.56MB
	Output: 8.56MB
	Saved: 0.00MB (0.0%)
------------------------------------------------
Batch completed at: 2025-04-26 19:11:03
Total input size: 35930.71 MB
Total output size: 19507.59 MB
Saved: 16423.12 MB
Total videos processed: 765
================================================
```

## 🤝 Contributing
Pull requests welcome! For major changes, please open an issue first.
