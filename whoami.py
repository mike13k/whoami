import face_recognition
import cv2
import glob, os
from os.path import splitext
import annotate
import base64
import io
import sys

reload(sys)
sys.setdefaultencoding('utf8')

owd = os.getcwd()

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


## Prof. Dr. Slim Abdennadher
os.chdir('pics/ProfSlim')

pics = glob.glob('*.jpg')

known_face_encodings = []
known_face_names = []
smiles = []

# Load sample pictures and learn how to recognize it.
for pic in pics:
    img = face_recognition.load_image_file(pic)
    encoding = face_recognition.face_encodings(img)
    if len(encoding) > 0:
        img_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(img_encoding)
        known_face_names.append('Prof. Dr. Slim Abdennadher')
        smiles.append(False)


## Prof. Dr. Ashraf Mansour
os.chdir(owd)
os.chdir('pics/ProfAshraf')

pics = glob.glob('*.jpg')

# Load sample pictures and learn how to recognize it.
for pic in pics:
    img = face_recognition.load_image_file(pic)
    encoding = face_recognition.face_encodings(img)
    if len(encoding) > 0:
        img_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(img_encoding)
        known_face_names.append('Prof. Dr. Ashraf Mansour')
        smiles.append(False)

## Michael Khalil
os.chdir(owd)
os.chdir('pics/Mike')

pics = glob.glob('*.jpg')

# Load sample pictures and learn how to recognize it.
for pic in pics:
    img = face_recognition.load_image_file(pic)
    encoding = face_recognition.face_encodings(img)
    if len(encoding) > 0:
        img_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(img_encoding)
        known_face_names.append('Michael Khalil')
        smiles.append(False)


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
color = (0, 0, 0)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                # big_frame = cv2.resize(frame, (0, 0), fx=2.0, fy=2.0)
                # rgb_big_frame = big_frame[:, :, ::-1].copy(order='C')
                os.chdir(owd)
                cv2.imwrite('detect.jpg', small_frame)
                with open('detect.jpg', 'rb') as f:
                    image_to_annotate = f.read()
                smiles[first_match_index] = annotate.annotate_image(image_to_annotate)
                print(smiles[first_match_index])

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        if name == "Unknown":
            color = (0, 0, 225)
        else:
            color = (0, 128, 128)

        index = known_face_names.index(name)

        if(smiles[index]):

            color = (0, 255, 0)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "Nice Smile!", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        else:
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, 'Hello ' + name + ', I heard you have the best smile', (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
