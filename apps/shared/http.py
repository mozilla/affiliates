import json

from django.http import HttpResponse


class JSONResponse(HttpResponse):
    status = 200

    def __init__(self, data, status=None):
        data_json = json.dumps(data)
        super(JSONResponse, self).__init__(data_json,
                                           mimetype='application/json',
                                           status=status or self.status)


class JSONResponseBadRequest(JSONResponse):
    status = 400
