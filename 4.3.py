import numpy as np
import collections
import cv2
from motrackers.detectors import TF_SSDMobileNetV2
from motrackers import CentroidTracker
from motrackers.utils import draw_tracks

from firebase import firebase
from threading import Timer
# import time

VIDEO_FILE = "./assets/pep.mp4"
WEIGHTS_PATH ='./assets/frozen_inference_graph.pb'
CONFIG_FILE_PATH = './assets/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
LABELS_PATH = "./assets/ssd_mobilenet_v2_coco_names.json"

url = 'https://test-project-3dc48-default-rtdb.asia-southeast1.firebasedatabase.app/'
firebase = firebase.FirebaseApplication(url)

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.2
DRAW_BOUNDING_BOXES = True
USE_GPU = False


tracker = CentroidTracker(max_lost=30, tracker_output_format='mot_challenge')


model = TF_SSDMobileNetV2(
    weights_path=WEIGHTS_PATH,
    configfile_path=CONFIG_FILE_PATH,
    labels_path=LABELS_PATH,
    confidence_threshold=CONFIDENCE_THRESHOLD,
    nms_threshold=NMS_THRESHOLD,
    draw_bboxes=DRAW_BOUNDING_BOXES,
    use_gpu=USE_GPU
)

H, W = 0, 0


def checkLeft(pts, x_c):
    global H, W
    if len(pts) >= 2 and pts[-1] < W // 2 and pts[-2] >= W // 2:
        direction = x_c - np.mean(pts)
        if direction < 0:
            return True
        else:
            return False
    else:
        return False


def checkRight(pts, x_c):
    global H, W
    if len(pts) >= 2 and pts[-1] > W // 2 and pts[-2] <= W // 2:
        direction = x_c - np.mean(pts)
        if direction > 0:
            return True
        else:
            return False
    else:
        return False


def main(video_path, model, tracker):
    global H, W
    totalLeft = 0
    totalRight = 0
    counted_ids = []
    pts = collections.defaultdict(list)

    cap = cv2.VideoCapture(video_path)
    # cap = cv2.VideoCapture(0)
    while True:
        ok, image = cap.read()

        if not ok:
            break

        image = cv2.resize(image, (640, 480))
        H, W = image.shape[:2]

        # people detection
        bboxes, confidences, class_ids = model.detect(image)

        # update tracker
        tracks = tracker.update(bboxes, confidences, class_ids)

        # draw boundingbox
        updated_image = model.draw_bboxes(image.copy(), bboxes, confidences, class_ids)

        # draw centertroid
        updated_image = draw_tracks(updated_image, tracks)

        # draw center line
        cv2.line(updated_image, (W // 2, 0), (W // 2, H), (0, 0, 255), 2)

        # update monitor result
        for track in tracks:
            # track_id
            track_id = track[1]

            # x coordinate
            x_coord = track[2]

            # width
            width = track[4]

            # x_center
            x_c = int(x_coord + 0.5 * width)

            # append x coordinate
            pts[track_id].append(x_c)

            if track_id not in counted_ids and checkRight(pts[track_id], x_c):
                counted_ids.append(track_id)
                totalRight += 1
                firebase.put("/Test Val", "Kanan", totalRight)
                del pts[track_id]
            if track_id not in counted_ids and checkLeft(pts[track_id], x_c):
                counted_ids.append(track_id)
                totalLeft += 1
                firebase.put("/Test Val", "Kiri", totalLeft)
                del pts[track_id]

            # penumpang = totalLeft +totalRight
            # firebase.put("/Test Val", "Value", penumpang)











    cap.release()
    # cv2.destroyAllWindows()
main(VIDEO_FILE,model,tracker)


def kirim (left, right) :
    penumpang = left + right
    firebase.put("/Test Val", "Value", penumpang)
    print(penumpang)
    Timer(2, kirim).start()

kirim(totalLeft,totalRight)