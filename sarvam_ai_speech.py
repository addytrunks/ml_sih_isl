import requests
import base64
from dotenv import load_dotenv
import os
import sounddevice as sd
import numpy as np
import io
import wave
import json

load_dotenv()

def record_audio_to_base64(duration=5, samplerate=16000, channels=1):
    """
    Records audio in real-time, converts it to base64-encoded string.

    Parameters:
    - duration (int): Duration to record in seconds.
    - samplerate (int): Sampling rate of audio.
    - channels (int): Number of audio channels.

    Returns:
    - str: Base64-encoded audio string.
    """
    print("Recording... Speak now!")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype=np.int16)
    sd.wait()  # Wait for recording to finish
    print("Recording finished.")

    # Save audio data to a buffer in WAV format
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 2 bytes per sample for np.int16
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    # Encode buffer content to base64
    base64_audio = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return base64_audio

def speech_to_text(base64_audio,language_code="ta-IN"):
    """
    Sends a base64-encoded audio to the speech-to-text API and returns the transcribed text in the same language as the audio.
    
    Link: https://sarvam.ai/docs/speech-to-text

    Parameters:
    - base64_audio (str): Base64-encoded audio content.
    - language_code (str): Language code for transcription (default is "ta-IN").
        - Avalailable language codes: hi-IN, bn-IN, kn-IN, ml-IN, mr-IN, od-IN, pa-IN, ta-IN, te-IN, gu-IN
    - with_timestamps (bool): Whether to include timestamps in the transcription (default is False).

    Returns:
    - str: Transcribed text or error message from the API.
    """
    
    url = "https://api.sarvam.ai/speech-to-text"

    data = {
        "model": "saarika:v1",
        "language_code": language_code,
        "with_timestamps": "true"
    }

    files = {
        "file": ("input.wav", base64.b64decode(base64_audio), "audio/wav")
    }

    headers = {
    'api-subscription-key': os.getenv('SARVAM_API_KEY')
    }

    try:
        response = requests.post(url, data=data, files=files,headers=headers)
        return response.json()['transcript']
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def speech_to_text_translate(base64_audio):
    """
    Sends a base64-encoded audio file to the speech-to-text API and returns the transcribed text in english.
    
    Link: https://sarvam.ai/docs/speech-to-text-translate

    Parameters:
    - base64_audio (str): Base64-encoded audio content.

    Returns:
    - str: Transcribed text or error message from the API.
    """
    
    url = "https://api.sarvam.ai/speech-to-text-translate"

    data = {
        "model": "saaras:v1",
    }

    files = {
        "file": ("input.wav", base64.b64decode(base64_audio), "audio/wav")
    }

    headers = {
    'api-subscription-key': os.getenv('SARVAM_API_KEY')
    }

    try:
        response = requests.post(url, data=data, files=files,headers=headers)
        return response.json()['transcript']
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


base64_audio = record_audio_to_base64()

# Call the speech-to-text function
transcription = speech_to_text_translate(base64_audio)
print("Transcription:", transcription)