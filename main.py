import os
import face_data.face_login as face_login
import assistant.voice_assistant as voice_assistant
import gestures.gesture_controller as gesture_controller

def main():
    print("--- Welcome to your Secure Personal AI Assistant ---")
    voice_assistant.speak("Welcome to your Secure Personal AI Assistant")
    face_data_dir= "face_data"
    encoding_file = os.path.join(face_data_dir, "known_face.npy")

    if not os.path.exists(encoding_file):
        print("\nNo registered user found. Starting one-time face registration.")
        if face_login.capture_and_encode_face(encoding_file):
            print("Face registered successfully!")
            voice_assistant.speak("Face registered successfully")
        else:
            print("Failed to register face. Please restart the application.")
            voice_assistant.speak("Failed to register face. Please restart the application.")
            return 
    
    print("\nPlease verify your identity to continue.")
    if not face_login.verify_face(encoding_file):
        print("Unauthorized User. Exiting program.")
        voice_assistant.speak("Unauthorized User. Exiting program.")
        return
    
    print("\nFace verification successful. Access Granted!")

    try:
        voice_assistant.speak("Access Granted. Welcome back.")
    
    except Exception as e:
        print(f"Initial greeting failed, but continuing: {e}")
    
    while True:
        print("\n----------------------------------")
        
        voice_assistant.speak("Say 'One for Voice Commands', 'Two for Gesture Control', or 'Exit'")
        print("----------------------------------")
        
        # We now use our listen() function instead of input()
        choice_command = voice_assistant.listen()

        if 'one' in choice_command:
            voice_assistant.run_voice_assistant()
        elif 'two' in choice_command:
            gesture_controller.run_gesture_controller()
        elif 'exit' in choice_command or 'stop' in choice_command:
            print("Thank you for using the AI Assistant. Goodbye!")
            try:
                voice_assistant.speak("Goodbye!")
            except:
                pass
            break
        elif choice_command: # This handles cases where it heard something, but it wasn't a valid command
             print(f"Invalid command: '{choice_command}'. Please try again.")
             voice_assistant.speak("That is not a valid choice. Please say voice commands, gesture control, or exit.")

if __name__ == "__main__":
    main()