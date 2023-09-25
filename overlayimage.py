import cv2
import numpy as np

image_path = 'test.png'
mask_path = './minimaps/split.png'

image = cv2.imread(image_path)
cv2.imshow("Original", image)
cv2.waitKey(0)

# mask = np.zeros(image.shape[:2], dtype="uint8")
# cv2.rectangle(mask, (0, 90), (290, 450), 255, -1)


mask = cv2.imread(mask_path)
opaque_pixels = np.where(
    (mask[:, :, 0] != 0) |
    (mask[:, :, 1] != 0) |
    (mask[:, :, 2] != 0)
)
mask[opaque_pixels] = [255, 255, 255]
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
cv2.imshow("Rectangular Mask", mask)
cv2.waitKey(0)

masked = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Mask Applied to Image", masked)
cv2.waitKey(0)