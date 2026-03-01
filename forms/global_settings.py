from wtforms import SelectField, BooleanField

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField

from ..constants.config import SsoRegistrationTypes


class OAuthGlobalSettingsForm(BaseForm):
    allow_registration = SelectField(
        "Allow registration",
        description="Control whether new users can register through SSO",
        choices=[
            (SsoRegistrationTypes.WHEN_ENABLED, "Only when registration is globally enabled"),
            (SsoRegistrationTypes.ALWAYS, "Always (even if registration is disabled)"),
            (SsoRegistrationTypes.NEVER, "Never, only if already registered"),
        ],
        default=SsoRegistrationTypes.WHEN_ENABLED,
    )
    verify_users = BooleanField(
        "Automatically verify users",
        description="Automatically mark users as verified when they log in through SSO",
        default=True,
    )

    submit = SubmitField("Save")
