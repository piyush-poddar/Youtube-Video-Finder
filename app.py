import streamlit as st
from youtube_api import search_videos
from llm_analyzer import analyze_titles
from voice_input import get_voice_input

st.set_page_config(page_title="YouTube Finder AI", layout="centered")
st.title("🎥 YouTube Video Finder (with LLM Analysis)")

st.markdown("Search YouTube using **text or voice**, and get the best video recommended by Gemini.")

# Select input method
input_mode = st.radio("Choose Input Method:", ["Text", "Voice (English)", "Voice (Hindi)"])

# Input query
query = None
if input_mode == "Text":
    query = st.text_input("Enter your query:")
elif st.button("🎤 Record Voice"):
    lang_code = "en-IN" if "English" in input_mode else "hi-IN"
    with st.spinner("Listening..."):
        query = get_voice_input(lang_code)
        if query:
            st.success(f"Recognized: {query}")
        else:
            st.error("Could not recognize speech.")

# Process input
if query:
    st.divider()
    st.subheader("🔍 Searching YouTube...")
    videos = search_videos(query)

    if not videos:
        st.error("No videos found.")
    else:
        st.success(f"{len(videos)} videos found and filtered.")
        st.subheader("📹 Video List")
        for video in videos:
            st.markdown(f"- **{video['title']}**: [Watch here]({video['url']}) - {video['duration']} mins")
        st.subheader("🧠 Gemini Analysis in Progress...")
        response = analyze_titles(query, videos)

        # Parse LLM response to find best video
        try:
            best_index = int(response.strip().split('.')[0]) - 1
            best_video = videos[best_index]
            st.success("🎯 Best Video Recommendation")
            st.markdown(f"**Title:** {best_video['title']}")
            st.markdown(f"**Link:** [Watch here]({best_video['url']})")
            st.markdown(f"**Duration:** {best_video['duration']} mins")
        except:
            st.warning("⚠️ Couldn't parse Gemini response.")

        st.subheader("📝 Gemini's Explanation")
        st.markdown(response.split('.', 1)[1].strip())
