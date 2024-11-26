import unittest
from unittest.mock import patch
from message_rating_function import predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    @patch("message_rating_function.SomeModel")
    def test1_get_norm(self, mock_model):
        mock_model.return_value.predict.return_value = 0.5
        result = predict_message_mood("text", 0.3, 0.8)
        self.assertEqual(result, "норм")

    @patch("message_rating_function.SomeModel")
    def test1_2_get_norm(self, mock_model):
        mock_model.return_value.predict.return_value = -7
        result = predict_message_mood("text", -10, -5)
        self.assertEqual(result, "норм")

    @patch("message_rating_function.SomeModel")
    def test1_3_equal_bad_threasholds_get_norm(self, mock_model):
        mock_model.return_value.predict.return_value = 4
        result = predict_message_mood("text", 4, 8)
        self.assertEqual(result, "норм")

    @patch("message_rating_function.SomeModel")
    def test2_get_otl(self, mock_model):
        mock_model.return_value.predict.return_value = 0.9
        result = predict_message_mood("message", 0.3, 0.8)
        self.assertEqual(result, "отл")

    @patch("message_rating_function.SomeModel")
    def test2_2_equal_good_threasholds_get_otl(self, mock_model):
        mock_model.return_value.predict.return_value = 1
        result = predict_message_mood("message", 0.6, 1)
        self.assertEqual(result, "отл")

    @patch("message_rating_function.SomeModel")
    def test3_get_neud(self, mock_model):
        mock_model.return_value.predict.return_value = 0.2
        result = predict_message_mood("paper", 0.3, 0.8)
        self.assertEqual(result, "неуд")

    def test4_bad_thresholds_greater_than_good(self):
        with self.assertRaises(ValueError):
            predict_message_mood("text", 0.9, 0.5)

    @patch("message_rating_function.SomeModel")
    def test_edge_just_above_bad_threshold(self, mock_model):
        mock_model.return_value.predict.return_value = 0.3000000000000000000001
        result = predict_message_mood("text", 0.3, 0.8)
        self.assertEqual(result, "норм")

    @patch("message_rating_function.SomeModel")
    def test_edge_just_below_good_threshold(self, mock_model):
        # 0.7999999999999999999999 -> 0.8
        mock_model.return_value.predict.return_value = 0.7999999999999999999999
        result = predict_message_mood("text", 0.3, 0.8)
        self.assertEqual(result, "отл")

    @patch("message_rating_function.SomeModel")
    def test_edge_just_above_good_threshold(self, mock_model):
        mock_model.return_value.predict.return_value = 0.8000000000000000000001
        result = predict_message_mood("text", 0.3, 0.8)
        self.assertEqual(result, "отл")

    @patch("message_rating_function.SomeModel")
    def test_edge_just_below_bad_threshold(self, mock_model):
        # 0.2999999999999999999999 -> 0.3
        mock_model.return_value.predict.return_value = 0.2999999999999999999999
        result = predict_message_mood("text", 0.3, 0.8)
        self.assertEqual(result, "норм")
