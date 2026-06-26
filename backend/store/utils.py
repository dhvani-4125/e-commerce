from rest_framework.response import Response

def custom_response(success, message, data=None, status_code=200):
    return Response({
        "status": status_code,
        "success": success,
        "message": message,
        "data": data
    }, status=status_code)