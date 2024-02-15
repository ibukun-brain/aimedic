import requests

from aimedic.utils.env_variable import get_env_variable


class HeartDisease:
    def __init__(self, params):
        self.params = params

    def create_dataset(self):
        # print(list(map(str, self.params)))
        data_body = {
            # "data": list(map(str, self.params))
            "data": self.params
        }  # this line only converts the input parameters\
        # to string data type if they are not already in the string format

        data_url = "https://api.autogon.ai/api/v1/models/generate/"
        try:
            # request to create dataset from input parameters
            data_response = requests.post(url=data_url, json=data_body).json()

        except Exception as e:
            raise Exception(f"Error encountered: {e}") from e

        dataset_url = data_response["data"]
        return dataset_url

    def get_prediction(self):
        dataset_url = self.create_dataset()

        flow_id = get_env_variable("FLOW_ID", "fl-2040f7c80be5438daae1401a238c5c58")
        api_key = get_env_variable(
            "API_KEY", "z509khsH.QVBA5qr8zTzrvuNrWTyxxnNMGjfH9GAS"
        )

        pipe_body = {"flow_id": flow_id, "data": dataset_url}

        header = {"X-Aug-Key": api_key}
        model_url = "https://api.autogon.ai/api/v1/models/production/"

        try:
            # request to get the model's prediction for the created dataset
            model_response = requests.post(
                url=model_url, json=pipe_body, headers=header
            ).json()

        except Exception as e:
            raise Exception(f"Error encountered: {e}") from e

        predicted_url = model_response["pred_url"]
        return predicted_url

    def get_value(self):
        # set prediction values from the result of the prediction
        prediction_url = self.get_prediction()

        if prediction_url is not None:
            try:
                pred_data = requests.get(prediction_url).text
            except Exception as e:
                raise Exception(f"Error encountered : {e}") from e
            pred = pred_data[-2]
            return pred

        raise Exception("prediction url fetch failed")


# if __name__ == "__main__":
#     test_sample = HeartDisease(63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1)
#     user_prediction = test_sample.get_value()

#     output_map = {
#         "1": "probably have high risk of heart disease",
#         "0": "probably does not have high risk of heart disease",
#     }

#     print(f"This user {output_map.get(user_prediction)}")
