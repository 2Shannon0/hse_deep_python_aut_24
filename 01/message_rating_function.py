# pylint: disable=too-few-public-methods
import random


class SomeModel:
    def __init__(self, input_i):
        self.input = input_i

    def predict(self, message: str = None) -> float:
        return random.random()*len(message)


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8
) -> str:
    if bad_thresholds > good_thresholds:
        raise ValueError(
            "Порог bad_thresholds не может быть больше good_thresholds"
        )
    model = SomeModel(message)
    predict = model.predict(message)
    if predict < bad_thresholds:
        return "неуд"
    if predict >= good_thresholds:
        return "отл"
    return "норм"
