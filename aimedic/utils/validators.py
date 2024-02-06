import os

from django.core.exceptions import ValidationError


class FileValidatorHelper:
    """
    Helper class to validate files
    """

    @staticmethod
    def validate_file_extension(value):
        """
        Checks that we are using a valid file extension
        """

        ext = os.path.splitext(value.name)[1]
        valid_extensions = [".pdf", ".doc", ".docx", ".jpg", ".png", ".xlsx", ".xls"]

        if not ext.lower() in valid_extensions:
            raise ValidationError("pdf,doc,docx,xlsx,xls,jpg and png file supported.")

    @staticmethod
    def validate_image_extension(value):
        """
        Checks that we are using a valid file extension
        """

        ext = os.path.splitext(value.name)[1]
        valid_extensions = [".jpg", ".png", ".jpeg"]

        if not ext.lower() in valid_extensions:
            raise ValidationError("jpg, jpeg and png file supported.")

    @staticmethod
    def validate_file_size(value):
        """
        Checks that file size is not too large
        """
        filesize = value.size

        if filesize > 5242880:
            raise ValidationError("The maximum file size that can be uploaded is 5MB")

        return value

    @staticmethod
    def validate_logo_size(value):
        """
        Checks that logo size is not too large
        """
        filesize = value.size
        if filesize > 2097152:
            raise ValidationError("The maximum file size that can be uploaded is 2MB")

        return value

    @staticmethod
    def validate_logo_extension(value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = [".jpg", ".png", ".jpeg", ".jfif"]

        if not ext.lower() in valid_extensions:
            raise ValidationError("jpg, jpeg, jfif and png file supported.")
