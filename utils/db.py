from CTFd.models import db

from ..models import OAuthClients, OAuthConfig


def get_oauth_clients():
    return OAuthClients.query.all()


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
