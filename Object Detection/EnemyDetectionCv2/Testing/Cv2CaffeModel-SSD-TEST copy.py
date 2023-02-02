import cv2
import numpy as np
import os

os.chdir(r"E:\Final Project\Auto Aim Nerf\Object Detection\EnemyDetectionCv2\Models")
# Load the pre-trained model for person detection
net = cv2.dnn.readNetFromCaffe('..\\Models\\MobileNetSSD_deploy.prototxt', '..\\Models\\MobileNetSSD_deploy.caffemodel')

# Load the video stream
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to a blob
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
    net.setInput(blob)

    # Run forward pass to get the detections
    detections = net.forward()

    # Loop over the detections
    for i in range(detections.shape[2]):
        try:
            confidence = detections[0, 0, i, 2]
            if confidence > 0.8:
                # Get the x, y, w, h for the detection
                x = int(detections[0, 0, i, 3] * frame.shape[1])
                y = int(detections[0, 0, i, 4] * frame.shape[0])
                w = int(detections[0, 0, i, 5] * frame.shape[1])
                h = int(detections[0, 0, i, 6] * frame.shape[0])

                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 255), 2)
        except:
            continue
    # Show the frame
    cv2.imshow('frame', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream
cap.release()

# Close all the windows
cv2.destroyAllWindows()
