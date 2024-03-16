import cv2

# extract frames from the input video to images, with fps and frame count as return value
def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    source_fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(f"{output_folder}/frame_{count}.jpg", frame)
        count += 1
    cap.release()
    
    return source_fps, count