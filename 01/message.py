from message_model import SomeModel


def predict_message_mood(
    message: str,
    bad_threshold: float = 0.3,
    good_threshold: float = 0.8,
) -> str:
    model = SomeModel()
    score = model.predict(message)

    if score < bad_threshold:
        return "неуд"
    if score > good_threshold:
        return "отл"
    return "норм"
