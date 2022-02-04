from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def successful_response(data=None, pagination=None, status_code=status.HTTP_200_OK):
    content = {
        'success': True,
    }
    if data is not None:
        content['data'] = data

    if pagination is not None:
        content['pagination'] = pagination

    return Response(content, status=status_code)


def unsuccessful_response(errors, status_code=status.HTTP_400_BAD_REQUEST):
    content = {
        'success': False,
        'errors': errors
    }
    return Response(content, status=status_code)


def planner_exception_handler(exc, context):
    errors = exception_handler(exc, context)
    return unsuccessful_response(errors=errors.data, status_code=errors.status_code)
