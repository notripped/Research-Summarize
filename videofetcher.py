from youtube_search import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def search_youtube(query, max_results=5):
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    return results

def get_video_summary(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item["text"] for item in transcript])
        summary = summarizer(full_text[:3000], max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Transcript unavailable: {e}"

def get_video_summaries(query):
    videos = search_youtube(query)
    summaries = []
    for video in videos:
        video_id = video["id"]
        title = video["title"]
        summary = get_video_summary(video_id)
        summaries.append({
            "title": title,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "summary": summary
        })
    return summaries
