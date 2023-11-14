import base64
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import cv2
from http.server import HTTPServer, SimpleHTTPRequestHandler, test

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

@app.get('/')
async def read_root():
    return {"Message": "Detect Object!"}

@app.get('/detect/')
async def detect_objects():
    video_path = 'bottle.mp4'

    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(3))
    height = int(cap.get(4))

    if not cap.isOpened():
        print("Error opening video stream or file")

    # Read the video frames
    frame_count = 0
    while cap.isOpened():
        detections = np.empty((0, 5))
        ret, frame = cap.read()

        if not ret:
            print("Error reading frames")
            break
        frame = cv2.resize(frame, (640, 480))
        code = base64.b64encode(frame)
        return {"frame": code}
