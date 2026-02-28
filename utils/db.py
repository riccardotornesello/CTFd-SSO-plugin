from CTFd.models import db

from ..models import OAuthClient, OAuthConfig


def get_oauth_clients():
    return OAuthClient.query.all()


def get_oauth_client(client_id) -> OAuthClient | None:
    return OAuthClient.query.filter_by(id=client_id).first()


def get_all_oauth_config():
    """
    Return an object with the OAuth configuration
    """
    return {config.key: config.value for config in OAuthConfig.query.all()}


def get_oauth_config(key):
    """
    Get the OAuth configuration for a given key
    """
    config = OAuthConfig.query.filter_by(key=key).first()
    return config.value if config else None


def update_oauth_config_key(key, value):
    """
    Update the OAuth configuration for a given key
    """
    config = OAuthConfig.query.filter_by(key=key).first()
    if config:
        config.value = value
    else:
        config = OAuthConfig(key=key, value=value)
        db.session.add(config)
    db.session.commit()
    return config
