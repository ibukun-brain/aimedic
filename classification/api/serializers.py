# import threading
from rest_framework import serializers

# from django_q.tasks import async_task, result
from aimedic.utils.choices import (
    SerializerChestPainTypeChoices,
    SerializerECGChoices,
    SerializerExangChoices,
    SerializerFastingBloodSugarChoices,
    SerializerGenderChoices,
    SerializerSlopeChoices,
    SerializerThalassemiaChoices,
)
from classification.utils.heart_disease import HeartDisease


class HeartClassificationSerializer(serializers.Serializer):
    age = serializers.IntegerField(help_text="age of the person (in years)")
    sex = serializers.ChoiceField(
        choices=SerializerGenderChoices.choices,
        help_text="gender of the person (1 = male; 0 = female)",
    )
    chest_pain_type = serializers.ChoiceField(
        choices=SerializerChestPainTypeChoices.choices,
    )
    resting_bp = serializers.FloatField(
        help_text="blood pressure while resting "
        + "(in mm Hg on admission to the hospital)"
    )
    cholesterol = serializers.FloatField(
        help_text="A person's serum cholesterol in mg/dl"
    )
    fasting_blood_sugar = serializers.ChoiceField(
        choices=SerializerFastingBloodSugarChoices.choices,
        help_text="Blood sugar while fasting & [ > 120 mg/dl ] (1 = true; 0 = false)",
    )
    restecg = serializers.ChoiceField(choices=SerializerECGChoices.choices)
    max_hr = serializers.FloatField(help_text="Maximum heart rate achieved")
    exang = serializers.ChoiceField(
        choices=SerializerExangChoices.choices,
        help_text="Exercise-induced angina (AP) is a common complaint of cardiac "
        + "patients, particularly when exercising in the cold. It usually happens "
        + "during activity (exertion) and goes away with rest or angina medication."
        + "For example, pain, when walking uphill or in cold weather, maybe angina."
        + "Stable angina pain is predictable and usually similar to previous episodes"
        + "of chest pain.",
    )
    oldpeak = serializers.FloatField(
        help_text="ST depression induced by exercise relative to rest"
        + "Exercise-induced ST segment depression is considered a reliable ECG"
        + "finding for the diagnosis of obstructive coronary atherosclerosis."
        + "ST-segment depression is believed as a common electrocardiographic"
        + "sign of myocardial ischemia during exercise testing. Ischemia is generally"
        + "defined as oxygen deprivation due to reduced perfusion."
        + "ST segment depression less than 0.5 mm is accepted in all leads. "
        + "ST segment depression 0.5 mm or more is considered pathological."
    )
    slope = serializers.ChoiceField(
        choices=SerializerSlopeChoices.choices,
    )
    num_major_vessels = serializers.IntegerField(
        min_value=0,
        max_value=3,
        help_text="no. of major vessels (0-3) colored by flourosopy",
    )
    thalassemia = serializers.ChoiceField(
        choices=SerializerThalassemiaChoices.choices,
        help_text="People with thalassemia can get too much iron in their bodies,"
        + "either from the disease or from frequent blood transfusions. "
        + "Too much iron can result in damage to your heart, liver,"
        + "& endocrine system which includes hormone-producing glands"
        + "that regulate processes throughout your body.",
    )

    def create(self, validated_data):
        # dataset = list(map(str, validated_data.values()))
        dataset = [str(value) for value in validated_data.values()]
        # thread = threading.Thread(
        #     target=heart_disease_classifier_task,
        #     # daemon=True
        # )
        # result = thread.start()
        # result = thread.join()
        # task = async_task(self.heart_disease_classifier_task)
        # task_result = result(task, 10000)
        # # print(result)
        # classifier = HeartDisease(63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1)
        classifier = HeartDisease(dataset)
        # classifier = HeartDisease(
        #     validated_data.get("age"),
        #     validated_data.get("sex"),
        #     validated_data.get("chest_paint_type"),
        #     validated_data.get
        # )
        prediction = classifier.get_value()
        output_map = {
            "1": "probably have high risk of heart disease",
            "0": "probably does not have high risk of heart disease",
        }
        result = output_map.get(prediction)
        return {
            "result": result,
        }
