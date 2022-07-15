from rest_framework import status
from rest_framework.exceptions import APIException

class ListCreateServiceException(APIException):
    default_code = 'service unavailable'
    default_detail = 'something went wrong while connecting'
    status_code = status.HTTP_400_BAD_REQUEST