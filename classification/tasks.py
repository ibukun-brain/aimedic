from classification.utils.heart_disease import HeartDisease


def heart_disease_classifier_task():
    classifier = HeartDisease(63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1)
    prediction = classifier.get_value()
    print(prediction)
    return prediction
    output_map = {
        "1": "probably have high risk of heart disease",
        "0": "probably does not have high risk of heart disease",
    }
    return output_map.get(prediction)
