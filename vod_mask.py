import cv2
import numpy as np

class Vod_Masker():
    """
    A class that applies a binary mask to a vod and saves he masked vod to an output location
    args:
        vod_path - a string that represents the location to the vod
        vod_map - a string that represents the map of the vod
        verbose - a bool that can be turned on to see the output of each step
    """

    vod = None
    vod_map = None
    vod_path = None
    vod_shape = None
    vod_fps = None
    out = None
    out_path = None
    mask = None
    verbose = None

    def __init__(self, vod_path: str, vod_map: str, verbose: bool = False):
        self.verbose = verbose

        # Initialize vod related variables
        self.vod_path = vod_path
        self.vod_map = vod_map
        self.vod = cv2.VideoCapture(self.vod_path)
        self.vod_shape = (int(self.vod.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(self.vod.get(cv2.CAP_PROP_FRAME_WIDTH)))
        self.vod_fps = self.vod.get(cv2.CAP_PROP_FPS)
        
        # Initialize output video related variables
        self.out_path = vod_path[:-10]+'MASKED.mp4'
        self.out = cv2.VideoWriter(
            self.out_path,
            cv2.VideoWriter_fourcc(*'mp4v'), 
            self.vod_fps, 
            (self.vod_shape[1],self.vod_shape[0])
        )

        self.mask = self.get_mask()

        self.apply_mask()

    def get_mask(self):
        if (self.vod_map == 'split'): # get the default scaling and offsets for the map
            yscale = 0.88
            xscale = 0.88
            yoff = 0.095
            xoff = 0.09
        
        # get the minimap path, and load it as a grayscale image
        mask_path = './minimaps/'+self.vod_map+'.png'
        mask = cv2.imread(mask_path)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        # here we are changing the x & y offset based on the vod resolution
        yoff = int(self.vod_shape[0]*yoff)
        xoff = int(self.vod_shape[1]*xoff)

        # create a new shape for the mask based on the vod scale, and resize the minimap
        new_mask_shape = (int(self.vod_shape[0]*xscale), int(self.vod_shape[1]*yscale))
        # NOTE: might want to look at other interpolation methods?
        mask = cv2.resize(mask, new_mask_shape, interpolation=cv2.INTER_LINEAR)

        # here we clip the values to the boundaries of the vod shape
        yoff_max = min(yoff+mask.shape[0], self.vod_shape[0])
        xoff_max = min(xoff+mask.shape[1], self.vod_shape[1])
        yoff = max(0, yoff)
        xoff = max(0, xoff)

        # create a final binary mask image
        mask_final = np.zeros(self.vod_shape, dtype="uint8")
        mask_final[yoff:yoff_max, xoff:xoff_max] = mask[0:yoff_max-yoff, 0:xoff_max-xoff]
        
        if (self.verbose):
            cv2.imshow("Final Mask", mask_final)
            cv2.waitKey(0)
        
        return mask_final
    
    def apply_mask(self):
        # open vod and read it
        while self.vod.isOpened():
            ret, frame = self.vod.read()
            if not ret: # if frame is read correctly ret is True
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # apply mask
            frame = cv2.bitwise_and(frame, frame, mask=self.mask)

            # write opened frame to output path
            self.out.write(frame)

            # if verbose, show video
            if (self.verbose):
                cv2.imshow("Mask Applied to Image", frame)
                if cv2.waitKey(1) == ord('q'):
                    break

        self.vod.release()
        self.out.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    vod_path = './vods/DRX vs FNATIC - VALORANT Champions - Knockout - Fracture Map 3_EDITED.mp4'
    Vod_Masker(
        vod_path=vod_path,
        vod_map='split',
        verbose=True,
    )
