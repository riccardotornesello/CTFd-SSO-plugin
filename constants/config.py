from CTFd.constants import JinjaEnum, RawEnum


@JinjaEnum
class SsoRegistrationTypes(str, RawEnum):
    WHEN_ENABLED = "when_enabled"
    ALWAYS = "always"
    NEVER = "never"


SSO_ALLOW_REGISTRATION_KEY = "sso_allow_registration"
SSO_VERIFY_USERS_KEY = "sso_verify_users"

DEFAULT_SSO_ALLOW_REGISTRATION = SsoRegistrationTypes.WHEN_ENABLED
DEFAULT_SSO_VERIFY_USERS = True
