import speech_recognition as sr
import pyaudio
import wave

def record_and_transcribe():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            return text
    except sr.WaitTimeoutError:
        return "⚠️ Mic timed out. Please try again."
    except sr.UnknownValueError:
        return "⚠️ Couldn't understand. Speak clearly."
    except Exception as e:
        return f"❌ Error: {e}"

def record_audio_with_pyaudio(filename, duration=5):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
        frames = []
        for _ in range(0, int(fs / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
        return True
    except Exception as e:
        print(f"PyAudio error: {e}")
        return False
