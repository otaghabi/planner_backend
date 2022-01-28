from rest_framework import status
from rest_framework.response import Response


def successful_response(data=None, status_code=status.HTTP_200_OK):
    content = {
        'success': True,
    }
    if data is not None:
        content['data'] = data

    return Response(content, status=status_code)


def unsuccessful_response(errors, status_code=status.HTTP_400_BAD_REQUEST):
    content = {
        'success': False,
        'errors': errors
    }
    return Response(content, status=status_code)
