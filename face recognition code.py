import face_recognition
import cv2
import numpy as np
import os
import xlwt
from xlwt import Workbook
from datetime import date
import xlrd
from xlutils.copy import copy as xl_copy

# Get the current folder path
CurrentFolder = os.getcwd()
image = os.path.join(CurrentFolder, 'likith.png')
image2 = os.path.join(CurrentFolder, 'saandhya.png')

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Load a sample picture and encode the face
person1_name = "likith"
person1_image = face_recognition.load_image_file(image)
person1_face_encodings = face_recognition.face_encodings(person1_image)

person2_name = "saandhya"
person2_image = face_recognition.load_image_file(image2)
person2_face_encodings = face_recognition.face_encodings(person2_image)

# Check if faces were found before accessing
if len(person1_face_encodings) > 0:
    person1_face_encoding = person1_face_encodings[0]
else:
    print("No face found in likith.png")

if len(person2_face_encodings) > 0:
    person2_face_encoding = person2_face_encodings[0]
else:
    print("No face found in saandhya.png")

# Create known face encodings list
known_face_encodings = []
known_face_names = []

if len(person1_face_encodings) > 0:
    known_face_encodings.append(person1_face_encoding)
    known_face_names.append(person1_name)

if len(person2_face_encodings) > 0:
    known_face_encodings.append(person2_face_encoding)
    known_face_names.append(person2_name)

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Open attendance Excel sheet
try:
    rb = xlrd.open_workbook('attendence_excel.xls', formatting_info=True)
    wb = xl_copy(rb)
except FileNotFoundError:
    wb = Workbook()
    
inp = input('Please enter the subject name: ')
sheet1 = wb.add_sheet(inp)
sheet1.write(0, 0, 'Name/Date')
sheet1.write(0, 1, str(date.today()))

row = 1
col = 0
already_attendance_taken = ""

while True:
    # Capture frame from webcam
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert BGR to RGB
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Process every other frame
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Find the best match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            # Take attendance
            if name != "Unknown" and already_attendance_taken != name:
                sheet1.write(row, col, name)
                col += 1
                sheet1.write(row, col, "Present")
                row += 1
                col = 0
                print(f"Attendance taken for {name}")
                wb.save('attendence_excel.xls')
                already_attendance_taken = name
            else:
                print("Next student")

    process_this_frame = not process_this_frame

    # Draw bounding box
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Show video
    cv2.imshow('Video', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
