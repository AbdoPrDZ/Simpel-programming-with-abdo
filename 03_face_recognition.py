''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import cv2
import numpy as np
import os 

if not os.path.exists("trainer/trainer.yml"):
    print("""[Error]: You cannot run this project because you do not have a file "trainer / trainer.yml"\n          or you are not running this project in the correct path\n → If you want to get "trainer / trainer.yml", please run "01_face_dataset.py"\n   for facial images, or "02_face_training.py" to create a "trainer / trainer.yml"\n   file for faces if you have face images""")
    input("press any key on keyboard to exit...")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = []
if os.path.exists(r"trainer\Characters_Names.cn"):
    cns = open(r"trainer\Characters_Names.cn", "r").read().split('\n')
    del(cns[-1])
    for cn in cns:
        names.append(cn.split('===')[2])

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
# cam = cv2.VideoCapture("Now You See Me 2.wmv")
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
cam.set(1, 2300)

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img = cam.read();

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (100-confidence > 40):
            try:
                id = names[id]
            except:
                id = "Face<{}>".format(id)
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "New Face"
            confidence = " 0%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
