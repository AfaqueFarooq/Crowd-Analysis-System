from flask import Flask, Response
from functions.counting_people import computePeople
app = Flask(__name__)

if __name__ == "__main__":
    app.run(threaded=True, port=80, debug="true", use_reloader=False)