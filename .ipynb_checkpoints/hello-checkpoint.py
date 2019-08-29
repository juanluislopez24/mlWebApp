from flask import Flask
import keras.models import load_model

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'