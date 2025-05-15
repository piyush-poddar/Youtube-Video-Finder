# voice_input.py
import speech_recognition as sr

def get_voice_input(lang="en-IN"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nSpeak your query (Hindi or English)...")
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language=lang)
        print(f"Recognized: {query}")
        return query
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("API unavailable or error")
    return None


if __name__ == "__main__":
    query = get_voice_input()
    if query:
        print(f"Your query is: {query}")
    else:
        print("No valid input received.")