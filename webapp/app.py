#upload files from the testing_file folder

from flask import Flask, request, jsonify, flash, redirect, url_for, send_from_directory, render_template
from model_files.model import Model, loadDataset,predict_genre
from werkzeug.utils import secure_filename
import pickle
import os


Upload_folder = '/Users/PRAKHAR/Desktop/work/Major Project/music genre detector/webapp/Upload_GenreFiles'

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = Upload_folder


#returns bin file of the model we have saved
def return_model():
    with open("model_files/model.bin","rb") as f_in:
        model = pickle.load(f_in)
    return model


@app.route('/')
def index():
    return render_template('upload_page.html')

@app.route('/Music_Genre', methods=['GET','POST'])
def Music_Genre():
    if request.method == 'POST':
        
        file = request.files['file']
        
        # secure the file
        filename = secure_filename(file.filename)

        #save the upload file to upload_files folder
        file.save(os.path.join(Upload_folder, filename))

        #load datset for model
        dataset = loadDataset("model_files/my.dat",0.66)

        #Return model
        model = return_model()

        #resullt of prediction made
        result = predict_genre(f"Upload_GenreFiles/{filename}",dataset,model)

        return render_template("Music_Genre.html", result=result)
    return render_template("Music_Genre.html")


if __name__ == "__main__":
    app.run(debug=True)

