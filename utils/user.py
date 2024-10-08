from CTFd.models import Users, db


def generate_username(api_data: dict) -> str:
    """
    Generate a username using the preferred_username or nickname field from the API data.
    If the preferred_username field is not present, use the email field.
    Since the username can't be an email, remove the @ and everything after it.
    If the username is already taken, append a number to the end of it.
    """

    username_fields = ["preferred_username", "nickname"]

    # Try to get the username from the preferred_username or nickname field.
    for field in username_fields:
        user_name = api_data.get(field, None)
        if user_name:
            break

    # If the username is not present, use the email field.
    if not user_name:
        user_name = api_data["email"].split("@")[0]

    # If the username is already taken, append a number to the end of it.
    i = 1
    while Users.query.filter_by(name=user_name).first():
        user_name = user_name + str(i)
        i += 1

        # If we can't generate a unique username after 100 tries, something is wrong.
        if i > 100:
            raise Exception("Could not generate a unique username")

    return user_name
