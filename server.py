"""API for video processing"""
import os
import sys
from dotenv import load_dotenv

from flask import (Flask, abort,
                   request, jsonify)
from werkzeug.utils import secure_filename

from pyngrok import ngrok
import gofile
import recorded_video_image as rvi
sys.path.append("objectcounting")
from functionality.model import load_model
from functionality.utils import export_video
load_dotenv()
token = os.getenv("NGROK")

TARGET_VIDEO_PATH = "result.mp4"
model = load_model()
ngrok.set_auth_token(token)
public_url = ngrok.connect(5000).public_url
app = Flask(__name__)



def upload_on_go(path : str)-> str:
    """
    Upload file on go server.

    Parameters
    ----------
    path
    path to upload on server

    Return
    ------
    str
    Downloadable link
    """
    server = gofile.getServer()
    dict_data = gofile.uploadFile(path)
    return dict_data['downloadPage']


print("PUBLIC URL", public_url)
@app.route('/')
def upload_file():
    '''
    Test function 
    '''
    return 'Hello'

@app.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
    '''
    Save file in local and doinf processing

    Parameters
    ----------
    None

    Return
    ------
    None
    '''
    if request.method == 'POST': # check if the method is post
        if "video" in request.files:
            f = request.files['video'] # get the file from the files object
            path = f.filename
            f.save(secure_filename(f.filename)) # this will secure the file
            print("File save successfully")
            flag = rvi.flask_video(path)
            if flag=="0k":
                export_video()
                link = upload_on_go("output.mp4")
                return jsonify({'Download link': link ,
                                'status' : 'Ok'})
            else:
                return abort(400,jsonify({'Error': 'Type Error'}))

        elif "image" in request.files:
            f = request.files['image'] # get the file from the files object
            path = f.filename
            f.save(secure_filename(f.filename)) # this will secure the file
            print("File save successfully")
            rvi.image_processing(path)
            link = upload_on_go(f"content/ByteTrack/{TARGET_VIDEO_PATH}")
            return jsonify({'Download link': link ,
                            "type" : "JPG"})
        else:
            abort(400, msg = "Bad Params")

if __name__ == '__main__':
    app.run(port=5001) # running the flask app