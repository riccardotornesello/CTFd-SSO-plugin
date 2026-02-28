from wtforms import StringField, FileField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Optional
from wtforms.widgets.html5 import ColorInput

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class OAuthClientCreationForm(BaseForm):
    # Display
    alias = StringField("Alias (ID)", validators=[Optional()])
    name = StringField("Display name", validators=[InputRequired()])
    text_color = StringField("Button text color", widget=ColorInput(), default="#ffffff")
    background_color = StringField("Button background color", widget=ColorInput(), default="#808080")
    icon = FileField("Button icon", description="PNG image for the login button")
    display_order = IntegerField("Display order", validators=[Optional()], default=0)

    # OAuth2 Settings
    use_discovery = BooleanField("Use discovery endpoint", default=False)
    discovery_url = StringField("Discovery endpoint URL", validators=[Optional()])
    authorize_url = StringField("Authorization URL", validators=[Optional()])
    access_token_url = StringField("Token URL", validators=[Optional()])
    api_base_url = StringField("User info URL", validators=[Optional()])
    client_id = StringField("Client ID", validators=[InputRequired()])
    client_secret = StringField("Client secret", validators=[InputRequired()])
    scope = StringField(
        "Scope",
        validators=[Optional()],
        default="profile roles openid email",
        description="Space separated list of scopes",
    )

    # Profile Claims
    id_claim = StringField("ID claim", validators=[Optional()], default="sub")
    username_claim = StringField("Username claim", validators=[Optional()], default="preferred_username")
    username_from_email = BooleanField("Derive username from email", default=False)
    email_claim = StringField("Email claim", validators=[Optional()], default="email")
    name_claim = StringField("Name claim", validators=[Optional()], default="name")
    given_name_claim = StringField("Given name claim", validators=[Optional()], default="given_name")
    family_name_claim = StringField("Family name claim", validators=[Optional()], default="family_name")

    submit = SubmitField("Add")


class OAuthClientUpdateForm(OAuthClientCreationForm):
    submit = SubmitField("Update")
