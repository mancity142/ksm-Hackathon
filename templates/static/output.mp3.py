from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")

audio = client.generate(
    text="Hello from ElevenLabs!",
    voice="Rachel",
    model="eleven_multilingual_v2"
)

with open("output.mp3", "wb") as f:
    f.write(audio)
