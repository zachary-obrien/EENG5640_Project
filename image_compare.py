#%%

# Used to load images and convert to grayscale
# if needed
from PIL import Image

# Used to perform matrix operations without manual
# effort
import numpy as np

# Used for calculating disparity and distance
import math


#%%

def image_compatability(image1, image2):
    if image1.shape == image2.shape and len(image1.shape) == 2:
        return True
    else:
        return False

# Use PIL (pillow) to lode in the image from file
# and then convert it to a matrix using numpy
def fetch_image_array(filename):
    try:
        img = Image.open(filename)
        return np.asarray(img)
    except:
        print("No image found by that name")

#%%

def get_min_col(matrix, row_matrix):
    # print("Matrix:", matrix)
    # print("Row Matrix:", row_matrix)
    col_val = 0
    min_score = -1
    found_column = -1
    # doing 8 nearest neighbors with a buffered image, so always going to be col
    # 1  and shape - 1 to skip buffer
    for index in range(1, row_matrix.shape[1]-1):
        # we're getting the submatrix that that is -1 and +2
        # (because it's non-inclusive)
        if index + 2 > row_matrix.shape[1]:
            compare_matrix = row_matrix[:,index-1:-1]
        else:
            compare_matrix = row_matrix[:,index-1:index+2]
        diff_matrix = np.abs(matrix - compare_matrix)
        matrix_score = np.sum(diff_matrix)
        if min_score == -1 or matrix_score < min_score:
            min_score = matrix_score
            found_column = col_val
        col_val += 1
    return found_column, min_score

#%%

def get_similar_point(left_image, right_image, row, column):
    buffered_left_image = np.pad(left_image, pad_width=1, mode='edge')
    buffered_right_image = np.pad(right_image, pad_width=1, mode='edge')
    point_matrix = buffered_left_image[row:row+3,column:column+3]
    row_matrix = buffered_right_image[row:row+3,:]
    found_col, score = get_min_col(point_matrix,row_matrix)
    return row, found_col

#%%

fake_left_image = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

fake_right_image = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

fake_index = (5,2)
found_row, found_col = get_similar_point(fake_left_image, fake_right_image,
                                             fake_index[0], fake_index[1])
# print("Expected Row,Col: 5 , 6")
# print("Got Row,Col:    ", found_row, ",", found_col)
