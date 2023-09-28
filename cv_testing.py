import cv2
import numpy as np

frame = cv2.imread('./vods/frame.png', cv2.IMREAD_COLOR)
windowName = 'vod'

class ChangeEffects():
    saved_blur_amt = 3
    saved_saturation_amt = 3

    def change_blur_amt(self, val):
        self.add_effects(blur_amt=(val*2)+1, saturation_amt=self.saved_saturation_amt)

    def change_saturation_amt(self, val):
        self.add_effects(blur_amt=self.saved_blur_amt, saturation_amt=val)

    def add_effects(self, blur_amt: int, saturation_amt: int):
        frame_copy = frame.copy()
        self.saved_blur_amt = blur_amt
        self.saved_saturation_amt = saturation_amt

        # Blur
        frame_copy = cv2.blur(frame_copy, (blur_amt, blur_amt))

        # Saturation
        frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(frame_copy)
        s = s*saturation_amt
        s = np.clip(s,0,255)
        frame_copy = cv2.merge([h,s,v])

        # Threshold color
        lower_limit = np.array([0, 155, 155])
        upper_limit = np.array([360, 255, 255])
        frame_copy = cv2.inRange(frame_copy, lower_limit, upper_limit)
        kernel = np.ones((3, 3), np.uint8)
        frame_copy = cv2.dilate(frame_copy, kernel)

        cv2.imshow(windowName, frame_copy)

    def __init__(self):
        cv2.imshow(windowName, frame)
        cv2.createTrackbar('blur_amt', windowName, 1, 100, self.change_blur_amt)
        cv2.createTrackbar('saturation_amt', windowName, 0, 100, self.change_saturation_amt)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

ChangeEffects()