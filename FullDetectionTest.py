from ObjectDetection.EnemyDetectionCv2.EnemyDetection import EnemyDetection
from ObjectDetection.EnemyDetectionCv2.EnemyTargeting import EnemyTargeting
import cv2, os
import numpy as np
STEP_SIZE_THRESHOLD: int = 60
SMALL_STEPS_IN_A_ROW: int = 10
small_steps_counter = 0
add_vertical = 5
YELLOW =(0, 255, 255)
PURPLE = (255, 0, 255)
color = YELLOW

def steps_thresholding(steps_tuple: tuple) -> tuple:
        global small_steps_counter
        global color
        """
        Inorder to avoid small steps we filter out any step lower
        then a certin threshold {STEP_SIZE_THRESHOLD}
        Args:
            steps_tuple: (tuple) - steps tuple, (x_steps, y_steps)
        Returns:
            filtered_steps_tuple: (tuple) - steps tuple, (x_steps, y_steps)
        """
        x_steps = 0 if abs(steps_tuple[0]) < STEP_SIZE_THRESHOLD else steps_tuple[0]
        y_steps = 0 if abs(steps_tuple[1]) < STEP_SIZE_THRESHOLD else steps_tuple[1]
        if not all((x_steps, y_steps)):
            print("Shouls send small steps: ", steps_tuple[0], steps_tuple[1], small_steps_counter)
            if (small_steps_counter < SMALL_STEPS_IN_A_ROW):
                # print("Steps: ", steps_tuple, "small steps counter: ", self.small_steps_counter)
                small_steps_counter += 1
                color = PURPLE
                return (steps_tuple[0], steps_tuple[1] + add_vertical)
            color = YELLOW
            # print("Too many small steps: ", steps_tuple, "small steps counter: ", small_steps_counter)
            return (x_steps, y_steps + add_vertical)
        # print("No small steps: ", steps_tuple, "small steps counter: ", small_steps_counter)
        color = YELLOW
        small_steps_counter = 0 
        return (x_steps, y_steps + add_vertical)

if __name__ == "__main__":
    ed = EnemyDetection(video_input=0)
    et = EnemyTargeting(1)
    # Get width of window
    window_width: int = ed.camera.get(3) 

        # Get height of window
    window_height: int = ed.camera.get(4)

    x = 0
    y = 0
    w = 0
    h = 0
    while True:
        try:
            frame = ed.get_image()
            params = [cv2.IMWRITE_JPEG_QUALITY, 15]
            _, buffer = cv2.imencode('.jpg', frame, params)
            frame = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
            person = ed.get_people_from_image(frame)
            if person != ():
                

                steps = et.get_steps_to_people_center(window_width // 2, window_height // 2, person)
                center = et.get_center_of_people(person)

                steps = steps_thresholding(steps)
                if steps[0] > 0 or steps[1] > 0:

                    x = person[0]
                    y = person[1]
                    w = person[2]
                    h = person[3]

                if y < 40:
                    print("OverHead")
                else:
                    print("Not")
                
                cv2.rectangle(frame, (x, y), (w, h), color, 2)    
                # Lazer dot
                cv2.circle(frame, center, 5, (0, 0, 255), 5)
            # Show the frame
            cv2.imshow('frame', frame)
        except Exception as e:
            print(e)
            pass
        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        