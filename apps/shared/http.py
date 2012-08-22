import json

from django.http import HttpResponse


class JSONResponse(HttpResponse):
    def __init__(self, data, status=200):
        data_json = json.dumps(data)
        super(JSONResponse, self).__init__(data_json,
                                           mimetype='application/json',
                                           status=status)
