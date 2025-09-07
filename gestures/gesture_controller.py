import cv2
import mediapipe as mp
import time
import datetime
import webbrowser
from assistant.voice_assistant import speak

# initialize mediapipe hands solution
mp_hands= mp.solutions.hands
#this main hands object will do the detection
# min_detection_confidence is the minimum confidence value for a hand detection to be considered successful
hands= mp_hands.Hands(min_detection_confidence= 0.7, min_tracking_confidence= 0.7)

# it will draw hand landmarks and connections on image
mp_draw= mp.solutions.drawing_utils

def detect_gesture(frame, landmarks):

# Detects a specific gesture based on hand landmark positions.
# Args:
#     frame: The camera frame, used to get image dimensions.
#     landmarks: A list of hand landmarks detected by MediaPipe.
# Returns:
#     str: A string representing the detected gesture name.

    tip_ids= [4,8,12,16,20] # Landmark indices for the tips of the fingers

    #get coordinates foe each landmark
    lm_list=[] 
    h, w, c = frame.shape
    for id, lm in enumerate(landmarks.landmark):
        cx, cy= int(lm.x * w), int(lm.y * h)
        lm_list.append([id, cx, cy])
    
    if not lm_list:
        return "Unknown"
    
    fingers= []

    # Thumb Logic
    # Checks if the thumb tip is horizontally to the right of the joint below it (for a right hand)
    if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1] :
        fingers.append(1) #Thumb is open
    else:
        fingers.append(0) #thumb is closed
    
    # other 4 finger logic
    for id in range(1,5):
        # Checks if the fingertip's Y-coordinate is above the joint two points below it
        if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2] :
            fingers.append(1) # finger is open
        else:
            fingers.append(0) # finger is closed
    
    total_fingers = fingers.count(1)

    #gesture mapping logic
    if total_fingers == 5:
        return "Palm"
    elif total_fingers == 1 and fingers[0] == 1 :
        return "Thumbs Up"
    elif total_fingers == 2 and fingers[1] == 1 and fingers[2] == 1:
        return "V-Sign"
    elif total_fingers == 1 and fingers[1] == 1:
        return "One finger"
    elif total_fingers == 0 :
        return "Fist"
    elif total_fingers == 2 and fingers[0] == 1 and fingers[4] == 1:
        return "Call Me"
    
    return "Unknown"




def run_gesture_controller():
    cap= cv2.VideoCapture(0)
    print("Gesture control mode activated. Show your hand to the camera.")
    speak("Gesture control activated.")
    print("Press 'q' to exit this mode.")

    last_action_time = 0
    action_cooldown = 5.0


    while True:
        success, frame= cap.read()
        if not success:
            print("Failed to capture image from camera.")
            break

        # Flip the frame horizontally for a later selfie-view display
        # and convert the BGR image to RGB.
        frame= cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.

        frame.flags.writeable= False
        results= hands.process(frame)

        # draw hand annotations on image
        frame.flags.writeable= True
        frame= cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        gesture_name = "Unknown"

        if results.multi_hand_landmarks:
             # loop through all detected hands
             for hand_landmarks in results.multi_hand_landmarks:
                 # it will draw skeleton of hand
                 mp_draw.draw_landmarks(
                     frame, 
                     hand_landmarks,
                     mp_hands.HAND_CONNECTIONS)
                 gesture_name = detect_gesture(frame, hand_landmarks)

        current_time = time.time()
        if gesture_name != "Unknown" and (current_time - last_action_time) > action_cooldown:
            
            if gesture_name == "V-Sign":
                print("Action: Opening YouTube")
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")
                last_action_time = current_time # Reset cooldown

            elif gesture_name == "Palm":
                print("Action: Palm (Stopping)")
                speak("Stopping gesture control.")
                break # Exit the loop and stop gesture control

            elif gesture_name == "Thumbs Up":
                print("Action: Thumbs Up (Affirmation)")
                speak("You're doing a great job on this project!")
                last_action_time = current_time

            elif gesture_name == "One Finger":
                print("Action: One Finger (Date & Time)")
                now = datetime.datetime.now()
                current_time_str = now.strftime("%I:%M %p")
                current_date_str = now.strftime("%A, %B %d")
                speak(f"The time is {current_time_str}. Today is {current_date_str}.")
                last_action_time = current_time

            elif gesture_name == "Call Me":
                print("Action: Call Me (Opening WhatsApp)")
                speak("Opening WhatsApp for you.")
                webbrowser.open("https://web.whatsapp.com")
                last_action_time = current_time

            
            elif gesture_name == "Fist":
                print("Action: Fist (Cancel)")
                speak("Action cancelled.")
                last_action_time = current_time

        

        cv2.putText(frame, f"Gesture: {gesture_name}", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) # <--- ADD THIS BLOCK

        cv2.imshow('Gesture Control', frame)       

        if cv2.waitKey(5) & 0xFF == ord("q"):
            break
    
    cap.release()
    cv2.destroyAllWindows()

