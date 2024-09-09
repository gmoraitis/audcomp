import numpy as np
import librosa
import soundfile as sf
from scipy.fft import fft, ifft
from pydub import AudioSegment
import os
import pandas as pd

# Helper function to get file size in MB
def file_size_info(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)

# Worker algorithm: Speed up and compress the audio file using FLAC
def worker_algorithm(input_file, output_file, speed_factor):
    # Load the audio
    y, sr = librosa.load(input_file, sr=None)

    # Apply Fourier Transform to convert the signal to frequency domain
    fft_y = fft(y)
    
    # Speed up the audio in the time domain
    y_fast = librosa.effects.time_stretch(y, rate=speed_factor)
    
    # Get FFT of the sped-up signal
    fft_y_fast = fft(y_fast)

    # Save the sped-up audio temporarily (to WAV format)
    temp_fast_output = 'temp_fast_output.wav'
    sf.write(temp_fast_output, y_fast, sr)
    
    # Compress the sped-up file using FLAC (lossless)
    audio_fast = AudioSegment.from_wav(temp_fast_output)
    audio_fast.export(output_file, format="flac")

    # Remove the temporary WAV file
    os.remove(temp_fast_output)

    # Capture transformation data
    transformation_data = {
        'speed_factor': speed_factor,
        'original_duration': len(y) / sr,
        'compressed_duration': len(y_fast) / sr,
        'fft_original': fft_y,
        'fft_fast': fft_y_fast
    }

    # Get file sizes
    original_size = file_size_info(input_file)
    compressed_size = file_size_info(output_file)
    
    # Print file sizes using pandas
    df = pd.DataFrame({
        "File": ["Original File", "Compressed (FLAC) File"],
        "Duration (s)": [len(y) / sr, len(y_fast) / sr],
        "Size (MB)": [original_size, compressed_size]
    })
    print(df)

    return transformation_data

# Observer algorithm: Decompress and restore the original file
def observer_algorithm(input_file, output_file, transformation_data):
    # Decompress the FLAC file to WAV
    audio_fast = AudioSegment.from_file(input_file, format="flac")
    temp_wav_output = "temp_restored_output.wav"
    audio_fast.export(temp_wav_output, format="wav")

    # Load the decompressed audio
    y_fast, sr = librosa.load(temp_wav_output, sr=None)
    
    # Reverse the speed-up in the time domain
    y_restored = librosa.effects.time_stretch(y_fast, rate=1 / transformation_data['speed_factor'])
    
    # TODO Apply inverse FFT to get back to the time domain (not yet done..)
    fft_restored = ifft(transformation_data['fft_fast'])
    y_final = np.real(fft_restored)

    # Save the restored audio
    sf.write(output_file, y_restored, sr)

    # Remove the temporary WAV file
    os.remove(temp_wav_output)

    # Get the file sizes
    restored_size = file_size_info(output_file)
    
    # Print restored file size using pandas
    df = pd.DataFrame({
        "File": ["Restored File"],
        "Duration (s)": [len(y_restored) / sr],
        "Size (MB)": [restored_size]
    })
    print(df)

# Apply worker algorithm
transformation_data = worker_algorithm('piano-88-bpm.wav', 'output_fast.flac', 4.0)

# Apply observer algorithm
observer_algorithm('output_fast.flac', 'restored.wav', transformation_data)


# TODO A feature to run the observer from an audio player and transform the music in real time(more work in ideas here !!!)  
# def observer_in_memory(input_file, transformation_data):
#     # Load the sped-up audio into memory (as bytes)
#     y_fast, sr = librosa.load(input_file, sr=None)
    
#     # Reverse the speed-up in the time domain
#     y_restored = librosa.effects.time_stretch(y_fast, transformation_data['speed_factor'])

#     # Store the decompressed audio in-memory instead of writing to disk
#     buffer = io.BytesIO()
#     sf.write(buffer, y_restored, sr, format='WAV')

#     # Return the in-memory audio file for further use
#     buffer.seek(0)  # Rewind the buffer to the beginning
#     return buffer

# # Usage
# buffer = observer_in_memory('output_fast_v2.wav', transformation_data)

# # `buffer` contains the expanded audio data in memory.
# # Pass this to an audio player.