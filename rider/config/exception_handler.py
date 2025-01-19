import logging

from rest_framework.views import exception_handler
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from rider.config.response import ErrorResponse


error_logger = logging.getLogger("error_logger")
request_logger = logging.getLogger("request_logger")


class CustomExceptionHandler(object):
    """
    Custom Exception Handler
    """

    def __new__(self, exc, context):
        request_data = {}
        request_data["data"] = context.get("request")._data
        request_data["query"] = context.get("request").query_params.dict()
        request_logger.info(str(request_data))
        response = exception_handler(exc, context)
        error_logger.error(exc)
        if response is not None:
            if response.status_code == HTTP_401_UNAUTHORIZED:
                message = "Unauthorized: Access is denied."
            elif response.status_code == HTTP_403_FORBIDDEN:
                return ErrorResponse(
                    status_code=HTTP_401_UNAUTHORIZED, message=str(exc)
                )
            else:
                try:
                    message = str(exc.detail.get("non_field_errors")[0])
                except Exception as e:
                    error_logger.error(e)
                    message = str(exc)
            return ErrorResponse(
                status_code=response.status_code, message=message
            )
        return ErrorResponse(
            message="Server is facing technical"
            + " difficulties, Please try after some time.",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
