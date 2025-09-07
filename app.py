import os
import google.generativeai as genai
from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
from werkzeug.utils import secure_filename

# Configure Gemini API
genai.configure(api_key="AIzaSyA_cVwS9XqomAfh0jFJ2Kk1MBByGCOvPwY")

app = Flask(__name__)

# Folder to save uploaded images
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return redirect(request.url)

    file = request.files["image"]

    if file.filename == "" or not allowed_file(file.filename):
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Open image with PIL
    image = Image.open(file_path)

    # Load Gemini model
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Generate description
    response = model.generate_content([image, "Describe this image."])
    description = response.text

    return render_template("index.html", image_path=file_path, description=description)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)