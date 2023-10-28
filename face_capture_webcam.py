import cv2
import numpy as np
import os
import re

# the same function we've used before
from helper_functions import resize_video

detector = "ssd"  # we suggest to keep SSD for more accurate detections
max_width = 800           # leave None if you don't want to resize and want to keep the original size of the video stream frame

max_samples = 20    # to control how many photos we'll be taking
starting_sample_number = 0  # default=0, but if you already have taken photos for the same person AND you don't want to overwrite them you need to choose a number higher than the last number of samples.

# # Create the final folder where the photos will be saved (if the path already doesn't exist)
def create_folders(final_path):
    if not os.path.exists(final_path):
        os.makedirs(final_path)

# Return the detected face using SSD
def detect_face_ssd(network, orig_frame, show_conf=True, conf_min=0.7):
    frame = orig_frame.copy()  # to keep the original frame intact (just if we want to save the full image
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
    network.setInput(blob)
    detections = network.forward()

    face_roi = None
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_min:
            bbox = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (start_x, start_y, end_x, end_y) = bbox.astype("int")

            if (start_x<0 or start_y<0 or end_x > w or end_y > h):
                continue

            face_roi = orig_frame[start_y:end_y,start_x:end_x]
            face_roi = cv2.resize(face_roi, (90, 120)) ## comment IF you don`t need to resize all faces to a fixed size
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)  # draw bounding box
            if show_conf:
                text_conf = "{:.2f}%".format(confidence * 100)
                cv2.putText(frame, text_conf, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return face_roi, frame
