from ObjectDetection.EnemyDetectionCv2.EnemyDetection import EnemyDetection
from ObjectDetection.EnemyDetectionCv2.EnemyTargeting import EnemyTargeting
import cv2, os
import numpy as np
if __name__ == "__main__":
    ed = EnemyDetection(video_input=0)
    et = EnemyTargeting(0)
    while True:
        try:
            frame = ed.get_image()
            params = [cv2.IMWRITE_JPEG_QUALITY, 15]
            _, buffer = cv2.imencode('.jpg', frame, params)
            frame = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
            person = ed.get_people_from_image(frame)
            if person != ():
                x = person[0]
                y = person[1]
                w = person[2]
                h = person[3]
                
                center = et.get_center_of_people(person)
                
                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 255), 2)    
                # Lazer dot
                cv2.circle(frame, center, 5, (0, 0, 255), 5)
            # Show the frame
            cv2.imshow('frame', frame)
        except:
            pass
        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        