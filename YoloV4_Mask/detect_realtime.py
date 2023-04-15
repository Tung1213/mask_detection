import cv2
import numpy as np
import socket
import time
import threading


starting_time= time.time()
frame_id = 0

host='127.0.0.1'
port=1213


y_m='0'
n_m='0'
u_m='0'
t_m='0'

count=0
# Load Yolo
weightsPath = r'./yolov4_data/yolov4-tiny-obj_final.weights'#模型权重文件
configPath = r'./yolov4_data/yolov4-tiny-obj.cfg'#模型配置文件
labelsPath = r'./yolov4_data/coco.names'#模型类别标签文件
net = cv2.dnn.readNet(weightsPath, configPath)
classes = []
with open(labelsPath , "r") as f:
    classes = [line.strip() for line in f.readlines()]
#print(len(classes))
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


# Loading image
#img = cv2.imread("src_room.jpg")
def client():
     
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    while True:

        outdata=t_m
        print('send:'+outdata)
        s.send(outdata.encode())

        indata=s.recv(1024)
        if len(indata)==0:
            s.close()
            print('server closed connection.')
            break
        print('recv :'+indata.decode())

cap=cv2.VideoCapture(0)

while(True):

    ret,img=cap.read()
    frame_id+=1
    img = cv2.resize(img, None, fx=0.8, fy=0.7)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN

    for i in range(len(boxes)):
        
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
         
            if label=="Yes":

                y_m=str(i)

            elif label=="No":
                n_m=str(i)

            elif label=="Un":

                u_m=str(i)
            #print()
            t_m=y_m+","+n_m+","+u_m
            
            #color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 1)
            cv2.putText(img, label, (x, y + 30), font, 1,  (255,0,0), 2)
    server_t=threading.Thread(target=client)
    server_t.start()
    elapsed_time = time.time() - starting_time
    fps=frame_id/elapsed_time
    print("fps",fps)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        
        break

cap.release()
cv2.destroyAllWindows()
