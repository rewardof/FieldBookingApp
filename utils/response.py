from rest_framework import status
from rest_framework.response import Response


class FailResponse(Response):
    def __init__(self, *args, **kwargs):
        status_code = kwargs.get('status') or status.HTTP_400_BAD_REQUEST
        data = {
            "status_code": status_code,
            "status": "FAIL",
            "message": kwargs.get("message") or "",
            "error": {
                "code": kwargs.get("code") or "validation_error",
                "path": kwargs.get("path") or ""
            }
        }
        super().__init__(status=status_code, data=data)


class SuccessResponse(Response):
    def __init__(self, *args, **kwargs):
        status_code = kwargs.get('status') or status.HTTP_200_OK
        data = {
            "status_code": status_code,
            "status": "SUCCESS",
            "message": kwargs.get("message") or "",
            "data": kwargs.get("data") or {}
        }
        super().__init__(status=status_code, data=data)
