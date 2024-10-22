import cv2
from deepface import DeepFace
import numpy as np

# Ask the user for the paths to the two images
image1_path = input("Enter the path to the first image: ")
image2_path = input("Enter the path to the second image: ")

# Load the images
image1 = cv2.imread(image1_path)
image2 = cv2.imread(image2_path)

# Ensure images are loaded
if image1 is None:
    print(f"Could not load image at {image1_path}")
    exit()
if image2 is None:
    print(f"Could not load image at {image2_path}")
    exit()


# Function to detect face and get bounding box
def get_face_area(image):
    detections = DeepFace.extract_faces(img_path=image, detector_backend='mtcnn', enforce_detection=False)
    if len(detections) > 0:
        face_info = detections[0]
        facial_area = face_info["facial_area"]
        return facial_area
    else:
        return None


# Get facial areas
facial_area1 = get_face_area(image1_path)
facial_area2 = get_face_area(image2_path)

if facial_area1 is None or facial_area2 is None:
    print("Face not detected in one of the images.")
    exit()

# Extract face regions
x1, y1, w1, h1 = facial_area1['x'], facial_area1['y'], facial_area1['w'], facial_area1['h']
x2, y2, w2, h2 = facial_area2['x'], facial_area2['y'], facial_area2['w'], facial_area2['h']

face_region1 = image1[y1:y1 + h1, x1:x1 + w1]
face_region2 = image2[y2:y2 + h2, x2:x2 + w2]

# Resize faces to match the target regions
face_region1_resized = cv2.resize(face_region1, (w2, h2))
face_region2_resized = cv2.resize(face_region2, (w1, h1))

# Create masks for seamless cloning
mask1 = 255 * np.ones(face_region1_resized.shape, face_region1_resized.dtype)
mask2 = 255 * np.ones(face_region2_resized.shape, face_region2_resized.dtype)

# Determine centers for seamless cloning
center1 = (x2 + w2 // 2, y2 + h2 // 2)
center2 = (x1 + w1 // 2, y1 + h1 // 2)

# Swap faces using seamless cloning
mixed_clone1 = cv2.seamlessClone(face_region1_resized, image2, mask1, center1, cv2.NORMAL_CLONE)
mixed_clone2 = cv2.seamlessClone(face_region2_resized, image1, mask2, center2, cv2.NORMAL_CLONE)

# Save the swapped images
cv2.imwrite('face/1.png', mixed_clone2)
cv2.imwrite('face/2.png', mixed_clone1)

print("Face swapping completed. Swapped images saved as 'image1_swapped.jpg' and 'image2_swapped.jpg'.")