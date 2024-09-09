

# Audio Compression and Transformation (Work in progress - demo project for my learning path)

## Overview

This project explores audio compression and transformation techniques using Python. It involves speeding up an audio file, compressing it, and then restoring the original quality(not yet ..!) and length. The project utilizes libraries such as `librosa`, `soundfile`, and `pydub` to perform these operations. 

### Key Components
- **Worker Algorithm**: Speeds up the audio, compresses it using FLAC (lossless format), and saves the transformation data.
- **Observer Algorithm**: Decompresses the audio, restores the original length and quality(Not yet), and saves the result.

## Installation

To set up the project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/audcomp.git
   cd audcomp
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv venv
   # For Unix-based systems
   source venv/bin/activate
   # For Windows
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Ensure FFmpeg is Installed**:
   This project uses `pydub`, which requires FFmpeg. Install it using:
   ```bash
   # For Ubuntu/Debian
   sudo apt-get install ffmpeg
   # For macOS
   brew install ffmpeg
   ```

## Usage

**Run**
   ```python
   python3 app.py
   ```

1. **Worker Algorithm**:
   This will process an input audio file (`piano-88-bpm.wav`), speed it up, compress it, and save the result as `output_fast.flac`. It also prints out file sizes and durations.

2. **Observer Algorithm**:
   This will decompress the FLAC file, restore the original audio quality(not yet) and length, and save the restored file as `restored.wav`.

3. **Output files on project folder**
    There will be 2 more files generated in the project folder: `output_fast.flac` , `restored.wav`


## Files

- `app.py`: Contains the main algorithms for processing audio.
- `requirements.txt`: Lists project dependencies.
- `piano-88-bpm.wav`: Test audio loop made with Bitwig
