import cv2
import numpy as np

# Capture video from the camera
cap = cv2.VideoCapture(0)  # Use the correct index for your camera

# Initialize the first frame
ret, frame1 = cap.read()
frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame1_gray = cv2.GaussianBlur(frame1_gray, (21, 21), 0)

# Define a region of interest (ROI) for the tray
roi = (100, 100, 400, 400)  # Example coordinates, adjust as needed

while True:
    # Read the next frame
    ret, frame2 = cap.read()
    if not ret:
        break
    
    # Extract the ROI from the frame
    frame2_roi = frame2[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    
    # Convert the frame to grayscale and blur it
    frame2_gray = cv2.cvtColor(frame2_roi, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.GaussianBlur(frame2_gray, (21, 21), 0)
    
    # Compute the absolute difference between the current frame and previous frame
    frame_diff = cv2.absdiff(frame1_gray, frame2_gray)
    
    # Apply a threshold to highlight motion
    _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
    
    # Dilate the thresholded image to fill in gaps
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    # Find contours of the regions where there is motion
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Analyze contours to determine if there is significant movement
    moving = False
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Adjust the area threshold as needed
            moving = True
            break
    
    if not moving:
        print("Tray is not moving!")
    else:
        print("Tray is spinning.")
    
    # Update the previous frame
    frame1_gray = frame2_gray
    
    # Display the camera feed with the detected motion (for debugging)
    cv2.rectangle(frame2, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 255, 0), 2)
    cv2.imshow('Motion Detection', frame2)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()