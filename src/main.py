from flask import Flask
from flask import request
from threading import Thread
import gemini

app = Flask('')

# Global variable to store chat history (for simplicity)
chat_history = []


@app.route('/')
def home():
    return "Welcome to the chat server!"


@app.route('/chat', methods=['POST'])
def handle_chat():
    if request.form.get('message') is None:
        return 'Invalid request: '+str(request.form)
    user_message = request.form['message']
    chat_history.append(f"User: {user_message}")
    response = ""
    try:
        gemini.convo.send_message(user_message)
        response = gemini.convo.last.text
    except Exception as e:
        response = str(e)
    chat_history.append(response)

    return response


def run():
    app.run(host='0.0.0.0', port=80)


def keep_alive():
    t = Thread(target=run)
    t.start()


if __name__ == '__main__':
    keep_alive()
