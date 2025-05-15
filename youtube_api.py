# youtube_api.py
import os
from googleapiclient.discovery import build
from isodate import parse_duration
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_videos(query, max_results=20):
    # Step 1: Search videos
    search_response = youtube.search().list(
        q=query,
        part="id",
        type="video",
        maxResults=max_results,
        publishedAfter=(datetime.utcnow() - timedelta(days=14)).isoformat("T") + "Z"
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]
    
    # Step 2: Get video details
    details = youtube.videos().list(
        part="snippet,contentDetails",
        id=",".join(video_ids)
    ).execute()

    filtered_videos = []
    for item in details["items"]:
        duration = parse_duration(item["contentDetails"]["duration"]).total_seconds() / 60
        if 4 <= duration <= 20:
            filtered_videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']}",
                "duration": round(duration, 2),
                "published": item["snippet"]["publishedAt"]
            })

    return filtered_videos

if __name__ == "__main__":
    query = "Recent Football Highlights"
    videos = search_videos(query)
    for video in videos:
        print(f"Title: {video['title']}")
        print(f"URL: {video['url']}")
        print(f"Duration: {video['duration']} minutes")
        print(f"Published: {video['published']}")
        print()