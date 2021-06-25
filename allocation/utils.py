from uuid import UUID


def validate_uuid4(uuid_string):
    """
    Verify if the provided string is a uuid4
    return True or False
    """
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False

    return val.hex == uuid_string.replace("-", "")
