from aimedic.utils.choices import (
    SerializerFastingBloodSugarChoices,
    SerializerSlopeChoices,
)

SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": "/api",
    "TITLE": "Afrimed API",
    "DESCRIPTION": "The Afrimed aims to revolutionize healthcare in Africa by addressing the severe shortage of Radiologists. Leveraging  AI innovative technology, this solution aids medical image analysis to enhance patient-doctor interactions and provide accurate diagnoses.",
    "VERSION": "Version 0.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "ENUM_NAME_OVERRIDES": {
        "FastingBloodSugarEnum": SerializerFastingBloodSugarChoices.choices,
        "SlopeEnum": SerializerSlopeChoices.choices,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "docExpansion": "none",
        "persistAuthorization": True,
        # "displayOperationId": True,
    },
    "CONTACT": {
        "name": "Afrimed API",
        # "url": "https://foo.com",
        "email": "ibukunolaifa@gmail.com",
    },
    "TAGS": [
        {
            "name": "appointments",
            "description": "Doctors and patients appointments",
        },
        {
            "name": "auth",
            "description": "Patient authentication, this endpoint is available to the doctors as well",
        },
        {
            "name": "chats",
            "description": "patients and doctors chats",
        },
        {
            "name": "classification",
            "description": "AutogonAI health disease classification",
        },
        {"name": "notifications", "description": "Patients and Doctors notifications"},
        {
            "name": "patient",
            "description": "Patient information, contains only patient's doctor endpoint only",
        },
        {"name": "practitioners", "description": "Practitioners information"},
        {"name": "detection", "description": "Image or object detection"},
    ],
}
