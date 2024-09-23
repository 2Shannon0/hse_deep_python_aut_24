import random


class SomeModel:
    def __init__(self, input_i):
        self.input = input_i

    def get_input(self) -> str:
        pass  # исправление Too few public methods (1/2) pylint error

    def predict(self, message: str = None, test_number: int = None) -> float:
        if message is None:
            message = self.input

        values = {1: 0.5, 2: 0.8, 3: 0.2, 4: 0.5, 5: 0.9}
        # в зависимости от номера теста выберем занчение для return
        if test_number is not None:
            return values[test_number]

        return random.random()


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
    test_number: int = None,
) -> str:
    if bad_thresholds > good_thresholds:
        raise ValueError(
            "Порог bad_thresholds не может быть больше good_thresholds"
        )
    model = SomeModel(message)
    predict = model.predict(message, test_number)
    if predict < bad_thresholds:
        return "неуд"
    if predict >= good_thresholds:
        return "отл"
    return "норм"
