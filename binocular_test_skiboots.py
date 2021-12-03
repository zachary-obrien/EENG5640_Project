from PIL import Image, ImageOps
import numpy as np
import math
import cv2

from numpy import asarray
from numpy import savetxt

# Use PIL (pillow) to load in the image from file
# and then convert it to a matrix using numpy

def fetch_image_array(filename):
    img = Image.open(filename)
    # Set grayscale filter to image
    img_gray1 = ImageOps.grayscale(img)

    newsize = (16,9)
    img_gray = img_gray1.resize(newsize)

    # Return image array
    return np.asarray(img_gray)


def get_min_col(matrix, row_matrix):
    #print("Matrix:", matrix)
    #print("Row Matrix:", row_matrix)
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


def get_similar_point(left_image, right_image, row, column):
    buffered_left_image = np.pad(left_image, pad_width=1, mode='edge')
    buffered_right_image = np.pad(right_image, pad_width=1, mode='edge')
    point_matrix = buffered_left_image[row:row+3,column:column+3]
    row_matrix = buffered_right_image[row:row+3,:]
    found_col, score = get_min_col(point_matrix,row_matrix)
    # print(point_matrix)
    return row, found_col





def disparity(x_1,y_1,x_2,y_2):
    d = math.sqrt(((x_2-x_1)**2)+((y_2-y_1)**2))

    return d

def depth (f,b,d):
    if d == 0:
        dep = d + 0.01
        z = (f*b)/dep
    else:
        z = (f*b)/d


    return z



# Send two images to fetch_image_array(filename) / returns array
left_image = fetch_image_array('im0e0.png') # Left is 0
right_image = fetch_image_array('im1e0.png') # Right is 1


# Get height and width of images / Left and Right should have the same measurements
h, w =left_image.shape
print(h,w)



# Iterate over all pixels in left_image to get the corresponding points in right_image/
#  calculate the disparity between each corresponding points/
#  caculate the depth using (given focus length, given baseline, and calculated disparity):

depth_z = []
for y in range(h):
        for x in range(w):


            found_row, found_col = get_similar_point(left_image, right_image,
                                             y, x)

            print("Left Image row, col:  ", y, ",", x )
            print("Got Row,Col:    ", found_row, ",", found_col)

            # Get corrdinates
            #print("Disparity:")
            d = disparity(x, y, found_col, found_row)
            print("disparity:",d)

            b= 87.85 # Given baseline
            f= 1758.23 # Given focus length

            #print("Depth:")
            z = depth(f,b,d)
            depth_z.append(z)
print("List: ", depth_z)


depth_unshape = np.asarray(depth_z)
depth_matrix = np.reshape(depth_unshape, (h, w))
print(" Depth Matrix: ", depth_matrix)

# save to csv file
savetxt('Depth_Matrix.csv', depth_matrix, delimiter=' ')











