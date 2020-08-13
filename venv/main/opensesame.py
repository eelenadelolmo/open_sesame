import os
os.chdir("/home/elena/PycharmProjects/open_sesame/open-sesame")

from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, send_file, render_template, url_for

UPLOAD_FOLDER = '/home/elena/PycharmProjects/open_sesame/open-sesame'
DOWNLOAD_FOLDER = '/home/elena/PycharmProjects/open_sesame/open-sesame/logs/pretrained_again_argid/'
file_original_name = ''

ALLOWED_EXTENSIONS = {'txt'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(response):
  response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
  if ('Cache-Control' not in response.headers):
    response.headers['Cache-Control'] = 'public, max-age=600'
  return response

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.stream.seek(0)
            os.system("python sesame/targetid.py --mode predict --model_name pretrained_again_targetid --raw_input " + filename)
            os.system("python sesame/frameid.py --mode predict --model_name pretrained_again_frameid --raw_input logs/pretrained_again_targetid/predicted-targets.conll")
            os.system("python sesame/argid.py --mode predict --model_name pretrained_again_argid --raw_input logs/pretrained_again_frameid/predicted-frames.conll")
            return redirect(url_for('download_file', filename='predicted-args.conll'))

    return render_template('main.html')


# http://0.0.0.0:5000/downloadfile/predicted-args.conll

@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = DOWNLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='', cache_timeout=0)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")
