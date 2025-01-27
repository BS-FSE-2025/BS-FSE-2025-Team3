import cv2

# Replace with your RTSP stream URL
RTSP_URL = "rtsp://mohamad:mohamad2005200iq@10.0.0.9:554/stream1"

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Error: Cannot open RTSP stream")
else:
    print("RTSP stream is working!")

cap.release()
