import random

class SomeModel:
    def __init__(self, input):
        self.input = input

    def predict(self, message: str = None, testNumber: int = None ) -> float:
        if message is None:
            message = self.input
        
        values = {
            1: 0.5,
            2: 0.8,
            3: 0.2,
            4: 0.5,
            5: 0.9
        }
        # в зависимости от номера теста выберем занчение для return
        if testNumber is not None:
            return values[testNumber]
        
        return random.random()


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
    testNumber: int = None
) -> str:
    if bad_thresholds > good_thresholds:
        raise ValueError("Порог bad_thresholds не может быть больше good_thresholds")
    model = SomeModel(message)
    predict = model.predict(message, testNumber)
    if predict < bad_thresholds:
        return "неуд"
    elif predict >= good_thresholds:
        return "отл"
    else:
        return "норм"
