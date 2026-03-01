from ..models import OAuthClient


def get_oauth_clients():
    return OAuthClient.query.order_by(OAuthClient.display_order).all()


def get_oauth_client(client_id) -> OAuthClient | None:
    return OAuthClient.query.filter_by(id=client_id).first()
