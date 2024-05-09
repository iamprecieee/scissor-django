from random import choices
import string


def generate_short_url():
    return "".join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
