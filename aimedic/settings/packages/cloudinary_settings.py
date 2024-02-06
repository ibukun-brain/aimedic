from aimedic.utils.env_variable import get_env_variable

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": get_env_variable("CLOUDINARY_CLOUD_NAME", "XXXX"),
    "API_KEY": get_env_variable("CLOUDINARY_API_KEY", "XXXX"),
    "API_SECRET": get_env_variable("CLOUDINARY_API_SECRET", "XXXX"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
