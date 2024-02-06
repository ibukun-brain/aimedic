from pathlib import Path

# from aimedic.utils.settings import get_env_variable

BASE_DIR = Path(__file__).resolve().parent.parent

CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_REQUIRE_STAFF = False
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 400,
        "width": "100%",
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                # your extra plugins here
                # 'Youtube',
                # 'codesnippet',
            ]
        ),
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"

# CKEDITOR_CONFIGS = {
#     "default": {
#         "toolbar": "Custom",
#         "height": 400,
#         "width": "100%",
#         'extraPlugins': ','.join([
#             'uploadimage',  # the upload image feature
#         ]),
#         "toolbar_Custom": [
#             [
#                 "Bold",
#                 "Underline",
#                 "-",
#                 "JustifyLeft",
#                 "JustifyCenter",
#                 "JustifyRight",
#                 "JustifyBlock",
#             ],
#             [
#                 "NumberedList",
#                 "BulletedList",
#                 "-",
#                 "Outdent",
#                 "Indent",
#                 "-",
#                 "RemoveFormat",
#                 "Source",
#             ],
#             [
#                 "Link",
#                 "Unlink",
#                 "-",
#                 "Find",
#                 "Replace",
#                 "-",
#                 "PasteText",
#                 "PasteFromWord",
#             ],
#             ["Cut", "Copy", "Paste", "-", "Undo", "Redo"],
#             ["Format", "Font", "FontSize"],
#         ],
#         "external_plugin_resources": [("youtube", "/assets/js/youtube/", "plugin.js")]
#     },
# }

CKEDITOR_BASEPATH = "/assets/ckeditor/ckeditor/"

# CKEDITOR_UPLOAD_PATH = get_env_variable("MEDIA_ROOT", BASE_DIR / "uploads")

CKEDITOR_ALLOW_NONIMAGE_FILES = False

CKEDITOR_JQUERY_URL = "/assets/libs/jquery/dist/jquery.min.js"

CKEDITOR_IMAGE_BACKEND = "pillow"
