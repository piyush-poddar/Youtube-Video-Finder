# main.py
from youtube_api import search_videos
from llm_analyzer import analyze_titles
from voice_input import get_voice_input

def choose_input_method():
    print("\nChoose input method:")
    print("1. Voice (Hindi or English)")
    print("2. Text")
    choice = input("Enter 1 or 2: ")
    if choice.strip() == "1":
        lang = input("Type language - 'en-IN' for English or 'hi-IN' for Hindi: ").strip()
        return get_voice_input(lang)
    else:
        return input("Type your query: ")

if __name__ == "__main__":
    query = choose_input_method()
    if not query:
        print("No input received.")
        exit()

    print("\nSearching YouTube...")
    videos = search_videos(query)

    if not videos:
        print("No relevant videos found.")
        exit()

    print(f"Found {len(videos)} videos. ")
    print("Video List:")
    for i, video in enumerate(videos):
        print(f"{i + 1}. {video['title']} - ({video['duration']} mins)")

    print("\n🧠 Analyzing titles with Gemini...")
    result = analyze_titles(query, videos)

    try:
        selected_index = int(result.split('.')[0]) - 1
        selected_video = videos[selected_index]

        print("\nBest Video Recommendation:")
        print(f"Title: {selected_video['title']}")
        print(f"URL: {selected_video['url']}")
        print(f"Duration: {selected_video['duration']} mins")
        print(f"Reason: {result.split('.', 1)[1].strip()}")
    except Exception as e:
        print("Error parsing Gemini response:", result)
