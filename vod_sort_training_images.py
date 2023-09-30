import os
import cv2

directory = './training_images/unsorted/'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    print(f)
    # checking if it is a file
    if os.path.isfile(f):
        image = cv2.imread(f)
        
        image_big = cv2.resize(image, (image.shape[1]*3, image.shape[0]*3), interpolation=cv2.INTER_LINEAR)
        cv2.imshow('image', image_big)
        key_press = cv2.waitKey(0)
        cv2.destroyWindow('image')
        if key_press == ord('q'):
            break
        else:
            continue
cv2.destroyAllWindows()