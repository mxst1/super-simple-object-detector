from flask import Flask, send_from_directory, request, redirect, url_for
from detector import detectObjects
from threading import Thread
from time import sleep
import cv2
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return send_from_directory("./src", "index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return "No file detected", 400
    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400
    
    file.save(f"src/images/image.jpg")

    detected = detectObjects(os.path.join("src", "images", "image.jpg"))

    cv2.imwrite("src/images/detected.jpg", detected)

    delete_image_later("src/images/detected.jpg")
    delete_image_later("src/images/image.jpg")

    return redirect("/")

@app.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory("src/images", filename)

def delete_image_later(path, delay=5):
    def delete_image():
        sleep(delay)
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted {path}")
    Thread(target=delete_image).start()


if __name__ == '__main__':
    app.run(debug=True)
