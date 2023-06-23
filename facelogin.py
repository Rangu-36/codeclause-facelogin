import cv2
import face_recognition

# Load sample images and learn how to recognize them
known_images = [
    face_recognition.load_image_file("photo.jpg"),
    face_recognition.load_image_file("photo1.jpg"),
    face_recognition.load_image_file("photo1.jpg")
               ]

known_encodings = []
known_names = ["suchithra", "sushma", "suma"]

# Encode known face images
for image in known_images:
    encoding = face_recognition.face_encodings(image)[0]
    known_encodings.append(encoding)

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Start capturing video from the camera
video_capture = cv2.VideoCapture(0)

while True:
    # Capture video frame-by-frame
    ret, frame = video_capture.read()

    # Resize frame to speed up face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (OpenCV default) to RGB color
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame to save processing power
    if process_this_frame:
        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Check if the face matches any known face
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            # If a match is found, use the name of the known face
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with the name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()
