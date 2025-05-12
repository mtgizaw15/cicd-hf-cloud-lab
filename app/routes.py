import os
import json
from flask import Blueprint, render_template, request, redirect, url_for
from app.detector import detect_faces
from app.send_email import send_email

main = Blueprint('main', __name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')

@main.route('/', methods=['GET', 'POST'])
def index():
    metadata_file = os.path.join('static', 'uploads', 'descriptions.json')

    if request.method == 'POST':
        file = request.files['image']
        description = request.form.get('description')

        if file:
            abs_upload_folder = os.path.join(os.getcwd(), UPLOAD_FOLDER)
            if not os.path.exists(abs_upload_folder):
                os.makedirs(abs_upload_folder)

            filename = file.filename
            filepath = os.path.join(abs_upload_folder, filename)
            file.save(filepath)

            detected_count = detect_faces(filepath, filepath)

            subs_file = os.path.join('static', 'uploads', 'subscribers.json')
            if os.path.exists(subs_file):
                with open(subs_file, 'r') as f:
                    subscribers = json.load(f)

                subject = "Új kép került feltöltésre!"
                body = f"Kép neve: {filename}\nLeírás: {description}\nDetektált arcok száma: {detected_count}"
                send_email(subscribers, subject, body)

            metadata = {}
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

            metadata[filename] = description
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            return redirect(url_for('main.index'))

    images = []
    descriptions = {}
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            descriptions = json.load(f)
    
    if os.path.exists(UPLOAD_FOLDER):
        for fname in os.listdir(UPLOAD_FOLDER):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                desc = descriptions.get(fname, "(nincs leírás)")
                images.append((fname, desc))

    return render_template('index.html', images=images)

@main.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if not email:
        return redirect(url_for('main.index'))

    subs_file = os.path.join('static', 'uploads', 'subscribers.json')
    subscribers = []

    upload_dir = os.path.dirname(subs_file)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    if os.path.exists(subs_file):
        with open(subs_file, 'r') as f:
            subscribers = json.load(f)

    if email not in subscribers:
        subscribers.append(email)

    with open(subs_file, 'w') as f:
        json.dump(subscribers, f, indent=2)

    return redirect(url_for('main.index'))