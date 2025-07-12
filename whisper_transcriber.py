import whisper
import tempfile

def transcribe_audio_file(audio_file):
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        temp_path = tmp.name

    # Load Whisper model
    model = whisper.load_model("base")  # You can try "small", "medium" if system allows
    result = model.transcribe(temp_path)

    return result["text"]
