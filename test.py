import cv2
import numpy as np
from keras.models import load_model

# Load the pre-trained model and other resources
model = load_model('model_file_30epochs.h5')
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

def detect_emotion_from_frame():
    # Open the video feed
    video = cv2.VideoCapture(0)
    ret, frame = video.read()
    if not ret:
        video.release()
        return "Error: Unable to access the camera."

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 3)

    if len(faces) == 0:
        video.release()
        return "No face detected."

    for x, y, w, h in faces:
        sub_face_img = gray[y:y + h, x:x + w]
        resized = cv2.resize(sub_face_img, (48, 48))
        normalize = resized / 255.0
        reshaped = np.reshape(normalize, (1, 48, 48, 1))
        result = model.predict(reshaped)
        label = np.argmax(result, axis=1)[0]
        video.release()
        return labels_dict[label]

    video.release()
    return "No face detected."
