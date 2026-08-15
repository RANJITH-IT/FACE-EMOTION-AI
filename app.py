from flask import Flask, render_template, jsonify
import pyttsx3
import random
from test import detect_emotion_from_frame

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    try:
        emotion = detect_emotion_from_frame()
        if "Error" in emotion or "No face" in emotion:
            return jsonify({'emotion': emotion, 'message': emotion})

        suggestions = {
            'Angry': [
                "Take a deep breath. Inhale... Exhale...",
                "Try to step away and calm yourself.",
                "Listening to calming music can help.",
                "Count to ten and let your anger fade.",
                "Focus on something that makes you smile."
            ],
            'Disgust': [
                "Try thinking about something positive.",
                "A quick walk might change your perspective.",
                "Focus on things you enjoy instead.",
                "Take a moment to center yourself.",
                "Shift your thoughts to a happy memory."
            ],
            'Fear': [
                "You're strong and can face this fear!",
                "Take slow, calming breaths.",
                "Fear is just an emotion; you are in control.",
                "Distract yourself with something comforting.",
                "Talk to someone you trust about your fears."
            ],
            'Happy': [
                "You look great when you smile! 😊",
                "Happiness suits you perfectly!",
                "Keep spreading those positive vibes!",
                "Enjoy the little things that make you smile.",
                "Cherish this moment of happiness."
            ],
            'Neutral': [
                "How about trying a fun activity?",
                "Feeling neutral? Maybe a quick stretch can help.",
                "Take a small break and enjoy some fresh air.",
                "Listen to your favorite song for a mood boost.",
                "Sometimes being neutral is peaceful too."
            ],
            'Sad': [
                "It's okay to feel sad; you're not alone.",
                "Would you like to hear a joke to cheer you up?",
                "Talking to a friend can make you feel better.",
                "Try focusing on things that make you happy.",
                "Sadness is temporary. Better days are ahead!"
            ],
            'Surprise': [
                "That was unexpected! Hope it's a good surprise.",
                "Surprises make life exciting, don't they?",
                "Take a moment to process the surprise.",
                "Life is full of surprises; embrace them!",
                "Surprised? Share it with someone you trust!"
            ]
        }

        if emotion in suggestions:
            message = random.choice(suggestions[emotion])
        else:
            message = "Emotion not recognized. Try again!"

        # Convert message to speech
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(message)
        engine.runAndWait()

        return jsonify({'emotion': emotion, 'message': message})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/tell_joke', methods=['GET'])
def tell_joke():
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don’t oysters donate to charity? Because they’re shellfish.",
        "I asked the librarian if the library had any books on suicide. She said they were all due back tomorrow."
    ]
    return jsonify({'joke': random.choice(jokes)})

if __name__ == '__main__':
    app.run(debug=True)
