import numpy as np
import cv2
from scipy.ndimage.filters import uniform_filter


# Draw a grid with the specified cell lengths over an image
def add_grid_lines(img, cell_length=30):
    for i in range(0, int(img.shape[0] / cell_length) + 1):
        cv2.line(img, (0, i * cell_length), (img.shape[1], i * cell_length), (0, 0, 255), 1, 1)
    for j in range(0, int(img.shape[1] / cell_length) + 1):
        cv2.line(img, (j * cell_length, 0), (j * cell_length, img.shape[0]), (0, 0, 255), 1, 1)


# Take a BGR binary image ([0,0,0] or [255,255,255]) and convert it to a 2D array to map where there is empty space
# and where there is objects
def convert_thresh_to_map_slow(img, cell_length=30, shift_amount=5, visualize=False):
    result = []
    # (y,x) indicates the position of the top left of the cell
    # On each iteration shift where to position the top left of the cell by the shift_amount specified
    for y in range(0, img.shape[0] - cell_length + 1, shift_amount):
        row = []
        for x in range(0, img.shape[1] - cell_length + 1, shift_amount):
            # Segment a region with specified the height and width as specified by cell length
            segment = img[y:y + cell_length, x:x + cell_length]
            # If the segment does not contain any white pixels, then it is empty, so we mark its value as 9
            if len(np.where(segment == [255, 255, 255])[0]) == 0:
                if visualize:
                    row.append(np.array([0, 0, 0], dtype=np.uint8))
                else:
                    row.append(0)
            # Otherwise we mark it as 1
            else:
                if visualize:
                    row.append(np.array([255, 255, 255], dtype=np.uint8))
                else:
                    row.append(1)
        result.append(row)
    if visualize:
        result = np.array(result)
    return result


# Take a BGR binary image ([0,0,0] or [255,255,255]) and convert it to a 2D array to map where there is empty space
# and where there is objects
def convert_thresh_to_map(img, cell_length=30, shift_amount=5, visualize=False):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    conv_img = uniform_filter(img, size=cell_length, mode="constant", cval=1)
    binary_conv = np.ones(shape=(img.shape[0], img.shape[1]), dtype=np.uint8)
    binary_conv[np.where(conv_img == 0)] = 0
    if visualize:
        binary_conv = binary_conv * 255
        binary_conv = cv2.cvtColor(binary_conv, cv2.COLOR_GRAY2BGR)
    else:
        binary_conv = binary_conv.tolist()
    return binary_conv


# Convert image to grayscale
# Use scipy.ndimage.filters.convolve
# Create binary mask of where non zero
# Have numpy array of black pixels and set to white wherever true
