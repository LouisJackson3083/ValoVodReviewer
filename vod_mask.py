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
        yscale = 0.89
        xscale = 0.88
        yoff = 0.09
        xoff = 0.085

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

def main():
    vod_path = './vods/FNATIC vs FUT Esports - VALORANT Champions - Knockout - Split Map 1_EDITED.mp4'
    out_path = vod_path[:-10]+'FINAL.mp4'
    add_mask(vod_path=vod_path, out_path=out_path)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
