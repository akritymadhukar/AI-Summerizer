from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
import fitz
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configurable so you're not hunting through code the next time Google retires a model.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")


def get_summary(prompt):
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        return response.text, None
    except Exception as e:
        return None, str(e)


@app.route('/summarize/text', methods=['POST'])
def summarize_text():
    data = request.get_json(silent=True) or {}
    text = data.get('text')

    if not text:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    prompt = f"Summarize the following text:\n{text}"

    summary, error = get_summary(prompt)
    if error:
        return jsonify({"error": error}), 502

    return jsonify({"summary": summary})


@app.route('/summarize/pdf', methods=['POST'])
def summarize_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "Missing 'file' in request"}), 400

    file = request.files['file']

    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
    except Exception as e:
        return jsonify({"error": f"Could not read PDF: {e}"}), 400

    if not text.strip():
        return jsonify({"error": "No extractable text found in PDF"}), 400

    prompt = f"Summarize the following PDF content:\n{text}"

    summary, error = get_summary(prompt)
    if error:
        return jsonify({"error": error}), 502

    return jsonify({"summary": summary})


@app.route('/summarize/youtube', methods=['POST'])
def summarize_youtube():
    data = request.get_json(silent=True) or {}
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
    elif "watch?v=" in url:
        video_id = url.split("watch?v=")[-1].split("&")[0]
    else:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
    except Exception as e:
        return jsonify({"error": f"Could not fetch transcript: {e}"}), 400

    text = " ".join([snippet.text for snippet in fetched_transcript])

    prompt = f"Summarize this YouTube video transcript:\n{text}"

    summary, error = get_summary(prompt)
    if error:
        return jsonify({"error": error}), 502

    return jsonify({"summary": summary})


if __name__ == "__main__":
    app.run(debug=True)