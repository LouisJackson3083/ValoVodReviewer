import cv2
import numpy as np

# image_path = 'test.png'
# mask_path = './minimaps/split.png'

# image = cv2.imread(image_path)
# cv2.imshow("Original", image)
# cv2.waitKey(0)

# mask = cv2.imread(mask_path)
# mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
# h, w = mask.shape
# yoff = 0
# xoff = 0
# mask_final = np.zeros(image.shape[:2], dtype="uint8")
# mask_final[yoff:yoff+h, xoff:xoff+w] = mask
# cv2.imshow("binary mask", mask_final)
# cv2.waitKey(0)

# masked = cv2.bitwise_and(image, image, mask=mask_final)
# cv2.imshow("Mask Applied to Image", masked)
# cv2.waitKey(0)

def get_map(vod_path: str):
    """
    returns:
    split - split
    -1 - ?
    """
    if 'split' in vod_path.lower():
        return 'split'
    else:
        return -1

def get_mask(vod_map: str, mask_path: str, vod_shape: tuple):
    if (vod_map == 'split'):
        yscale = 0.88
        xscale = 0.88
        yoff = 0.095
        xoff = 0.09

    yoff = int(vod_shape[0]*yoff)
    xoff = int(vod_shape[1]*xoff)
    mask = cv2.imread(mask_path)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    new_shape = (int(vod_shape[0]*xscale), int(vod_shape[1]*yscale))
    mask = cv2.resize(mask, new_shape, interpolation= cv2.INTER_LINEAR)
    yoff_max = min(yoff+mask.shape[0], vod_shape[0])
    xoff_max = min(xoff+mask.shape[1], vod_shape[1])
    print(yoff_max,vod_shape[0])

    print(vod_shape)
    mask_final = np.zeros(vod_shape, dtype="uint8")
    mask_final[yoff:yoff_max, xoff:xoff_max] = mask[0:yoff_max-yoff, 0:xoff_max-xoff]
    return mask_final

def add_mask(vod_path: str, vod_map: str, out_path: str):
    # vod_map = get_map(vod_path=vod_path)
    mask_path = './minimaps/'+vod_map+'.png'

    vod = cv2.VideoCapture(vod_path)
    vod_shape = (int(vod.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(vod.get(cv2.CAP_PROP_FRAME_WIDTH)))
    vod_fps = vod.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(
        out_path,
        cv2.VideoWriter_fourcc(*'mp4v'), 
        vod_fps, 
        (vod_shape[1],vod_shape[0])
    )

    mask = get_mask(vod_map=vod_map, mask_path=mask_path, vod_shape=vod_shape)

    while vod.isOpened():
        ret, frame = vod.read()
        if not ret: # if frame is read correctly ret is True
            print("Can't receive frame (stream end?). Exiting ...")
            break

        frame = cv2.bitwise_and(frame, frame, mask=mask)
        out.write(frame)
        cv2.imshow("Mask Applied to Image", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    vod.release()
    out.release()
    cv2.destroyAllWindows()

def change_value(value):
    return value

def highlight_color(vod_path: str, team: str, out_path: str):
    windowName = 'vod'

    vod = cv2.VideoCapture(vod_path)
    vod_shape = (int(vod.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(vod.get(cv2.CAP_PROP_FRAME_WIDTH)))
    vod_fps = vod.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(
        out_path,
        cv2.VideoWriter_fourcc(*'mp4v'), 
        vod_fps, 
        (vod_shape[1],vod_shape[0])
    )

    while vod.isOpened():
        ret, frame = vod.read()
            
        if not ret: # if frame is read correctly ret is True
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        frame_blurred = cv2.blur(frame, (3, 3))
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(frame_hsv)
        s = s*2
        s = np.clip(s,0,255)
        frame_hsv = cv2.merge([h,s,v])

        lower_limit = np.array([0, 155, 155])
        upper_limit = np.array([360, 255, 255])
        
        frame_limited = cv2.inRange(frame_hsv, lower_limit, upper_limit)
        kernel = np.ones((3, 3), np.uint8)
        frame_limited = cv2.dilate(frame_limited, kernel)
        # frame_limited = cv2.erode(frame_limited, kernel)
        # frame_limited = cv2.cvtColor(frame_limited, cv2.COLOR_GRAY2BGR)
        # frame_limited = cv2.cvtColor(frame_limited, cv2.COLOR_BGR2GRAY)
        # mask = cv2.cvtColor(frame_limited, cv2.COLOR_HSV2BGR_FULL)


        # mask = cv2.bitwise_and(mask, mask, mask = mask_blurred)
        # result = cv2.bitwise_not(frame, frame, mask = mask)

        # (h, s, v) = cv2.split(mask)

        # detector = cv2.SimpleBlobDetector()
        # keypoints = detector.detect(frame_limited)
        # frame_with_keypoints = cv2.drawKeypoints(frame_limited, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        	
        out.write(frame_limited)
        cv2.imshow(windowName, frame_limited)

        if cv2.waitKey(1) == ord('q'):
            break

    vod.release()
    out.release()
    cv2.destroyAllWindows()

def combine_masks(vod_path_1: str, vod_path_2: str, out_path: str):
    vod_1 = cv2.VideoCapture(vod_path_1)
    vod_2 = cv2.VideoCapture(vod_path_2)
    vod_shape = (int(vod_1.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(vod_1.get(cv2.CAP_PROP_FRAME_WIDTH)))
    vod_fps = vod_1.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(
        out_path,
        cv2.VideoWriter_fourcc(*'mp4v'), 
        vod_fps, 
        (vod_shape[1],vod_shape[0])
    )

    while vod_1.isOpened():
        ret_1, frame_1 = vod_1.read()
        if not ret_1: # if frame is read correctly ret is True
            print("Can't receive frame (stream end?). Exiting ...")
            break

        while vod_2.isOpened():
            ret_2, frame_2 = vod_2.read()
            if not ret_2: # if frame is read correctly ret is True
                print("Can't receive frame (stream end?). Exiting ...")
                break

        
            out.write(result)
            cv2.imshow("Mask Applied to Image", result)
            if cv2.waitKey(1) == ord('q'):
                break

    vod_1.release()
    vod_2.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    vod_path = './vods/DRX vs FNATIC - VALORANT Champions - Knockout - Fracture Map 3_EDITED.mp4'
    mask_path_1 = vod_path[:-10]+'MASK_COLOR.mp4'
    mask_path_2 = vod_path[:-10]+'MASK_DEFAULT.mp4'
    color_path = vod_path[:-10]+'COLOR.mp4'
    out_path = vod_path[:-10]+'FINAL.mp4'

    highlight_color(vod_path=vod_path, team='attack', out_path=color_path)
    # add_mask(vod_path=color_path, vod_map='split', out_path=mask_path_1)
    # combine_masks(vod_path_1=mask_path_1, vod_path_2=mask_path_2, out_path=out_path)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
