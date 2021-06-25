from uuid import UUID

TEST_EMAIL = "TEST-EMAIL"
TEST_PASSWORD = "TEST-PASSWORD"
TEST_ENCR_PWD = "TEST-ENCR-PWD"
TEST_RESET_CODE = "TEST-RESET-CODE"
TEST_VALIDATION_CODE = "TEST_VALIDATION_CODE"
TEST_AUTHENTICATION_URL = "TEST_AUTHENTICATION_URL"

TEST_DOCUMENT_NAME = "TEST_DOCUMENT_NAME"
TEST_DOCUMENT_ID = "TEST_DOCUMENT_ID"


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


class MockResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def get_json(self):
        return self.content


class StubFromDict:
    def __init__(self, **args):
        for k, v in args.items():
            setattr(self, k, v)
