import cv2
import numpy as np
import time

# Capture video from the camera
cap = cv2.VideoCapture(0)  # Use the correct index for your camera

# Initialize the first frame
ret, frame1 = cap.read()
frame1_roi = frame1[100:500, 100:500]  # Extract ROI from the initial frame
frame1_gray = cv2.cvtColor(frame1_roi, cv2.COLOR_BGR2GRAY)
frame1_gray = cv2.GaussianBlur(frame1_gray, (21, 21), 0)

# Define a region of interest (ROI) for the tray as an ellipse
roi_center = (300, 300)  # Center of the ellipse (adjust as needed)
roi_axes = (200, 200)  # Length of the axes (adjust as needed)
roi_angle = 0  # Angle of rotation of the ellipse

# Counter for continuous tray movement
movement_counter = 0
alert_sent = False

while True:
    # Read the next frame
    ret, frame2 = cap.read()
    if not ret:
        break
    
    # Create a mask for the elliptical ROI
    mask = np.zeros(frame2.shape[:2], dtype=np.uint8)
    cv2.ellipse(mask, roi_center, roi_axes, roi_angle, 0, 360, 255, -1)
    
    # Apply the mask to both the initial and current frames
    frame1_masked = cv2.bitwise_and(frame1, frame1, mask=mask)
    frame2_masked = cv2.bitwise_and(frame2, frame2, mask=mask)
    
    # Convert the masked frames to grayscale and blur them
    frame1_gray = cv2.cvtColor(frame1_masked, cv2.COLOR_BGR2GRAY)
    frame1_gray = cv2.GaussianBlur(frame1_gray, (21, 21), 0)
    frame2_gray = cv2.cvtColor(frame2_masked, cv2.COLOR_BGR2GRAY)
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
    
    if moving:
        movement_counter += 1
        if movement_counter >= 14 and not alert_sent:
            alert_sent = True
    else:
        movement_counter = 0
        alert_sent = False
    
    # Display message if the tray stops moving
    if not moving:
        cv2.putText(frame2, 'TRAY STOPPED MOVING!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        print("Tray is not moving!")
    else:
        print("Tray is spinning.")
    
    # Update the previous frame
    frame1 = frame2.copy()
    
    # Display the camera feed with the detected motion (for debugging)
    cv2.ellipse(frame2, roi_center, roi_axes, roi_angle, 0, 360, (0, 255, 0), 2)
    cv2.imshow('Motion Detection', frame2)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()