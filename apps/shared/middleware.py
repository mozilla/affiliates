class ExceptionLoggingMiddleware(object):
    """
    Small middleware that logs exceptions to the console. Useful in local
    development.
    """
    def process_exception(self, request, exception):
        import traceback
        print traceback.format_exc()


class PrivacyMiddleware(object):
    """Adds P3P policy headers to responses."""
    def process_response(self, request, response):
        response['P3P'] = 'CP="This is not a P3P policy!"'
        return response
