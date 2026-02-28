from flask import request

from CTFd.utils.uploads import upload_file


def get_request_form_data() -> dict:
    request_data = {
        "name": request.form["name"],
        "client_id": request.form["client_id"],
        "client_secret": request.form["client_secret"],
        "access_token_url": request.form["access_token_url"],
        "authorize_url": request.form["authorize_url"],
        "user_info_url": request.form["user_info_url"],
        "scope": request.form["scope"],
        "text_color": request.form.get("text_color"),
        "background_color": request.form.get("background_color"),
        "icon": request.files.get("icon"),
    }

    if request_data["icon"]:
        f = upload_file(file=request_data["icon"])
        request_data["icon"] = f.id
    else:
        request_data["icon"] = None

    return request_data
