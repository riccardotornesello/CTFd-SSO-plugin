from wtforms import StringField, FileField, IntegerField
from wtforms.validators import InputRequired, Optional
from wtforms.widgets.html5 import ColorInput

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class OAuthClientCreationForm(BaseForm):
    # Display
    id = StringField(
        "Key (Unique)",
        validators=[
            InputRequired(),
        ],
    )  # TODO: validate format and uniqueness of the key.
    name = StringField(
        "Display name",
        validators=[InputRequired()],
    )
    text_color = StringField(
        "Button text color",
        widget=ColorInput(),
        default="#ffffff",
    )
    background_color = StringField(
        "Button background color",
        widget=ColorInput(),
        default="#808080",
    )
    icon = FileField("Button icon", description="PNG image for the login button")
    display_order = IntegerField(
        "Display order",
        validators=[Optional()],
        default=0,
    )

    # OAuth2 Settingsì
    authorize_url = StringField(
        "Authorization URL",
        validators=[InputRequired()],
    )
    access_token_url = StringField(
        "Token URL",
        validators=[InputRequired()],
    )
    user_info_url = StringField(
        "User info URL",
        validators=[InputRequired()],
    )
    server_metadata_url = StringField(
        "OpenID Configuration URL",
        validators=[InputRequired()],
    )
    client_id = StringField(
        "Client ID",
        validators=[InputRequired()],
    )
    client_secret = StringField(
        "Client secret",
        validators=[InputRequired()],
    )
    scope = StringField(
        "Scope",
        validators=[InputRequired()],
        default="profile email",  # TODO: allow custom scopes and add openid if the user wants to use that protocol.
        description="Space separated list of scopes",
    )

    # Profile Claims
    username_claim = StringField(
        "Username claim",
        validators=[Optional()],
        default="preferred_username",
    )
    email_claim = StringField(
        "Email claim",
        validators=[InputRequired()],
        default="email",
    )

    submit = SubmitField("Add")


class OAuthClientUpdateForm(OAuthClientCreationForm):
    submit = SubmitField("Update")
