import speech_recognition as sr

def record_and_transcribe():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Listening... Please speak now.")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            return text
    except sr.WaitTimeoutError:
        return "⚠️ Mic timed out. Please try again."
    except sr.UnknownValueError:
        return "⚠️ Couldn't understand. Speak clearly."
    except Exception as e:
        return f"❌ Error: {e}"
