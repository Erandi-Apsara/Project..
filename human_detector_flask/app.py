from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
import subprocess
import shutil

app = Flask(__name__)

# === Config ===
YOLO_PATH = "/Users/pawandinendra/Desktop/model/human/yolov5"
WEIGHTS = os.path.join(YOLO_PATH, "runs/train/human_yolov53/weights/best.pt")
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
DETECT_NAME = "flask_detect"

# === Create folders if not exist ===
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# === Home Page: Upload Image ===
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file.filename != "":
            filename = f"{uuid.uuid4().hex}.jpg"
            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(upload_path)

            # === Run YOLOv5 detection ===
            subprocess.run([
                "python3", os.path.join(YOLO_PATH, "detect.py"),
                "--weights", WEIGHTS,
                "--img", "640",
                "--conf-thres", "0.01",
                "--source", upload_path,
                "--save-conf",
                "--save-txt",
                "--project", os.path.join(YOLO_PATH, "runs/detect"),
                "--name", DETECT_NAME,
                "--exist-ok"
            ], stdout=subprocess.DEVNULL)

            # === Copy detected image to results folder ===
            result_img = os.path.join(YOLO_PATH, "runs/detect", DETECT_NAME, filename)
            output_img = os.path.join(RESULT_FOLDER, filename)
            shutil.copy(result_img, output_img)

            return redirect(url_for("result", filename=filename))

    return render_template("index.html")


# === Result Page: Show image + detection table ===
@app.route("/result/<filename>")
def result(filename):
    label_path = os.path.join(YOLO_PATH, "runs/detect", DETECT_NAME, "labels", filename.replace(".jpg", ".txt"))
    detections = []

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 6:
                    # Convert strings to readable values
                    class_id = parts[0]
                    xc, yc, w, h, conf = map(lambda x: round(float(x), 3), parts[1:])
                    detections.append([class_id, xc, yc, w, h, conf])

    return render_template("result.html", filename=filename, detections=detections)


# === Run Flask App ===
if __name__ == "__main__":
    app.run(debug=True)
