from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    name = os.environ.get("GREETING_TARGET", "World")
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)