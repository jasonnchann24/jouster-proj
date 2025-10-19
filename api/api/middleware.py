import sys
import traceback
from django.http import JsonResponse
from django.conf import settings


class ForceJSONResponseMiddleware:
    """
    Middleware to force JSON responses for all errors, even in DEBUG mode
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Convert 404 and other error responses to JSON
        if response.status_code >= 400:
            # Check if response is already JSON
            content_type = response.get("Content-Type", "")
            if "application/json" not in content_type:
                # Convert HTML error to JSON
                error_messages = {
                    404: "Not Found",
                    403: "Forbidden",
                    400: "Bad Request",
                    401: "Unauthorized",
                    405: "Method Not Allowed",
                    500: "Internal Server Error",
                }

                return JsonResponse(
                    {
                        "error": error_messages.get(response.status_code, "Error"),
                        "detail": "The requested resource was not found."
                        if response.status_code == 404
                        else f"HTTP {response.status_code} error occurred.",
                        "path": request.path,
                        "status_code": response.status_code,
                    },
                    status=response.status_code,
                )

        return response

    def process_exception(self, request, exception):
        """
        Catch all exceptions and return JSON
        """
        if settings.DEBUG:
            # In debug mode, include detailed traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            return JsonResponse(
                {
                    "error": exc_type.__name__,
                    "detail": str(exception),
                    "traceback": traceback.format_exc().split("\n"),
                    "path": request.path,
                },
                status=500,
            )
        else:
            # In production, don't expose details
            return JsonResponse(
                {
                    "error": "Internal Server Error",
                    "detail": str(exception),
                    "path": request.path,
                },
                status=500,
            )


class CleanRequestBodyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Access request.body here before DRF
        return self.get_response(request)
