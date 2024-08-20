from wtforms import StringField, FileField
from wtforms.validators import InputRequired
from wtforms.widgets.html5 import ColorInput

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class OAuthClientCreationForm(BaseForm):
    name = StringField("Client name", validators=[InputRequired()])
    client_id = StringField("OAuth client id", validators=[InputRequired()])
    client_secret = StringField("OAuth client secret", validators=[InputRequired()])
    access_token_url = StringField("Access token url", validators=[InputRequired()])
    authorize_url = StringField("Authorization url", validators=[InputRequired()])
    api_base_url = StringField("User info url", validators=[InputRequired()])
    scope = StringField(
        "Scope",
        validators=[InputRequired()],
        default="profile roles openid email",
        description="Space separated list of scopes",
    )

    text_color = StringField("Button txt color", widget=ColorInput(), default="#ffffff")
    background_color = StringField("Button background color", widget=ColorInput(), default="#808080")
    icon = FileField("Button icon")

    submit = SubmitField("Add")
