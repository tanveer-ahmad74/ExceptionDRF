from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework import status


def get_response(message='', result={}, status=False, status_code=200):
    return dict(message=message, result=result, status=status, status_code=status_code)


def get_error_message(error_dict):
    field = next(iter(error_dict))
    response = error_dict[next(iter(error_dict))]
    if isinstance(response, dict):
        response = get_error_message(response)
    elif isinstance(response, list):
        response_message = response[0]
        if isinstance(response_message, dict):
            response = get_error_message(response_message)
        else:
            response = field + ": " + response[0]
    return response


def handle_exception(exc, context):
    error_response = exception_handler(exc, context)
    if error_response is not None:
        error = error_response.data

        if isinstance(error, list) and error:         # list
            if isinstance(error[0], dict):
                error_response.data = get_response(
                    message=get_error_message(error),
                    status_code=error_response.status_code,
                )

            elif isinstance(error[0], str):              # str
                error_response.data = get_response(
                    message=error[0],
                    status_code=error_response.status_code
                )

        if isinstance(error, dict):                     # dict
            error_response.data = get_response(
                message=get_error_message(error),
                status_code=error_response.status_code
            )
    return error_response


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 500:
            response = get_response(
                message="Internal server error, please try again later",
                status_code=response.status_code
            )
            return JsonResponse(response, status=response['status_code'])

        if response.status_code == 404 and "Page not found" in str(response.content):
            response = get_response(
                message="Page not found, Something went wrong.",
                status_code=response.status_code
            )
            return JsonResponse(response, status=response['status_code'])

        if response.status_code == 401:
            response = get_response(
                message=response.data['message'],
                status_code=response.status_code
            )
            return JsonResponse(response, status=response['status_code'])

        if response.status_code == 400:
            response = get_response(message="Sending wrong data",
                                    status_code=response.status_code)
            return JsonResponse(response, status=response['status_code'])

        # if response.status_code == 403:
        #     response = get_response(message='Not allowed',
        #                             status_code=response.status_code)
        #     return JsonResponse(response, status=response['status_code'])
        # continue with other status if you want to override but don't forget to add middleware in settings
        # and add EXCEPTION_HANDLER in REST_FRAMEWORK.
        return response
