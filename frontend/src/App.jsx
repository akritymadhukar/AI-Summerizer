import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [mode, setMode] = useState("text");
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [file, setFile] = useState(null);
  const [youtubeURL, setYoutubeURL] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    setLoading(true);
    setSummary("");

    try {
      let res;

      if (mode === "text") {
        if (!text.trim()) {
          alert("Please enter some text");
          setLoading(false);
          return;
        }

        res = await axios.post(
          "http://localhost:5000/summarize/text",
          {
            text: text,
          }
        );
      } else if (mode === "pdf") {
        if (!file) {
          alert("Please upload a PDF file");
          setLoading(false);
          return;
        }

        const formData = new FormData();
        formData.append("file", file);

        res = await axios.post(
          "http://localhost:5000/summarize/pdf",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
      } else if (mode === "youtube") {
        if (!youtubeURL.trim()) {
          alert("Please enter a YouTube URL");
          setLoading(false);
          return;
        }

        res = await axios.post(
          "http://localhost:5000/summarize/youtube",
          {
            url: youtubeURL,
          }
        );
      }

      if (res && res.data) {
        setSummary(res.data.summary);
      }
    } catch (err) {
  console.error(err);

  if (err.response) {
    console.log(err.response.data);
    alert(err.response.data.error);
  } else {
    alert(err.message);
  }
}
    finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
      <h1 className="title">🧠 AI Summarizer</h1>

      <p className="subtitle">
      Summarize Text, PDFs and YouTube videos instantly using Gemini AI.
      </p>
      <div className="mode-buttons">
        <button
          className={mode === "text" ? "active" : ""}
          onClick={() => setMode("text")}
        >
          Text
        </button>

        <button
          className={mode === "pdf" ? "active" : ""}
          onClick={() => setMode("pdf")}
        >
          PDF
        </button>

        <button
          className={mode === "youtube" ? "active" : ""}
          onClick={() => setMode("youtube")}
        >
          YouTube
        </button>
      </div>

      {mode === "text" && (
        <textarea
          placeholder="Paste your text here..."
          rows={10}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      )}

      {mode === "pdf" && (
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
      )}

      {mode === "youtube" && (
        <input
          type="text"
          placeholder="Paste your YouTube video URL here..."
          value={youtubeURL}
          onChange={(e) => setYoutubeURL(e.target.value)}
        />
      )}

      <button className="summarize-btn" onClick={handleSummarize} disabled={loading}>
        {loading ? "Summarizing..." : "Summarize"}
      </button>

      {summary && (
        <div className="summary-box">
          <h2>📝 Summary</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  </div>
  );
}

export default App;