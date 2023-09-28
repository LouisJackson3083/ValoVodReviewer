import cv2
import numpy as np

frame = cv2.imread('./vods/frame.png', cv2.IMREAD_COLOR)
windowName = 'vod'

class ChangeEffects():
    saved_blur_amt = 3
    saved_saturation_amt = 3
    saved_dilate_amt = 3
    saved_threshold_limit_dist = 100
    saved_lower_color_limit = 0
    saved_upper_color_limit = 360

    def change_blur_amt(self, val):
        self.saved_blur_amt = (val*2) + 1
        self.add_effects(
            blur_amt=self.saved_blur_amt,
            saturation_amt=self.saved_saturation_amt,
            dilate_amt=self.saved_dilate_amt,
            threshold_limit_dist=self.saved_threshold_limit_dist,
            lower_color_limit = self.saved_lower_color_limit,
            upper_color_limit = self.saved_upper_color_limit,
        )

    def change_saturation_amt(self, val):
        self.saved_saturation_amt = val
        self.add_effects(
            blur_amt=self.saved_blur_amt,
            saturation_amt=self.saved_saturation_amt,
            dilate_amt=self.saved_dilate_amt,
            threshold_limit_dist=self.saved_threshold_limit_dist,
            lower_color_limit = self.saved_lower_color_limit,
            upper_color_limit = self.saved_upper_color_limit,
        )
    
    def change_dilate_amt(self, val):
        self.saved_dilate_amt = (val*2) + 1
        self.add_effects(
            blur_amt=self.saved_blur_amt,
            saturation_amt=self.saved_saturation_amt,
            dilate_amt=self.saved_dilate_amt,
            threshold_limit_dist=self.saved_threshold_limit_dist,
            lower_color_limit = self.saved_lower_color_limit,
            upper_color_limit = self.saved_upper_color_limit,
        )

    def change_threshold_limit_dist(self, val):
        self.saved_threshold_limit_dist = val
        self.add_effects(
            blur_amt=self.saved_blur_amt,
            saturation_amt=self.saved_saturation_amt,
            dilate_amt=self.saved_dilate_amt,
            threshold_limit_dist=self.saved_threshold_limit_dist,
            lower_color_limit = self.saved_lower_color_limit,
            upper_color_limit = self.saved_upper_color_limit,
        )

    def change_lower_color_limit(self, val):
        self.saved_lower_color_limit = val
        self.add_effects(
            blur_amt=self.saved_blur_amt,
            saturation_amt=self.saved_saturation_amt,
            dilate_amt=self.saved_dilate_amt,
            threshold_limit_dist=self.saved_threshold_limit_dist,
            lower_color_limit = self.saved_lower_color_limit,
            upper_color_limit = self.saved_upper_color_limit,
        )

    def change_upper_color_limit(self, val):
        self.saved_lower_color_limit = val
        self.add_effects(
            blur_amt=self.saved_blur_amt,
            saturation_amt=self.saved_saturation_amt,
            dilate_amt=self.saved_dilate_amt,
            threshold_limit_dist=self.saved_threshold_limit_dist,
            lower_color_limit = self.saved_lower_color_limit,
            upper_color_limit = self.saved_upper_color_limit,
        )

    def add_effects(
            self, 
            blur_amt: int, 
            saturation_amt: int,
            dilate_amt: int,
            threshold_limit_dist: int,
            lower_color_limit: int,
            upper_color_limit: int,
            ):
        
        frame_copy = frame.copy()

        # Blur
        frame_copy = cv2.blur(frame_copy, (blur_amt, blur_amt))

        # Saturation
        frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(frame_copy)
        s = s*(saturation_amt/50)
        s = np.clip(s,0,255)
        frame_copy = cv2.merge([h,s,v])

        # Threshold color
        lower_limit = np.array([lower_color_limit, (255-threshold_limit_dist), (255-threshold_limit_dist)])
        upper_limit = np.array([upper_color_limit, 255, 255])
        frame_copy = cv2.inRange(frame_copy, lower_limit, upper_limit)

        # Dilate amount
        kernel = np.ones((dilate_amt, dilate_amt), np.uint8)
        frame_copy = cv2.dilate(frame_copy, kernel)

        
        res = cv2.bitwise_and(frame,frame,mask = frame_copy)
        cv2.imshow(windowName, frame_copy)
        cv2.imshow('finish', res)

    def __init__(self):
        cv2.imshow(windowName, frame)
        cv2.createTrackbar('blur_amt', windowName, 0, 100, self.change_blur_amt)
        cv2.createTrackbar('saturation_amt', windowName, 0, 100, self.change_saturation_amt)
        cv2.createTrackbar('dilate_amt', windowName, 0, 100, self.change_dilate_amt)
        cv2.createTrackbar('threshold_limit_dist', windowName, 0, 255, self.change_threshold_limit_dist)
        cv2.createTrackbar('lower_color_limit', windowName, 0, 360, self.change_lower_color_limit)
        cv2.createTrackbar('upper_color_limit', windowName, 0, 360, self.change_upper_color_limit)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

ChangeEffects()