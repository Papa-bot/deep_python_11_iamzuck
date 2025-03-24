import unittest
from unittest import mock

from message import predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    @mock.patch("message.SomeModel.predict")
    def test_bad_mood_low_limit(self, mock_predict):
        mock_predict.return_value = 0.0
        self.assertEqual("неуд", predict_message_mood("test"))

    @mock.patch("message.SomeModel.predict")
    def test_bad_mood(self, mock_predict):
        mock_predict.return_value = 0.2
        self.assertEqual("неуд", predict_message_mood("test"))

    @mock.patch("message.SomeModel.predict")
    def test_normal_mood_low_limit(self, mock_predict):
        mock_predict.return_value = 0.3
        self.assertEqual("норм", predict_message_mood("test"))

    @mock.patch("message.SomeModel.predict")
    def test_normal_mood(self, mock_predict):
        mock_predict.return_value = 0.5
        self.assertEqual("норм", predict_message_mood("test"))

    @mock.patch("message.SomeModel.predict")
    def test_normal_mood_upper_limit(self, mock_predict):
        mock_predict.return_value = 0.8
        self.assertEqual("норм", predict_message_mood("test"))

    @mock.patch("message.SomeModel.predict")
    def test_good_mood(self, mock_predict):
        mock_predict.return_value = 0.9
        self.assertEqual("отл", predict_message_mood("test"))

    @mock.patch("message.SomeModel.predict")
    def test_good_mood_upper_limit(self, mock_predict):
        mock_predict.return_value = 1.0
        self.assertEqual("отл", predict_message_mood("test"))

    @mock.patch("message.SomeModel.predict")
    def test_custom_thresholds(self, mock_predict):
        mock_predict.return_value = 0.85
        self.assertEqual("норм", predict_message_mood("test", 0.8, 0.99))

    @mock.patch("message.SomeModel.predict")
    def test_wrong_type(self, mock_predict):  # pylint: disable=unused-argument
        with self.assertRaises(TypeError):
            predict_message_mood(123)
