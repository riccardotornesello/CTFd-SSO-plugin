from authlib.integrations.flask_client import OAuth

from CTFd.models import db, Files

from flask import url_for


class OAuthClient(db.Model):
    __tablename__ = "oauth_clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    client_id = db.Column(db.Text)
    client_secret = db.Column(db.Text)
    access_token_url = db.Column(db.Text)
    authorize_url = db.Column(db.Text)
    user_info_url = db.Column(db.Text)
    scope = db.Column(db.Text)

    text_color = db.Column(db.Text, default="#000000")
    background_color = db.Column(db.Text, default="#808080")
    icon = db.Column(db.Text)

    def register(self, oauth: OAuth):
        oauth.register(
            name=self.id,
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url,
            api_base_url=self.user_info_url,
            client_kwargs={"scope": self.scope},
        )

    def update(self, oauth: OAuth):
        self.disconnect(oauth)
        self.register(oauth)

    def disconnect(self, oauth: OAuth):
        oauth._registry.pop(self.id)
        oauth._clients.pop(self.id)

    def get_icon(self):
        if not self.icon:
            return None

        f = Files.query.filter_by(id=self.icon).first()
        if not f:
            return None

        return url_for("views.files", path=f.location)


class OAuthConfig(db.Model):
    __tablename__ = "oauth_config"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text)
    value = db.Column(db.Text)
