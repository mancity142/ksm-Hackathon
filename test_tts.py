from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY_HERE")

audio = client.generate(
    text="Hello from ElevenLabs!",
    voice="Rachel",
    model="eleven_multilingual_v2"
)

with open("output.mp3", "wb") as f:
    f.write(audio)
