import string

from django.utils.crypto import get_random_string


def dash_sep(_string, n=4):
    """
    adds a `-` to the `string` parameter for every
    character count denoted by `n`
    """
    new_str = ""
    for index, s in enumerate(_string):
        if index and not index % n:
            new_str += "-"
        new_str += s

    return new_str


def generate_ref_no(amount=8):
    """generates random characters `amount` number of times"""
    return f"{get_random_string(amount, string.ascii_lowercase)}"


def generate_random_colour():
    """generate random colours"""
    hexnum = get_random_string(6, "0123456789abcdef").lower()
    return f"#{hexnum}"
