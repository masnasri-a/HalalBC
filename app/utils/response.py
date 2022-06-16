""" response function """

from typing import Any
from fastapi import Response, status


def response_detail(status_code:int, data:Any, response:Response):
    """ response detail """
    message = 'success'
    if status_code != 200:
        response.status_code = status.HTTP_400_BAD_REQUEST
        message = 'failed'
    else:
        response.status_code = status.HTTP_200_OK
    return {'message':message, 'data':data}
