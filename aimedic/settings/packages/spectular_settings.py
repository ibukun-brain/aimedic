from aimedic.utils.choices import (
    SerializerFastingBloodSugarChoices,
    SerializerSlopeChoices,
)

SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": "/api",
    "TITLE": "Afrimed API",
    "DESCRIPTION": "The Afrimed aims to revolutionize healthcare in Africa by addressing the severe shortage of Radiologists. Leveraging  AI innovative technology, this solution aids medical image analysis to enhance patient-doctor interactions and provide accurate diagnoses.",
    "VERSION": "0.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "ENUM_NAME_OVERRIDES": {
        "FastingBloodSugarEnum": SerializerFastingBloodSugarChoices.choices,
        "SlopeEnum": SerializerSlopeChoices.choices,
    },
    # 'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        "deepLinking": True,
        # "docExpansion": "none",
    },
}
