import cv2  # Proper import

cam_port = 0  # Use 0 for the default webcam, change to 1 if needed
cam = cv2.VideoCapture(cam_port)

inp = input('Enter person name: ')

# Capture one frame
ret, image = cam.read()

if ret:  # If image is successfully captured
    cv2.imshow(inp, image)  # Show the image

    key = cv2.waitKey(0)  # Wait for a key press
    if key:  # If any key is pressed
        cv2.imwrite(inp + ".png", image)  # Save image
        print("Image taken and saved as " + inp + ".png")
    
    cv2.destroyAllWindows()  # Close the image window
else:
    print("No image detected. Please try again.")

cam.release()  # Release the camera
