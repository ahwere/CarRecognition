from scipy.spatial import distance
import numpy as np
from collections import OrderedDict
from collections import Counter

class Tracker:
    def __init__(self, maxLost=30):  # maxLost: maximum object lost counted when the object is being tracked
        self.nextObjectID = 0  # ID of next object
        self.objects = OrderedDict()  # stores ID:Locations
        self.lost = OrderedDict()  # stores ID:Lost_count

        self.detectedIDs = OrderedDict()
        self.detectedTimes = OrderedDict()
        self.detectedColors = OrderedDict()
        self.classified_information = []
        self.maxLost = maxLost  # maximum number of frames object was not detected.

    def addObject(self, new_object_location, label, detected_time, detected_color):
        classified_list = []
        self.objects[self.nextObjectID] = new_object_location  # store new object location
        self.lost[self.nextObjectID] = 0  # initialize frame_counts for when new object is undetected
        classified_list.append(label)

        self.detectedIDs[self.nextObjectID] = classified_list
        self.detectedTimes[self.nextObjectID] = detected_time
        self.detectedColors[self.nextObjectID] = detected_color
        self.nextObjectID += 1

    def removeObject(self, objectID):  # remove tracker data after object is lost
        del self.objects[objectID]
        del self.lost[objectID]
        #del self.detectedIDs[objectID]

    @staticmethod
    def getLocation(bounding_box):
        xlt, ylt, xrb, yrb = bounding_box
        return (int((xlt + xrb) / 2.0), int((ylt + yrb) / 2.0))

    def getClassifiedDict(self):
        return self.detectedIDs

    def getClassifiedInfo(self):
        self.classified_information = []
        for i in range(0, len(self.detectedIDs)):
            label_statis = Counter(self.detectedIDs[i])
            most = label_statis.most_common(1)
            self.classified_information.append((i, most, self.detectedTimes[i], self.detectedColors[i]))
        return self.classified_information

    def update(self, detections, labels, detected_time, detected_color):
        if len(detections) == 0:  # if no object detected in the frame
            lost_ids = list(self.lost.keys())
            for objectID in lost_ids:
                self.lost[objectID] += 1
                if self.lost[objectID] > self.maxLost: self.removeObject(objectID)

            return self.objects

        new_object_locations = np.zeros((len(detections), 2), dtype="int")  # current object locations

        for (i, detection) in enumerate(detections): new_object_locations[i] = self.getLocation(detection)

        if len(self.objects) == 0:
            for i in range(0, len(detections)): self.addObject(new_object_locations[i], labels[i], detected_time[i], detected_color[i])
        else:
            objectIDs = list(self.objects.keys())
            previous_object_locations = np.array(list(self.objects.values()))

            D = distance.cdist(previous_object_locations,
                               new_object_locations)  # pairwise distance between previous and current

            row_idx = D.min(axis=1).argsort()  # (minimum distance of previous from current).sort_as_per_index

            cols_idx = D.argmin(axis=1)[row_idx]  # index of minimum distance of previous from current

            assignedRows, assignedCols = set(), set()

            for (row, col) in zip(row_idx, cols_idx):

                if row in assignedRows or col in assignedCols:
                    continue

                objectID = objectIDs[row]
                self.objects[objectID] = new_object_locations[col]
                (self.detectedIDs[objectID]).append(labels[col])
                self.lost[objectID] = 0

                assignedRows.add(row)
                assignedCols.add(col)

            unassignedRows = set(range(0, D.shape[0])).difference(assignedRows)
            unassignedCols = set(range(0, D.shape[1])).difference(assignedCols)

            if D.shape[0] >= D.shape[1]:
                for row in unassignedRows:
                    objectID = objectIDs[row]
                    self.lost[objectID] += 1

                    if self.lost[objectID] > self.maxLost:
                        self.removeObject(objectID)

            else:
                for col in unassignedCols:
                    self.addObject(new_object_locations[col], labels[col], detected_time[col], detected_color[col])

        return self.objects
