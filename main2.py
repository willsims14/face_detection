import cv2
import sys
import time


def main(max_images_to_download=15, reset_interval_seconds=10):
    # Dependencies
    faceCascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')
    video_capture = cv2.VideoCapture(0)

    # Flags and Counters
    found_face = False
    length_of_faces = 0
    new_face_time = 0
    face_count = 0

    while True and face_count < max_images_to_download:
        # If it has been enough time since the last face was captured
        if found_face == True and (time.time() - new_face_time) > reset_interval_seconds:
            print "Elapsed Time Since Capture: {} Seconds".format(str(round((time.time() - new_face_time), 2)))
            sys.stdout.flush()
            found_face = False # Reset Flag

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )


        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        length_of_faces = len(faces)
        if found_face == False and len(faces) > 0:            
            print "Found New Face"
            sys.stdout.flush()
            new_face_time = time.time()
            new_image_filename = 'images/new_face_{}.png'.format(str(face_count+1)) 
            cv2.imwrite(new_image_filename, frame) # Download Image


            found_face = True # Set Flag
            face_count += 1 # Increment Face Counter

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    num_args = len(sys.argv)
    if num_args == 1:
        print "Enter and argument"
    # Number of Images to Download
    elif num_args == 2:
        if unicode(sys.argv[1], 'utf-8').isnumeric():
            main(max_images_to_download=int(sys.argv[1]))
    # Seconds to reset
    elif num_args == 3:
        if unicode(sys.argv[1], 'utf-8').isnumeric() and unicode(sys.argv[2], 'utf-8').isnumeric():
            main(max_images_to_download=int(sys.argv[1]), reset_interval_seconds=int(sys.argv[2]))

