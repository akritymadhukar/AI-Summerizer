from flask import request, jsonify
from extensions import app

from services import (
    get_summary,
    extract_pdf_text,
    extract_video_id,
    get_youtube_transcript,
)


@app.route("/summarize/text", methods=["POST"])
def summarize_text():

    data = request.get_json(silent=True) or {}
    text = data.get("text")

    if not text:
        return jsonify({"error": "Missing text"}), 400

    prompt = f"Summarize the following text:\n{text}"

    summary, error = get_summary(prompt)

    if error:
        return jsonify({"error": error}), 502

    return jsonify({"summary": summary})


@app.route("/summarize/pdf", methods=["POST"])
def summarize_pdf():

    if "file" not in request.files:
        return jsonify({"error": "Missing file"}), 400

    text, error = extract_pdf_text(request.files["file"])

    if error:
        return jsonify({"error": error}), 400

    if not text.strip():
        return jsonify({"error": "No text found"}), 400

    prompt = f"Summarize the following PDF content:\n{text}"

    summary, error = get_summary(prompt)

    if error:
        return jsonify({"error": error}), 502

    return jsonify({"summary": summary})


@app.route("/summarize/youtube", methods=["POST"])
def summarize_youtube():

    data = request.get_json(silent=True) or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing url"}), 400

    video_id = extract_video_id(url)

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    text, error = get_youtube_transcript(video_id)

    if error:
        return jsonify({"error": error}), 400

    prompt = f"Summarize this YouTube video transcript:\n{text}"

    summary, error = get_summary(prompt)

    if error:
        return jsonify({"error": error}), 502

    return jsonify({"summary": summary})