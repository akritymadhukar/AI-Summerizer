from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
import fitz
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")


def get_summary(prompt):
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        return response.text, None
    except Exception as e:
        return None, str(e)


def extract_pdf_text(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text, None
    except Exception as e:
        return None, f"Could not read PDF: {e}"


def extract_video_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]

    elif "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]

    return None


def get_youtube_transcript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        text = " ".join([snippet.text for snippet in fetched_transcript])
        return text, None
    except Exception as e:
        return None, f"Could not fetch transcript: {e}"