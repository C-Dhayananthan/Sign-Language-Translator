import asyncio
import websockets
import base64
import os
import cv2
import numpy as np
import pandas as pd
import numpy  as np
from flask import Flask, render_template, request
import json
import VideoLocate
import PreprocessText
import ModelFinal
import os
from flask_socketio import SocketIO, emit
from flask import Flask, render_template
from flask_sockets import Sockets
models  = ModelFinal.SignModel()
txt = PreprocessText.text_preprocess()
app = Flask(__name__, template_folder=r"./template")       
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

            

@app.route("/")
def home(): 
    return render_template(r"index.html")
@app.route("/sign_to_text")
def sign_to_text ():
    return render_template("page1.html")
@app.route("/text_to_sign")
def text_to_sign():
    return render_template("test2.html")




def base64_to_image(base64_charactering):
    # Extract the base64 encoded binary data from the input charactering
    base64_data = base64_charactering.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


#sign to text
@socketio.on("connect")
def test_connect():
    print("__________________Sign to text is Connected___________________")
    emit("my response", {"data": "Connected"})

@socketio.on("image")
def receive_image(image):
    # Decode the base64-encoded image data
    if image:
        image = base64_to_image(image)
        
        #plt.imshow(image)
        #plt.show()

        try:
            hds = ModelFinal.HandDetect(image)
            input,keypo = hds.detector()
    
            char = models.predict(input,keypo )
            char
            print("_______Predicted________: ", char)
            txt.sentence_preocess(char)
            
           
            socketio.emit("word_reponse",{"data":char})
            socketio.emit("test_response",{"data":txt.character})

        except Exception as e:

            print("Hand is NOt detected",e)

@socketio.on("clear_sentence")
def clear_sentence(data):
    #print("_______________Sentence Clear___________     ")
    print("--------------------------------",data['message'])
    txt.cleared()
    socketio.emit("test_response",{"data":txt.character})
#text to sign
@socketio.on('send_data')
def handle_data(data):
    print("__________tester________",data)
    sentence = data["data"]
    path_instance = VideoLocate.VideoPath(sentence)
    
    #path_dict = path_instance.path()
    
    pre_sentence = path_instance.pre_text.upper()

    #tokens = list(path_dict.keys()) 

    #paths = list(path_dict.values())

    path_lst2,path,condition=  path_instance.path()
    act_tokens = path_instance.tokens2
    #tokens = path_instance

    print("_____paths______",path_lst2)
    print("_____Tokens_____", act_tokens)


    #tok_dic = {"tokens":tokens}
    #path_dic = {"dict":paths}
    #json_token = json.dumps(act_tokens)
    #json_path = json.dumps(paths)

    json_token = json.dumps(act_tokens)
    json_path = json.dumps(path_lst2)

    glooss = np.array(path.keys())
    condition = np.array(condition)
    
    if "IndexError" in path_lst2:
        #print("_____paths______",paths)
        socketio.emit("NotVideoLoad" , {"message":"Some Gloss videos are not found","pre_sentence":pre_sentence,"token":json_token,
        "path":json.dumps([])
        })
    elif True in condition:
        socketio.emit("FingerSpelling",{"message":"Finger Spelling is show for not words","pre_sentence":pre_sentence,"token":json_token,"path":json_path})
    
    else:
            
        socketio.emit("VideoLoaded",{"message":'VideosFound',"pre_sentence":pre_sentence,"token":json_token,"path":json_path})


if __name__ == "__main__":
    socketio.run(app, debug=False,port = 600,host = '0.0.0.0')
