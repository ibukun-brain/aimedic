import requests
from aimedic.utils.env_variable import get_env_variable


def get_img_prediction(image_url: str) -> str:
    # local variables
    endpoint_url = "https://api.autogon.ai/api/v1/label/model/predict/"
    app_id = get_env_variable("AUTOGONAI_IMAGE_DETECTION_APP_ID")
    img_url = [image_url]
    model_name = "herm_model_2"
    confidence_thresh = 0.3
    overlap_tresh = 0.5
    # body
    body = {
        "app_id": app_id,
        "image_urls": img_url,
        "model_name": model_name,
        "confidence_tresh": confidence_thresh,
        "overlap_tresh": overlap_tresh,
    }

    # auth params
    header = {"X-Aug-Key": get_env_variable("AUTOGONAI_API_KEY")}

    # request part
    try:
        # request to get the model's prediction for the image
        model_response = requests.post(
            url=endpoint_url, json=body, headers=header
        ).json()

        if model_response["status"]:
            # Extract all the labels only either "yes" or "no"
            labels = [
                (label["lbl"], label["conf"])
                for labels in model_response["annotations"].values()
                for label in labels
            ]

            # filter the result, if there is any yes with confidence level greater than
            # or equal to set threshold,
            filtered = list(
                filter(lambda x: x[0] == "yes" and x[1] >= confidence_thresh, labels)
            )

            if bool(filtered):
                return "Hemorrhage Detected"

            else:
                return "Hemorrhage Not Detected"

    # handling exceptions if any
    except Exception as e:
        raise e
