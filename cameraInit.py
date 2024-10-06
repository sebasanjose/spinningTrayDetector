import cv2

# Capture video from the camera
cap = cv2.VideoCapture(0)  # Use the correct index for your camera

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
