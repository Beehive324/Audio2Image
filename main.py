from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import speech_recognition as sr
import pyttsx3
import os
from torch import autocast
from diffusers import StableDiffusionPipeline

from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

r = sr.Recognizer()


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Generate Image")


def audio_to_text(audio_path):
    output_text = r.recognize_google_cloud(audio_path)
    return output_text


def text_to_image(text):
    pipe = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        use_auth_token=True
    ).to("cuda")

    with autocast("cuda"):
        image = pipe(text)["sample"][0]
    image.save(f"{text.split()[:10]}")

    return image


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', "POST"])
def home():
    """
    add exception if file type is not like an audio file endswith, mp3, wav etc..
       create render template here etc..
       :return:

       audio = upload_audio()
       text = audio_to_text(audio)
       image = text_to_image(text)
   """
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                            secure_filename(file.filename))
        file.save(path)
        text = audio_to_text(path)
        image = text_to_image(text)

        return image
    return render_template('audio2image.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
