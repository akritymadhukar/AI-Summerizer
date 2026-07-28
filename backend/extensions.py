from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    origins=[
        "http://localhost:5173",
        "https://ai-summerizer-nine.vercel.app"
    ]
)