# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:07:04 2020

@author: MAHE
"""
from mtcnn.mtcnn import MTCNN
import math
import numpy as np
import copy
import cv2
# defining face detector
detector= MTCNN()
ds_factor=0.6
class Camera1(object):
    
    #some observations made by manually running some experiment on my laptop webcam
    #all the dimensions are in inch
    #actual width of the object
    WIDTH = 57
    # Perpendicular distance from the camera
    DISTANCE = 38
    #pixels covered by the object in the image
    PIXELS = 480
    # focus of the camera
    # this value will be used in future calculations
    FOCUS = PIXELS * DISTANCE / WIDTH
    Face = (9,8)
    def __init__(self):
        
        #capturing video
        self.cap=cv2.VideoCapture(0)
        self.faces = []
        self.warning=[]
    
    def __del__(self):
        #releasing camera
        self.cap.release()
    def get_frame(self):
        #extracting frames
        status,photo=self.cap.read()
        photo=cv2.resize(photo,(640,480))
        result=detector.detect_faces(photo)
        face_cor=[]
        for a in range(len(result)):
            face_cor.append(result[a]['box'])
    #     face_cor=face_model.detectMultiScale(photo)
        self.faces=[]
        if len(face_cor)==0:
            pass
        else:
            for x in range(0,len(face_cor)):
                x1=face_cor[x][0]
                y1=face_cor[x][1]
                x2=x1+face_cor[x][2]
                y2=y1+face_cor[x][3]
                photo=cv2.rectangle(photo,(x1,y1),(x2,y2),[0,255,0])
            for face in face_cor:
                y = round((self.Face[0]*self.FOCUS/(face[2])),5)
                if face[0]   < 240:
                    P = 480 - 2*(face[0] )
                    P_ = y * P /38
                    x = round((P_ * y / (self.FOCUS * 2)),5)
                    x = -x
                elif face[0]   > 240:
                    P = 2*(face[0] ) - 480
                    P_ = y * P /38
                    x = round((P_ *y / (self.FOCUS * 2)),5)
                else:
                    x = 0
                self.faces.append((x,y))
            
            self.warning = []
            for face in self.faces:
                self.warning.append([])
            if len(self.faces)>1:
                y0, dy = 50, 20

                for a in range(len(self.faces)):
                    for b in range(a + 1,len(self.faces)):
                        dist = (self.faces[a][0] - self.faces[b][0])**2 + ( self.faces[a][1] - self.faces[b][1])**2
                        dist = round(math.sqrt(dist),5)
                        if dist < 500:
                            self.warning[a].append(b)
                            self.warning[b].append(a)
                            dist_str="distance is "+str(dist)
                            #y1 = y0 + i*dy
                            #y1 = int(y1)
                            cv2.putText(photo,dist_str,(100,50),cv2.FONT_HERSHEY_SIMPLEX,1,[0,0,255],2)
    #                             
            
            if len(self.warning)>0:
                for war in range(len(self.warning)):
                    if len(self.warning[war])>0:
                        if war <0:
                            pass
                        else:
                            x1=face_cor[war][0]
                            y1=face_cor[war][1]
                            x2=x1+face_cor[war][2]
                            y2=y1+face_cor[war][3]
                            photo=cv2.rectangle(photo,(x1,y1),(x2,y2),[0,0,255])
            str1 = ''
            n = 0
            if len(self.warning)>0:
                for war in range(len(self.warning)):
        #             n = n+1
                    str1 += '\n'
                    str1 += 'Person '
                    war3 = str(n)
                    str1 += war3
                    str1 += ' near to : '
                    for war2 in self.warning[war]:
                        str1 += str(war2)
                        str1 += ' , '
                    n = n+1
            y0, dy = 50, 20
            for i, line in enumerate(str1.split('\n')):
                y1 = y0 + i*dy
                y1 = int(y1)
                cv2.putText(photo, line , (0,y1) ,cv2.FONT_HERSHEY_SIMPLEX,0.5,[0,0,255],2)
        #         cv2.putText(photo, str1 , (50,200) ,cv2.FONT_HERSHEY_SIMPLEX,1,[0,0,255],3)
        photo=cv2.resize(photo,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)                    
        gray=cv2.cvtColor(photo,cv2.COLOR_BGR2GRAY)     
       # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', photo)
        return jpeg.tobytes()
