class ExceptionLoggingMiddleware(object):
    """
    Small middleware that logs exceptions to the console. Useful in local
    development.
    """
    def process_exception(self, request, exception):
        import traceback
        print traceback.format_exc()
