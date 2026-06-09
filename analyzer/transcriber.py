import whisper

model = whisper.load_model("small")

def transcribe_audio(audio_path):

    result = model.transcribe(
        audio_path,
        language="en"
    )

    return result["text"]