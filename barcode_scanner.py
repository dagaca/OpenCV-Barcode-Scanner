import cv2
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode, ZBarSymbol


def main():
    # Start the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert the frame to a PIL image
        pil_image = Image.fromarray(gray)

        # Use the decode function with the ZBar library
        result = decode(pil_image, symbols=[ZBarSymbol.QRCODE])

        for symbol in result:
            # Print the type of barcode
            print(f"Barcode Type: {symbol.type}")

            # Get the barcode data and check its type
            barcode_data = symbol.data
            if isinstance(barcode_data, bytes):
                # Convert the byte data to a string
                barcode_data = barcode_data.decode('utf-8')

            # Print the barcode content
            print(f"Barcode Content: {barcode_data}")

            # Draw a rectangle around the barcode
            rect_points = symbol.polygon

            # At least 4 points are needed to draw a rectangle
            if len(rect_points) >= 4:
                # Take only the first 4 points
                pts = rect_points[:4]
                pts = np.array(pts, dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Show the frame
        cv2.imshow('Barcode Scanner', frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera
    cap.release()

    # Close all windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()