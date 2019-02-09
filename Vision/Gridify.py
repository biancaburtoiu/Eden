import numpy as np
import cv2


# Draw a grid with the specified cell lengths over an image
def add_grid_lines(img, cell_length=21):
    for i in range(0, int(img.shape[0] / grid_size) + 1):
        cv2.line(img, (0, i * grid_size), (img.shape[1], i * grid_size), (0, 0, 255), 1, 1)
    for j in range(0, int(img.shape[1] / grid_size) + 1):
        cv2.line(img, (j * grid_size, 0), (j * grid_size, img.shape[0]), (0, 0, 255), 1, 1)

# Take a BGR binary image ([0,0,0] or [255,255,255]) and convert it to a 2D array to map where there is empty space
# and where there is objects
def convert_thresh_to_map(img, cell_length=30, shift_amount=10):
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
                row.append(0)
            # Otherwise we mark it as 1
            else:
                row.append(1)
        result.append(row)
    return result
