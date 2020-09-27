from flask import Flask, render_template, request, redirect, url_for,abort, send_from_directory
from werkzeug.utils import secure_filename # helps to convert bad filename into a secure filename
import os 

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 2 # 2MB
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('upload.html',upfiles=files)


@app.route('/',methods=['POST'])
def upload_file(): 
    uploaded_file = request.files.get('file')                       # we are getting file from FORM
    filename = secure_filename(uploaded_file.filename)              # clean the filename n store it in variable
    if filename != '':                                              # if the filename is not empty then
        file_ext = os.path.splitext(filename)[1]                    # get the extension from filename abc.png ['abc','.png']
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:         # if extension is not valid
            abort(400)                                              # then stop execution else
        path = os.path.join(app.config['UPLOAD_PATH'],filename)     # make os compatible path string
        uploaded_file.save(path)                                    # then save the file with original name 
    return redirect(url_for('index'))                               # reload the page to refresh


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'],filename)

@app.errorhandler(413)
def too_large(e):
    return render_template('error_too_big.html')

if __name__ == '__main__':
    app.run(debug=True)