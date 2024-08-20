from wtforms import SelectField

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField

from ..constants.config import SsoRegistrationTypes


class OAuthGlobalSettingsForm(BaseForm):
    allow_registration = SelectField(
        "Allow registration",
        description="Control whether users can register through SSO",
        choices=[
            (SsoRegistrationTypes.WHEN_ENABLED, "When registration is globally enabled"),
            (SsoRegistrationTypes.ALWAYS, "Always (even if registration is disabled)"),
            (SsoRegistrationTypes.NEVER, "Never, only if already registered"),
        ],
        default=SsoRegistrationTypes.WHEN_ENABLED,
    )
    submit = SubmitField("Save")
