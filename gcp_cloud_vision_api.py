import json
import argparse

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw


#TODO face_boxを連想配列にする
def check_face_loc(face_box,left_eye,right_eye,nose_tip):
    if((face_box[0][0]-face_box[1][0])*(face_box[1][1]-face_box[2][1]) < 200 * 200):#ここ調整
        print("もう少し近づいて")
        return "forward"
    if(face_box[0][0] > 1024*1/2):
        return "right" #被写体は右に
    if(face_box[1][0] < 1024*1/2):
        return "left" #被写体は左に
    if(face_box[0][1] > 768*1/2):
        return "forward" #顔はもう少し上に
    if(face_box[3][1] < 768*1/2):
        return "back" #顔はもう少し下に
    
    # print(nose_tip.x)
    # if(nose_tip.x < 1024*4/7):
    #     print("もうちょい右やで")    
    #     return "move right"
    # if(nose_tip.x > 1024*4/7):
    #     print("もうちょい左やで")
    #     return "move left"
    # if(nose_tip.y < 768*4/7):
    #     print("もうちょい下(後ろに下がって)")
    #     return "get back"
    # if(nose_tip.y > 768*4/7):
    #     print("もうちょい上(前に出て)")
    #     return "move forward"
    return "ok"

def detect_face(face_file):
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = types.Image(content=content)
    return client.face_detection(image=image).face_annotations


def highlight_faces(image, faces):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    
    for face in faces:
        left_eye =  face.landmarks[0].position
        right_eye = face.landmarks[1].position
        nose_tip =  face.landmarks[7].position

        box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]#(左上、右上、右下、左下)
        draw.line(box + [box[0]], width=5, fill='#00ff00')
    print(box)
    im.save("./output.jpg")
    return check_face_loc(box,left_eye,right_eye,nose_tip)

def main(input_filename):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image)
        if not faces:
            print("顔を認識できません")
            return "nobody"
        image.seek(0)
        return highlight_faces(image, faces)

if __name__ == '__main__':
    check_face_loc_result = main("img/tes.JPG")
    print(check_face_loc_result)
