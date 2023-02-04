from ObjectDetection.EnemyDetectionCv2.EnemyDetection import EnemyDetection
from ObjectDetection.EnemyDetectionCv2.EnemyTargeting import EnemyTargeting
import cv2, os

if __name__ == "__main__":
    ed = EnemyDetection()
    et = EnemyTargeting(1)
    while True:
        frame = ed.get_image()
        person = ed.get_people_from_image(frame)
        if person != ():
            x = person[0]
            y = person[1]
            w = person[2]
            h = person[3]
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 255), 2)    
            
            center = et.get_center_of_people(person)
            # Lazer dot
            cv2.circle(frame, center, 5, (0, 0, 255), 5)
        # Show the frame
        cv2.imshow('frame', frame)
        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(10000) & 0xFF == ord('q'):
            break
        