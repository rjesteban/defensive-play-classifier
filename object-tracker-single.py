# Import the required modules
from transform import four_point_transform, get_four_points
import dlib
import cv2
import argparse as ap
import get_points
import json
import numpy as np
import os.path


def run(side_pos, four_points, source=0, dispLoc=False):
    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print "Video device or file couldn't be opened"
        exit()

    result = {side_pos: []}

    while True:
        retval, img = cam.read()
        if not retval:
            print "Cannot capture frame device"
            exit()
        break

    if len(four_points) is 0:
        result["points"] = get_four_points(img)
    else:
        result["points"] = np.array(four_points)
    img = four_point_transform(img, result["points"])

    # Co-ordinates of objects to be tracked
    # will be stored in a list named `points`
    points = get_points.run(img)

    if not points:
        print "ERROR: No object to be tracked."
        exit()

    cv2.namedWindow("tracking...", cv2.WINDOW_NORMAL)
    cv2.imshow("tracking...", img)

    # Initial co-ordinates of the object to be tracked
    # Create the tracker object
    tracker = dlib.correlation_tracker()
    # Provide the tracker the initial position of the object
    tracker.start_track(img, dlib.rectangle(*points[0]))

    while True:
        # Read frame from device or file
        retval, img = cam.read()
        if not retval:
            print "*" * 10 + "End" + "*" * 10
            break
        img = four_point_transform(img, result["points"])
        img_clean = img.copy()
        # Update the tracker
        tracker.update(img)
        # Get the position of the object, draw a
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        # print "Object tracked at [{}, {}] \r".format(pt1, pt2),
        result[side_pos].append([int(rect.right()), int(rect.bottom())])
        if dispLoc:
            loc = (int(rect.left()), int(rect.top() - 20))
            txt = "Object tracked at [{}, {}]".format(pt1, pt2)

            cv2.putText(img, txt, loc,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.namedWindow("tracking...", cv2.WINDOW_NORMAL)
        cv2.imshow("tracking...", img)

        key = cv2.waitKey(0)
        # 'p' was typed, tweak it
        if key == 1048688:
            img = img_clean
            points = get_points.run(img)

            if not points:
                print "ERROR: No object to be tracked."
                exit()

            cv2.namedWindow("tracking...", cv2.WINDOW_NORMAL)
            cv2.imshow("tracking...", img)

            # Initial co-ordinates of the object to be tracked
            # Create the tracker object
            tracker = dlib.correlation_tracker()
            # Provide the tracker the initial position of the object
            tracker.start_track(img, dlib.rectangle(*points[0]))
        if key == 1048603:
            break
    # Relase the VideoCapture object
    cam.release()
    result["points"] = result["points"].tolist()
    return result


if __name__ == "__main__":
    # Parse command line arguments
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])

    side_pos = raw_input("o or d,then position #, ex: o1 is offense 1\n")
    result = {}
    four_points = []

    file = args["videoFile"] + ".json"
    json_data = {}
    if os.path.exists(file):
        with open(file) as json_file:
            json_data = json.load(json_file)
            four_points = np.array(json_data["points"])

    result = run(side_pos, four_points, source, args["dispLoc"])
    with open(file, 'w') as f:
        json_data[side_pos] = result[side_pos]
        json_data["points"] = result["points"]
        f.write(json.dumps(json_data, sort_keys=True))
