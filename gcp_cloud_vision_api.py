import json
import argparse

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw


def check_face_loc(left_eye,right_eye,nose_tip):
    print(nose_tip.x)
    if(nose_tip.x < 3280*1/3):
        print("もうちょい右やで")    
        return -1
    if(nose_tip.x > 3280*2/3):
        print("もうちょい左やで")
        return -2   
    if(nose_tip.y < 2464*1/3):
        print("もうちょい下")
        return -3        
    if(nose_tip.y > 2464*2/3):
        print("もうちょい上")
        return -4
    return 0

def detect_face(face_file, max_results=4):
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = types.Image(content=content)
    return client.face_detection(image=image).face_annotations


def highlight_faces(image, faces):
    for face in faces:
        left_eye =  face.landmarks[0].position
        right_eye = face.landmarks[1].position
        nose_tip =  face.landmarks[7].position 
        #print(faces)
        #print(face.landmarks[0].position)#左目
        #print(face.landmarks[1].position)#右目
    #print(left_eye)
    #print(right_eye)
    #print(nose_tip)
    return check_face_loc(left_eye,right_eye,nose_tip)

def main(input_filename,max_results):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        image.seek(0)
        return highlight_faces(image, faces)


if __name__ == '__main__':
    check_face_loc_result = main("img/test.JPG",4)
    print(check_face_loc_result)