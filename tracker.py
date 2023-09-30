import math

class EuclideanDistTracker:
    def __init__(self):
        # Here we create a queue of frames that contain a dictionary
        # of centre positions of detected objects
        self.frames = [{}]
        # Keep count of the object IDs
        self.id_count = 0
        # How far back should the tracker look for detected objects?
        # This is to prevent "flickering"
        self.frame_limit = 150
        self.max_object_distance = 15

    def update(self, detected_objects):
        tracked_object_ids = []

        # Get the centre point of a detected object
        for object in detected_objects:
            # get the position, and size
            x, y, w, h = object
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if the object has been detected already
            redetected_object = False
            best_dist = self.max_object_distance
            best_rect = None
            # for each dict of centre points
            for centre_points in self.frames:
                # get the id, position of each previously detected object
                for id, pt in centre_points.items():
                    # calculate the euclidean distance
                    dist = math.hypot(cx-pt[0], cy-pt[1])
                    
                    # if the distance is small enough, we have a match
                    if dist < best_dist:
                        best_dist = dist
                        best_rect = [x, y, w, h, id]
                        redetected_object = True
            
            if (redetected_object == True):
                # append the redetected object, pop it from the dictionary
                tracked_object_ids.append(best_rect)
                for centre_points in self.frames:
                    if (best_rect[4] in centre_points):
                        centre_points.pop(best_rect[4])

            # If we have detected a new object
            if (redetected_object == False):
                tracked_object_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1
            
        new_objects = {}
        for tracked_object in tracked_object_ids:
            x, y, w, h, id = tracked_object
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            new_objects[id] = (cx, cy)
        self.frames.append(new_objects)
        
        if (len(self.frames) > self.frame_limit):
            self.frames.pop(0)

        return tracked_object_ids
        
