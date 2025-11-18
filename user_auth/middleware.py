class CustomerHeaderMiddleware:
    """
    Middleware to add a custom header to the request indicating
    whether the user is authenticated as a customer.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            request["X-Django-User"] = str(request.user.email)

        return response