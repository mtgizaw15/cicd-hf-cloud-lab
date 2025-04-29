import face_recognition
import cv2

def detect_faces(input_path, output_path):
    image = face_recognition.load_image_file(input_path)

    face_locations = face_recognition.face_locations(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for top, right, bottom, left in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imwrite(output_path, image)

    return len(face_locations)
