from rest_framework.exceptions import ValidationError, NotAcceptable, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler


def base_exception_handler(exc, context):
    response = exception_handler(exc, context)
    status_code = 400
    code = "validation_error"
    status = "FAIL"
    path = ""

    # check that a ValidationError exception is raised
    message = ""
    if isinstance(exc, ValidationError) or isinstance(exc, NotAcceptable) or isinstance(exc, NotAuthenticated):
        # here prepare the 'custom_error_response' and
        # set the custom response data on response object
        status_code = response.status_code
        if isinstance(response.data, dict):
            code = response.data.get('message').code if response.data.get('message') else "validation_error"
            for key, value in response.data.items():
                message1 = key + ": " if key else ""
                message = _process_value(value, message1)
        if isinstance(response.data, list):
            code = response.data[0].code if response.data[0] else "validation_error"
            message = _process_value(response.data, message)

        path = context['request'].path

    if response is not None:
        status_code = response.status_code
    else:
        if exc and exc.args:
            for value in exc.args:
                message += "%s\n" % ("".join(value) if value and isinstance(value, (tuple, list)) else value)
                status_code = 500
                code = "attribute_error"
    data = {
        "status_code": status_code,
        "status": status,
        "message": message,
        "error": {
            "code": code,
            "path": path
        }
    }
    return Response(data, status=status_code)


def _process_value(value, message1="Message1: ", indent="  "):
    def recursive_process(val, indent_level=0):
        msg = ""
        if isinstance(val, dict):
            for key1, value1 in val.items():
                msg += f"{indent * indent_level}{key1 + ': ' if key1 else ''}"
                if isinstance(value1, (list, tuple)):
                    msg += "\n" + recursive_process(value1, indent_level + 1)
                else:
                    msg += recursive_process(value1, indent_level)
        elif isinstance(val, (list, tuple)):
            msg += "".join([recursive_process(item, indent_level) for item in val])
        else:
            msg += val
        return msg

    message2 = recursive_process(value)
    message = f"{message1}\n{message2}"
    return message
