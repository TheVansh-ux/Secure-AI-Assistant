import cv2
import numpy as np
import face_recognition
import os
import time
# --- THIS IS THE NEW, IMPROVED FUNCTION ---

def capture_and_encode_face(encoding_path):
    
    # Captures a face from the webcam, encodes it, and saves it to a file.
   
    cap = cv2.VideoCapture(0)
    
    print("Starting camera. Look at the camera and position your face.")
    print("Press 'c' to capture your face. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Find all face locations in the current frame
        face_locations = face_recognition.face_locations(frame)
        
        # Draw a rectangle around each detected face
        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Add instructions on the screen
        cv2.putText(frame, "Press 'c' to capture, 'q' to quit", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Display the video feed
        cv2.imshow('Face Registration', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            if face_locations:
                print("Capturing image...")
                face_encodings = face_recognition.face_encodings(frame, face_locations)
                
                if face_encodings:
                    known_face_encoding = face_encodings[0]
                    np.save(encoding_path, known_face_encoding)
                    print(f"Success! Face encoding saved to {encoding_path}")
                    break 
            else:
                print("No face detected. Position your face in the frame.")
        
        
        elif key == ord('q'):
            print("Registration cancelled by user.")
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
    # Check if the file was actually created to return a status
    return os.path.exists(encoding_path)
    


def verify_face(known_encoding_path):
  
    # Verifies a face from the webcam against a stored face encoding.

    # First, check if the encoding file exists
    if not os.path.exists(known_encoding_path):
        print("Error: Known face encoding file not found.")
        print("Please run the face registration first.")
        return False

    # Load the known face encoding from the file
    known_face_encoding = np.load(known_encoding_path)

    cap = cv2.VideoCapture(0)
    
    print("Verifying face... Please look at the camera.")
    
    # Give the user 5 seconds to show their face
    start_time = time.time()
    verified = False
    
    while time.time() - start_time < 5: # Loop for 5 seconds
        ret, frame = cap.read()
        if not ret:
            break

        # Find all faces and their encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Assume the user is unauthorized until verified
        name = "Unauthorized"
        color = (0, 0, 255) # Red for unauthorized

        for face_encoding, face_loc in zip(face_encodings, face_locations):
            # The core of the verification: compare the live face to the saved one
            matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
            
            # If a match is found
            if True in matches:
                name = "Authorized"
                color = (0, 255, 0) # Green for authorized
                verified = True

            # Draw a box around the face and display the name
            top, right, bottom, left = face_loc
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # Display the resulting image
        cv2.imshow('Face Verification', frame)

        # If we found a match, we can stop early
        if verified:
            time.sleep(1) # Pause for 1 second to show "Authorized"
            break
        
        # Allow quitting with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    return verified

