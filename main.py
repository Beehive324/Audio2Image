from flask import Flask, render_template, request
from pydub import ____

app = Flask(__name__)


def upload_audio(file_upload):
    """
    1.Search how to upload an audio file in Python
    """
    pass


def audio_to_text(audio):
    """
    1.Convert audio to text using an API, watch a youtube video on this
    :param audio:
    :return:
    """

def text_to_image(text):
    """
    Use AI to Convert the text into image
    :param text:
    :return:
    """
    pass


@app.route('/', methods=['Get', 'POST'])
def run():
    """
    create render template here etc..
    :return:
    """
    audio = upload_audio()
    text = audio_to_text(audio)
    image = text_to_image(text)

    return render_template('audio2image.html')

if __name__ == "__main__":
    app.run(debug=True)
