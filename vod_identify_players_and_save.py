import cv2
import numpy as np
from tracker import *
import os
import glob

# Remove all unsorted training images
files = glob.glob('./training_images/unsorted/*')
for f in files:
    os.remove(f)

cap = cv2.VideoCapture('./vods/DRX vs FNATIC - VALORANT Champions - Knockout - Fracture Map 3_MASKED.mp4')

tracker = EuclideanDistTracker()

object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
    ret, frame = cap.read()
    if not ret: # if frame is read correctly ret is True
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    frame_info = frame

    # 1. Object detection
    mask = object_detector.apply(frame)
    # Processing on the mask
    _ , mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    erode_kernel = np.ones((3, 3), np.uint8)
    dilate_kernel = np.ones((5, 5), np.uint8)
    blur_amount = 5
    mask = cv2.erode(mask, erode_kernel)
    mask = cv2.dilate(mask, dilate_kernel)
    mask = cv2.blur(mask, (blur_amount, blur_amount))
    _ , mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if (area > 100):
            # cv2.drawContours(frame, [cnt], -1, (0,255,0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            if (w > 15 and w < 30 and h > 15 and h < 30):
                detections.append([x, y, w, h])

    # 2. Object tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id

        identified_player = frame[y:y+h, x:x+w]
        filename = './training_images/unsorted/'+str(box_id)+'.png'
        cv2.imwrite(filename, identified_player)
        cv2.putText(frame_info, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0 , 0), 2)
        cv2.rectangle(frame_info, (x,y), (x+w, y+h), (0, 255, 0), 3)


    cv2.imshow("Frame", frame_info)
    cv2.imshow("Mask", mask)
    
    if cv2.waitKey(2) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
