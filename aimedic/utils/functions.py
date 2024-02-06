def booleanize(value):
    """
    This function turns statements into booleans

    Returns:
        Boolean: True or False
    """
    returned_value = None
    if value == "on":
        returned_value = True
    elif value == "off":
        returned_value = False
    return returned_value


def get_user_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    # print(x_forwarded_for)
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(",")[0]
        return ip_address
    ip_address = request.META.get("REMOTE_ADDR")
    return ip_address


def get_user_geo_location_city(request):
    pass


def get_user_geo_location_long(request):
    pass


def get_user_geo_location_lat(request):
    pass
