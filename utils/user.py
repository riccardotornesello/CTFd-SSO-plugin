from CTFd.models import Users

from ..models import OAuthClient
from ..constants.settings import MAX_USERNAME_RETRIES


def generate_username(user_info: dict, client: OAuthClient) -> str:
    """
    Generate a username using the chosen claim from the API data.
    If the claim is not defined, use the email field.
    Since the username can't be an email, remove the @ and everything after it.
    If the username is already taken, append a number to the end of it.
    """

    if client.username_claim and client.username_claim != "":
        retrieved_user_name = user_info.get(client.username_claim, None)
    else:
        retrieved_user_name = user_info["email"].split("@")[0]

    if (
        not retrieved_user_name
        or not isinstance(retrieved_user_name, str)
        or len(retrieved_user_name) == 0
    ):
        raise Exception("Username not found in user info")

    # If the username is already taken, append a number to the end of it.
    i = 1
    user_name = retrieved_user_name
    while Users.query.filter_by(name=user_name).first():
        user_name = retrieved_user_name + str(i)
        i += 1

        # If we can't generate a unique username after amy tries, something is wrong.
        if i > MAX_USERNAME_RETRIES:
            raise Exception("Could not generate a unique username")

    return user_name
