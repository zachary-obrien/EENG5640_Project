import unittest

import image_compare
import numpy as np

fake_left_image = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]])

fake_right_image = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]])

bad_fake_right_image = np.array([[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]])

class Testing(unittest.TestCase):
    def test_positive_image_compatability(self):
        """
        testing the validation of images
        """
        result = image_compare.image_compatability(fake_left_image, fake_right_image)
        self.assertTrue(result)
    def test_negative_image_compatability(self):
        """
        testing the validation of images
        """
        result = image_compare.image_compatability(fake_left_image, bad_fake_right_image)
        self.assertFalse(result)
    def test_fetch_image_basic(self):
        img = image_compare.fetch_image_array("StereoImageProcessingFlowchart.png")
        self.assertIsNotNone(img)

    def test_get_min_col(self):
        row = 5
        column = 1
        buffered_left_image = np.pad(fake_left_image, pad_width=1, mode='edge')
        buffered_right_image = np.pad(fake_right_image, pad_width=1, mode='edge')
        point_matrix = buffered_left_image[row:row + 3, column:column + 3]
        row_matrix = buffered_right_image[row:row + 3, :]
        found_col, score = image_compare.get_min_col(point_matrix, row_matrix)
        self.assertEqual(found_col, 5)

    def test_get_similar_point(self):
        result_y, result_x = image_compare.get_similar_point(fake_left_image, fake_right_image, 5, 1)
        self.assertEqual(result_y, 5)
        self.assertEqual(result_x, 5)

if __name__ == '__main__':
    unittest.main()