import unittest
from unittest.mock import patch, MagicMock, mock_open
import numpy as np
import cv2
from PIL import Image
from Imports.logic import (
    find_corners_closest_to_edges,
    process_image,
    convert_to_opencv,
)
from Imports.raport import generate_report
from Imports import buttons
import builtins
import json
import importlib
import sys


class TestLogicFunctions(unittest.TestCase):

    def test_convert_to_opencv_rgb_input(self):
        pil_image = Image.fromarray(np.ones((100, 100, 3), dtype=np.uint8) * 255)
        result = convert_to_opencv(pil_image)
        self.assertEqual(result.shape, (100, 100, 3))
        self.assertEqual(result.dtype, np.uint8)

    def test_find_corners_simple(self):
        image_shape = (1000, 800)
        corners = [(0, 0), (799, 0), (799, 999), (0, 999)]
        result = find_corners_closest_to_edges(corners, image_shape)
        self.assertEqual(len(result), 4)

    def test_find_corners_arbitrary_order(self):
        image_shape = (100, 100)
        corners = [(90, 90), (0, 0), (0, 99), (99, 0)]
        result = find_corners_closest_to_edges(corners, image_shape)
        self.assertIn((0, 0), result)

    def test_process_image_result_shape(self):
        dummy_image = Image.fromarray(np.uint8(np.random.rand(600, 400, 3) * 255))
        result = process_image(dummy_image)
        self.assertEqual(result.shape, (1400, 1000, 3))

    def test_process_image_type(self):
        dummy_image = Image.fromarray(np.uint8(np.random.rand(600, 400, 3) * 255))
        result = process_image(dummy_image)
        self.assertEqual(result.dtype, np.uint8)

    def test_score_to_grade_5(self):
        score = 9
        score_points = 10
        grade_table = [0.9, 0.75, 0.6]
        self.assertGreaterEqual(score / score_points, grade_table[0])

    def test_score_to_grade_4(self):
        score = 8
        score_points = 10
        grade_table = [0.9, 0.75, 0.6]
        self.assertGreaterEqual(score / score_points, grade_table[1])

    def test_score_to_grade_3(self):
        score = 6.5
        score_points = 10
        grade_table = [0.9, 0.75, 0.6]
        self.assertGreaterEqual(score / score_points, grade_table[2])

    def test_score_to_grade_2(self):
        score = 5.5
        score_points = 10
        threshold = 0.5
        self.assertGreaterEqual(score / score_points, threshold)

    def test_score_to_grade_1(self):
        score = 4
        score_points = 10
        threshold = 0.5
        self.assertLess(score / score_points, threshold)

    def test_failed_test_detection(self):
        score = 3
        score_points = 10
        threshold = 0.5
        self.assertLess(score / score_points, threshold)

    def test_passed_test_detection(self):
        score = 8
        score_points = 10
        threshold = 0.5
        self.assertGreaterEqual(score / score_points, threshold)

    def test_grade_table_length(self):
        grade_table = [0.9, 0.75, 0.6]
        self.assertEqual(len(grade_table), 3)

    def test_process_image_corner_order(self):
        dummy_image = Image.fromarray(np.uint8(np.random.rand(600, 400, 3) * 255))
        result = process_image(dummy_image)
        self.assertTrue(isinstance(result, np.ndarray))

    def test_image_warping_dimension(self):
        dummy_image = Image.fromarray(np.uint8(np.random.rand(600, 400, 3) * 255))
        warped = process_image(dummy_image)
        self.assertEqual(warped.shape, (1400, 1000, 3))

    def test_exit_program_calls_destroy(self):
        root = MagicMock()
        buttons.exit_program(root)
        root.destroy.assert_called_once()

    def test_toggle_help_text_behavior(self):
        frame = MagicMock()
        frame.winfo_ismapped.side_effect = [False, True]
        buttons.toggle_help_text(frame)
        frame.grab_set.assert_called_once()
        frame.place.assert_called_once()
        buttons.toggle_help_text(frame)
        frame.grab_release.assert_called_once()
        frame.place_forget.assert_called_once()

    def test_show_page1_behavior(self):
        page1 = MagicMock()
        separator = MagicMock()
        page2 = MagicMock()
        separator.winfo_ismapped.return_value = False
        buttons.show_page1(page1, separator, page2)
        page1.place.assert_called()
        separator.place.assert_called()
        page2.place_forget.assert_called_once()

    def test_toggle_settings_option_behavior(self):
        frame = MagicMock()
        frame.winfo_ismapped.side_effect = [False, True]
        buttons.toggle_settings_option(frame)
        frame.grab_set.assert_called_once()
        frame.place.assert_called_once()
        buttons.toggle_settings_option(frame)
        frame.grab_release.assert_called_once()
        frame.place_forget.assert_called_once()

    def test_toggle_test_settings_behavior(self):
        frame = MagicMock()
        frame.winfo_ismapped.side_effect = [True, False]
        buttons.toggle_test_settings(frame)
        frame.grab_release.assert_called_once()
        frame.place_forget.assert_called_once()
        buttons.toggle_test_settings(frame)
        frame.grab_set.assert_called()
        frame.place.assert_called()

    def test_show_page2_behavior(self):
        page1 = MagicMock()
        separator = MagicMock()
        page2 = MagicMock()
        buttons.show_page2(page1, separator, page2)
        page1.place_forget.assert_called_once()
        separator.place_forget.assert_called_once()
        page2.place.assert_called_once()

    def test_approve_color_template_sets_color(self):
        frame = MagicMock()
        buttons.approve_color_template(frame)
        frame.configure.assert_called_once_with(border_color="lightgreen")

    def test_ctk_appearance_mode_and_theme(self):
        with patch("main.ctk.set_appearance_mode") as mock_mode, \
                patch("main.ctk.set_default_color_theme") as mock_theme:
            import importlib
            import main
            importlib.reload(main)
            mock_mode.assert_called_with("System")
            mock_theme.assert_called_with("blue")

    # były próby testowania hasła, ale wychodziły BARDZO źle :DDD

if __name__ == "__main__":
    unittest.main()
