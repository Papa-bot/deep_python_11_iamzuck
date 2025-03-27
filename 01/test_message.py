import unittest
from unittest import mock

from message import predict_message_mood


class TestPredictMessageMood(unittest.TestCase):

    @mock.patch("message.SomeModel.predict")
    def test_predict_called_with_correct_message(self, mock_predict):
        mock_predict.return_value = 0.5
        message = "hello"
        predict_message_mood(message)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_bad_mood_just_below_threshold(self, mock_predict):
        mock_predict.return_value = 0.2999
        message = "test"
        result = predict_message_mood(message)
        self.assertEqual("неуд", result)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_bad_mood_on_threshold(self, mock_predict):
        mock_predict.return_value = 0.3
        message = "test"
        result = predict_message_mood(message)
        self.assertEqual("норм", result)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_normal_mood_just_above_bad_threshold(self, mock_predict):
        mock_predict.return_value = 0.3001
        message = "test"
        result = predict_message_mood(message)
        self.assertEqual("норм", result)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_normal_mood_just_below_good_threshold(self, mock_predict):
        mock_predict.return_value = 0.7999
        message = "test"
        result = predict_message_mood(message)
        self.assertEqual("норм", result)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_normal_mood_on_good_threshold(self, mock_predict):
        mock_predict.return_value = 0.8
        message = "test"
        result = predict_message_mood(message)
        self.assertEqual("норм", result)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_good_mood_just_above_threshold(self, mock_predict):
        mock_predict.return_value = 0.8001
        message = "test"
        result = predict_message_mood(message)
        self.assertEqual("отл", result)
        mock_predict.assert_called_once_with(message)

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
        message = "test"
        result = predict_message_mood(message)
        self.assertEqual("отл", result)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_bad_mood_lower_limit(self, mock_predict):
        mock_predict.return_value = 0.0
        message = "test"
        result = predict_message_mood(message)
        self.assertEqual("неуд", result)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_custom_threshold_just_under_good(self, mock_predict):
        mock_predict.return_value = 0.849
        message = "test"
        result = predict_message_mood(
            message,
            bad_threshold=0.3,
            good_threshold=0.85)
        self.assertEqual("норм", result)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_custom_threshold_exact_good(self, mock_predict):
        mock_predict.return_value = 0.85
        message = "test"
        result = predict_message_mood(
            message,
            bad_threshold=0.3,
            good_threshold=0.85)
        self.assertEqual("норм", result)
        mock_predict.assert_called_once_with(message)

    @mock.patch("message.SomeModel.predict")
    def test_custom_threshold_just_over_good(self, mock_predict):
        mock_predict.return_value = 0.851
        message = "test"
        result = predict_message_mood(
            message,
            bad_threshold=0.3,
            good_threshold=0.85)
        self.assertEqual("отл", result)
        mock_predict.assert_called_once_with(message)
        self.assertEqual("отл", predict_message_mood("test"))

    @mock.patch("message.SomeModel.predict")
    def test_custom_thresholds(self, mock_predict):
        mock_predict.return_value = 0.85
        self.assertEqual("норм", predict_message_mood("test", 0.8, 0.99))

    @mock.patch("message.SomeModel.predict")
    def test_wrong_type(self, mock_predict):  # pylint: disable=unused-argument
        with self.assertRaises(TypeError):
            predict_message_mood(123)
