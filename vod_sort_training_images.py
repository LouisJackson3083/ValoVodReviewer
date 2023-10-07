import os
import cv2

directory = './data/unsorted/'
for filename in os.listdir(directory):
    # Skip the git ignore file
    if (filename == '.gitignore'): continue
    f = os.path.join(directory, filename)

    # checking if it is a file
    if os.path.isfile(f):
        image = cv2.imread(f)
        
        image_big = cv2.resize(image, (image.shape[1]*3, image.shape[0]*3), interpolation=cv2.INTER_LINEAR)
        cv2.imshow('image', image_big)
        key_press = cv2.waitKey(0)
        cv2.destroyWindow('image')

        # r = Raze
        # o = Omen
        # s = Skye
        # k = Killjoy
        # b = Breach
        # 

        identified_feature = None

        if (key_press == 27): # If we press escape, get out
            break
        elif (key_press == 32):
            identified_feature = 'spike'
        elif (key_press == ord('r')):
            identified_feature = 'raze'
        elif (key_press == ord('o')):
            identified_feature = 'omen'
        elif (key_press == ord('s')):
            identified_feature = 'skye'
        elif (key_press == ord('k')):
            identified_feature = 'killjoy'
        elif (key_press == ord('b')):
            identified_feature = 'breach'
        else:
            continue
        
        newpath = './data/sorted/'+str(identified_feature)+'/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        output_filename = newpath+str(hash(filename))+'.png'
        os.remove(f)
        cv2.imwrite(output_filename, image)
cv2.destroyAllWindows()