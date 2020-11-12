#upload files from the testing_file folder

from flask import Flask, request, jsonify, flash, redirect, url_for, send_from_directory, render_template
from model_files.model import Model, loadDataset,predict_genre
from werkzeug.utils import secure_filename
import pickle
import os

Upload_folder = '/Users/PRAKHAR/Desktop/work/Major Project/music genre detector/webapp/upload_files'
Allowed_extensions = "wav"


app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = Upload_folder

#Checks if the uploaded file is valid or not
def isAllowedFile(filename):
    a = "." in filename and filename.rsplit('.',1)[1].lower() == Allowed_extensions
    return a

#returns bin file of the model we have saved
def return_model():
    with open("model_files/model.bin","rb") as f_in:
        model = pickle.load(f_in)
    return model

@app.route('/', methods=['GET','POST'])
def upload_and_predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file Part')

        file = request.files['file']

        #if no file is selected
        if(file == ''):
            flash('No selected file')
            return redirect(request.url)

        if(file and isAllowedFile(file.filename)):
            # secure the file
            filename = secure_filename(file.filename)

            #save the upload file to upload_files folder
            file.save(os.path.join(Upload_folder, filename))

            #load datset for model
            dataset = loadDataset("model_files/my.dat",0.66)

            #Return model
            model = return_model()

            #resullt of prediction made
            result = predict_genre(f"upload_files/{filename}",dataset,model)

            return render_template("upload_file.html", result=result)
    return render_template("upload_file.html")

if __name__ == "__main__":
    app.run(debug=True)

