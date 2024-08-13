from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from flask_wtf import FlaskForm
from openai import OpenAI
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import speech_recognition as sr
import os
from torch import autocast
from diffusers import StableDiffusionPipeline
import torch

organization = 'org-EvWopVgEuGbYlCBGz0bbJDoF'
open_api_key = "sk-zv0P4MDjgo3TkMWiv8nNmzMPyx8vEzljanmQha0XBpT3BlbkFJJFDDEtkGfYOsenvvhaD546uXh2_2l710_CeLtvidQA"

client = OpenAI(
    api_key=open_api_key
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['GENERATED_FOLDER'] = 'static/generated'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac'}

r = sr.Recognizer()


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Generate Image")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def audio_to_text(audio_path):
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        output_text = r.recognize_google(audio)
    except sr.UnknownValueError:
        output_text = "Speech recognition could not understand the audio"
    except sr.RequestError:
        output_text = "Could not request results from the speech recognition service"
    return output_text


def text_to_image(text):
    response = client.images.generate(
        model="dall-e-2",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    return image_url


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            text = audio_to_text(path)
            image_path = text_to_image(text)
            return redirect(url_for('generated_image', filename=os.path.basename(image_path)))
        else:
            flash('Invalid file type. Please upload an audio file.')
            return redirect(request.url)
    return render_template('audio2image.html', form=form)


@app.route('/generated/<filename>')
def generated_image(filename):
    return send_from_directory(app.config['GENERATED_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
