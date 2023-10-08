import os
import cv2

directory = './data/sorted/'
for folder in os.listdir(directory):
    # Skip the git ignore file
    if (folder == '.gitignore'): continue

    for filename in os.listdir(directory+folder):
        f = os.path.join(directory+folder, filename)

        # checking if it is a file
        if os.path.isfile(f):
            image = cv2.imread(f)
            image = cv2.resize(image, (24,24), interpolation = cv2.INTER_AREA)
            cv2.imwrite(f, image)
        
cv2.destroyAllWindows()