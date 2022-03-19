from flask import Flask , render_template,request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg' ,'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET'])
def index():
    for i in os.listdir(UPLOAD_FOLDER):
        os.remove(UPLOAD_FOLDER+'/'+i)
    return render_template('index.htm', title='crop leaf disease')

@app.route('/',methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash("no file part")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("no imiage selected for uploading")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        disease = 'nes'#predict(filename)
        return render_template('index.htm', filename=filename, disease=disease)
    else:
        flash("not allowed file")
        return redirect(request.url)

@app.route('/upload/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='upload/'+filename),code=301)

if __name__ == "__main__":
    app.run(debug = True)
