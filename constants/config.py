from CTFd.constants import JinjaEnum, RawEnum


@JinjaEnum
class SsoConfigTypes(str, RawEnum):
    SSO_ALLOW_REGISTRATION = "SSO_ALLOW_REGISTRATION"


@JinjaEnum
class SsoRegistrationTypes(str, RawEnum):
    WHEN_ENABLED = "when_enabled"
    ALWAYS = "always"
    NEVER = "never"
