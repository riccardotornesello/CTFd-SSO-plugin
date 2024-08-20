from wtforms import StringField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class OAuthClientCreationForm(BaseForm):
    name = StringField("Client name", validators=[InputRequired()])
    client_id = StringField("OAuth client id", validators=[InputRequired()])
    client_secret = StringField("OAuth client secret", validators=[InputRequired()])
    access_token_url = StringField("Access token url", validators=[InputRequired()])
    authorize_url = StringField("Authorization url", validators=[InputRequired()])
    api_base_url = StringField("User info url", validators=[InputRequired()])
    scope = StringField("Scope", validators=[InputRequired()], default="profile roles openid email", description="Space separated list of scopes")
    submit = SubmitField("Add")
