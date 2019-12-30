from rest_framework.response import Response as BaseResponse


class Response(BaseResponse):

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None,
                 message=None,):

        response_data = {
            'data': data
        }

        super().__init__(response_data, status=status)
