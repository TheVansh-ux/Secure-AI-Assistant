Secure Personal AI Assistant

This is a multi-modal AI assistant built in Python that uses face recognition for security, and can be controlled by both voice commands and hand gestures. This project was developed as a comprehensive exploration of computer vision and AI interaction techniques.

Features

Biometric Security: Uses the face_recognition library to ensure only an authorized user can activate the assistant.

Voice Control: A fully-featured voice assistant powered by Google's Text-to-Speech and Speech-to-Text engines.

Search Wikipedia

Open websites (Google, YouTube)

Play songs on YouTube

Tell the current time and date

Set reminders

Check the weather for any city

Gesture Control: A hands-free control system using MediaPipe to recognize hand gestures in real-time.

V-Sign (✌️): Opens YouTube

Palm (✋): Stops the current mode

Thumbs Up (👍): Gives a positive affirmation

One Finger (👆): Tells the current time and date

"Call Me" (🤙): Opens WhatsApp Web

How to Run

Clone the repository:

git clone [https://github.com/TheVansh-ux/Secure-AI-Assistant.git](https://github.com/TheVansh-ux/Secure-AI-Assistant.git)
cd Secure-AI-Assistant


Set up a virtual environment:

python -m venv venv
.\venv\Scripts\activate


Install dependencies:
(Note: dlib installation can be complex. It's recommended to install cmake first.)

pip install cmake dlib face_recognition opencv-python mediapipe SpeechRecognition gTTS playsound==1.2.2 pywhatkit wikipedia requests numpy


Run the application:

python main.py


On the first run, the application will guide you through a one-time face registration process.