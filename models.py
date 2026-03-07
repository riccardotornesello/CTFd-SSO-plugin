from authlib.integrations.flask_client import OAuth
from sqlalchemy import Column, String, Integer, Boolean

from CTFd.models import db, Files

from flask import url_for


class OAuthClient(db.Model):
    __tablename__ = "oauth_clients"

    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    text_color = Column(String(255))
    background_color = Column(String(255))
    icon = Column(String(255))
    display_order = Column(Integer)

    authorize_url = Column(String(255))
    access_token_url = Column(String(255))
    user_info_url = Column(String(255))
    client_id = Column(String(255))
    client_secret = Column(String(255))
    scope = Column(String(255))

    username_claim = Column(String(255))
    email_claim = Column(String(255))
    server_metadata_url = Column(String(255))

    def register(self, oauth: OAuth):
        oauth.register(
            name=self.id,
            authorize_url=self.authorize_url,
            access_token_url=self.access_token_url,
            userinfo_endpoint=self.user_info_url,
            server_metadata_url=self.server_metadata_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            client_kwargs={"scope": self.scope},
        )

    def update(self, oauth: OAuth):
        self.disconnect(oauth)
        self.register(oauth)

    def disconnect(self, oauth: OAuth):
        oauth._registry.pop(self.id, None)
        oauth._clients.pop(self.id, None)

    def get_icon(self):
        if not self.icon:
            return None

        f = Files.query.filter_by(id=self.icon).first()
        if not f:
            return None

        return url_for("views.files", path=f.location)
