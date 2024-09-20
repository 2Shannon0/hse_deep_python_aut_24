import unittest
from index import predict_message_mood

class TestPredictMassageMood(unittest.TestCase):
    def test1_get_norm(self):
        result = predict_message_mood("text", 0.3, 0.8, 1)
        expected_result = 'норм'
        self.assertEqual(result, expected_result)

    def test2_get_otl(self):
        result = predict_message_mood("massage", 0.2, 0.7, 2)
        expected_result = 'отл'
        self.assertEqual(result, expected_result)

    def test3_get_neud(self):
        result = predict_message_mood("paper", 0.5, 0.9, 3)
        expected_result = 'неуд'
        self.assertEqual(result, expected_result)

    def test4_predict_eq2_bad_thresholds(self):
        result = predict_message_mood("article", 0.5, 0.9, 4)
        expected_result = 'норм'
        self.assertEqual(result, expected_result)

    def test5_predict_eq2_good_thresholds(self):
        result = predict_message_mood("Чапаев и пустота", 0.5, 0.9, 5)
        expected_result = 'отл'
        self.assertEqual(result, expected_result)

    def test6_bad_thresholds_greater_than_good(self):
        with self.assertRaises(ValueError) as context:
            predict_message_mood("Чапаев и пустота", 0.9, 0.5, 5)  
        
