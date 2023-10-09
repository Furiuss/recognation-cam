import cv2
import numpy as np
import os
import re

# the same function we've used before
from helper_functions import resize_video

### Choose the face detector
# -> Options: ssd   |  haarcascade
detector = "ssd"  # we suggest to keep SSD for more accurate detections
max_width = 800           # leave None if you don't want to resize and want to keep the original size of the video stream frame

max_samples = 20    # to control how many photos we'll be taking
starting_sample_number = 0  # default=0, but if you already have taken photos for the same person AND you don't want to overwrite them you need to choose a number higher than the last number of samples.
                             # e.g. i took 20 photos and want to take more but keep the others, so I need to change from 0 to 21

# def parse_name(name):
#     name = re.sub(r"[^\w\s]", '', name) # Remove all non-word characters (everything except numbers and letters)
#     name = re.sub(r"\s+", '_', name)    # Replace all runs of whitespace with a single underscore
#     return name
#
# # Create the final folder where the photos will be saved (if the path already doesn't exist)
def create_folders(final_path):
    if not os.path.exists(final_path):
        os.makedirs(final_path)
    # if not os.path.exists(final_path_full):
    #     os.makedirs(final_path_full)

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
                # face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    return face_roi, frame
#
# if detector == "ssd":
#     # For Face Detection with SSD (OpenCV's DNN) -> load weights from caffemodel
#     network = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")
# else:
#     # For Face Detection with HAAR CASCADE -> import haar cascade for face detection
#     face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#
# # video capture object
# cam = cv2.VideoCapture(0)
#
# folder_faces = "dataset/"      # where the cropped faces will be stored
# folder_full = "dataset_full/"  # where will be stored the full photos
#
# person_name = input('Enter your name: ')
# person_name = parse_name(person_name)
#
# # Join the path (dataset directory + subfolder)
# final_path = os.path.sep.join([folder_faces, person_name])
# final_path_full = os.path.sep.join([folder_full, person_name])
# print("All photos are going to be saved in {}".format(final_path))

# create_folders(final_path, final_path_full)

# sample = 0
# while(True):
#     ret, frame = cam.read()
#
#     # resize only if a max_width is specified
#     if max_width is not None:
#         video_width, video_height = resize_video(frame.shape[1], frame.shape[0], max_width)
#         frame = cv2.resize(frame, (video_width, video_height))
#
#     face_roi, processed_frame = detect_face_ssd(network, frame)
#
#     if face_roi is not None:
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             sample = sample+1
#             photo_sample = sample+starting_sample_number-1 if starting_sample_number>0 else sample
#             image_name = person_name + "." + str(photo_sample) + ".jpg"
#             cv2.imwrite(final_path + "/" + image_name, face_roi)  # save the cropped face (ROI)
#             cv2.imwrite(final_path_full + "/" + image_name, frame)  # save the full image too (not cropped)
#             print("=> photo " + str(sample))
#
#             cv2.imshow("face", face_roi)
#
#             #cv2.waitKey(500)
#
#     cv2.imshow("Capturing face", processed_frame)
#     cv2.waitKey(1)
#
#     if (sample >= max_samples):
#         break
#
# print ("Completed!")
# cam.release()
# cv2.destroyAllWindows()