from flask import request

from CTFd.utils.uploads import upload_file

from ..forms.client import OAuthClientCreationForm


def get_request_form_data() -> dict:
    icon = request.files.get("icon")
    if icon:
        f = upload_file(file=icon)
        icon = f.id
    else:
        icon = None

    data = {**OAuthClientCreationForm(request.form).data, "icon": icon}
    data.pop("submit", None)
    data.pop("csrf_token", None)
    data.pop("nonce", None)
    return data
