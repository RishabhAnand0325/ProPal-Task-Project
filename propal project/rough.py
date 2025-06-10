import os
import requests
import subprocess
from deepgram import Deepgram
import google.generativeai as genai
import pygame
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import keyboard
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('api_keys.env')

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.0-flash")
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb" 

# Constants
API_KEY = ELEVENLABS_API_KEY
ELEVENLABS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"


AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}


def record_speech(output_file, samplerate=44100):
    print("Recording... Press Enter to stop.")

    audio_frames = []
    stream = sd.InputStream(samplerate=samplerate, channels=1, dtype=np.int16)
    stream.start()

    try:
        while not keyboard.is_pressed("enter"):
            data, _ = stream.read(1024)
            audio_frames.append(data)
    finally:
        stream.stop()
        stream.close()

    audio_data = np.concatenate(audio_frames, axis=0)
    write(output_file, samplerate, audio_data)
    print(f"Recording saved to {output_file}")
    return output_file



def speech_to_text(local_file_path):
    deepgram = Deepgram(DEEPGRAM_API_KEY)

    async def transcribe_file():
        with open(local_file_path, "rb") as audio:
            source = {"buffer": audio, "mimetype": "audio/wav"}  # Replace with your file's MIME type if different
            options = {"punctuate": True, "language": "en"}
            response = await deepgram.transcription.prerecorded(source, options)
            return response["results"]["channels"][0]["alternatives"][0]["transcript"]

    # Run the asynchronous transcription
    loop = asyncio.get_event_loop()
    transcript = loop.run_until_complete(transcribe_file())
    return transcript


def generate_conversation(text):
    prompt = f"""you are an AI assistant that is helping the user generate answer for the '{text}'
            
                        The tone and Style should be friendly and informal.
                        the generated answer should be like that two person that are friends are having a conversation with each other
            
                        -The generated answer should crisp and precise
                        -it doesnot contain any intro and outro just the generated answer
                        -the generated answer should have only one friend
                        -donot give multiple responses only give one response
                        -the generated answer should look like a conversation is building

                        Format:
                        generated answer

                        """
    response1 = model.generate_content(prompt).text.strip()
    return response1


def text_to_speech(text, output_file):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    # Send request to ElevenLabs API
    response = requests.post(ELEVENLABS_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        # Save audio content to a file
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Audio saved to {output_file}")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def play_audio(file_path):
    # Initialize the mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(file_path)

    # Play the MP3 file
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def main():
    print("enter(y/n)?")
    while True:
        
        if keyboard.is_pressed('y'):   
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            recorded_file = f"input_audio_{timestamp}.wav"
            record_speech(recorded_file) 
                
            res = speech_to_text(recorded_file)
            conversation = generate_conversation(res)
            print(f"query: {res} \n response: {conversation}")


            text = conversation
            audio_file = f"output_audio_{timestamp}.mp3"
    
            # Generate audio and play it
            text_to_speech(text, audio_file)
            play_audio(audio_file)

        if keyboard.is_pressed('n'):
            print("exiting conversation...")
            break
        

if __name__ == "__main__":
    main()
