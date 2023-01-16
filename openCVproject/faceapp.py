from flask import Flask,render_template,Response
import cv2
import face_recognition
import numpy as np

app = Flask(__name__)

# VideoCapture(0) used to capture video from web cam
camera = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it
hasan_image = face_recognition.load_image_file("image/hasan.jpg")
hasan_face_encoding = face_recognition.face_encodings(hasan_image)[0]

# Load a second sample picture and learn how to recognize it
wazim_image = face_recognition.load_image_file("image/wazim.jpg")
wazim_face_encoding = face_recognition.face_encodings(wazim_image)[0]

# Load a second sample picture and learn how to recognize it
nazra_image = face_recognition.load_image_file("image/nazra.jpg")
nazra_face_encoding = face_recognition.face_encodings(nazra_image)[0]

# Load a second sample picture and learn how to recognize it
tazim_image = face_recognition.load_image_file("image/tazim.jpg")
tazim_face_encoding = face_recognition.face_encodings(tazim_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    hasan_face_encoding,
    wazim_face_encoding,
    nazra_face_encoding,
    tazim_face_encoding
]
known_face_names = [
    "hasan",
    "poliya",
    "nazra",
    "Kpop"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def generate_frames():
    while True:       
        # reading camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
    
            # Find all faces and face encodings in current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if face is a match for known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Or instead, use known face with smallest distance to new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

            # Display results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since frame detected, in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(debug=True)