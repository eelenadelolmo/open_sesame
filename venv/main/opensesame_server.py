# -*- coding: utf-8 -*-

import os
import subprocess
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template, url_for
import shutil


def make_archive(source, destination):
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s' % (name, format), destination)


UPLOAD_FOLDER = 'in/'
DOWNLOAD_FOLDER = 'logs/pretrained_again_argid/out'

shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
shutil.rmtree(DOWNLOAD_FOLDER + '/', ignore_errors=True)
shutil.rmtree('logs/pretrained_again_targetid/out', ignore_errors=True)
shutil.rmtree('logs/pretrained_again_frameid/out', ignore_errors=True)
os.makedirs(UPLOAD_FOLDER)
os.makedirs(DOWNLOAD_FOLDER + '/')
os.makedirs('logs/pretrained_again_targetid/out/')
os.makedirs('logs/pretrained_again_frameid/out/')

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


filename_original = ""


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':

        shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
        shutil.rmtree(DOWNLOAD_FOLDER + '/', ignore_errors=True)
        shutil.rmtree('logs/pretrained_again_targetid/out', ignore_errors=True)
        shutil.rmtree('logs/pretrained_again_frameid/out', ignore_errors=True)
        os.makedirs(UPLOAD_FOLDER)
        os.makedirs(DOWNLOAD_FOLDER + '/')
        os.makedirs('logs/pretrained_again_targetid/out/')
        os.makedirs('logs/pretrained_again_frameid/out/')

        # check if the post request has the file part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        # if user does not select file, browser also
        # submit an empty part without filename
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.stream.seek(0)

                # Deleting quotes in order to lower complexity
                """
                with io.open(UPLOAD_FOLDER + filename, 'r+') as f:
                    original = f.read()
                    new = re.sub('"', '', original)
                    f.seek(0)
                    f.truncate()
                    f.write(new)
                    f.close()
                """

        os.chdir("../../open-sesame")
        subprocess.Popen(
            "python -m sesame.targetid --mode predict --model_name pretrained_again_targetid --raw_input in",
            shell=True).wait()
        subprocess.Popen(
            "python -m sesame.frameid --mode predict --model_name pretrained_again_frameid --raw_input logs/pretrained_again_targetid/out",
            shell=True).wait()
        subprocess.Popen(
            "python -m sesame.argid --mode predict --model_name pretrained_again_argid --raw_input logs/pretrained_again_frameid/out",
            shell=True).wait()

        make_archive(DOWNLOAD_FOLDER, DOWNLOAD_FOLDER + '/en_framenet_annotated.zip')
        return redirect(url_for('download_file', filename='en_framenet_annotated.zip'))

    return render_template('main.html')


# http://0.0.0.0:5000/downloadfile/predicted-args.conll

@app.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)


@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = '../../open-sesame/' + DOWNLOAD_FOLDER + '/' + filename
    return send_file(file_path, as_attachment=True, attachment_filename=filename, cache_timeout=0)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5002")