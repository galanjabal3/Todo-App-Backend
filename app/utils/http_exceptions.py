import falcon

class CustomHTTPError(falcon.HTTPError):
    """
    Base class for all custom HTTP errors.
    Can include optional internal error code.
    """

    def __init__(
        self,
        status: str,
        title: str,
        msg: str,
        code: str | int | None = None
    ):
        super().__init__(
            code=code,
            status=status,
            title=title,
            description=msg,
        )
        self._message = msg

    def to_dict(self, obj_type=dict):
        """
        Customize Falcon JSON output
        """
        result = super().to_dict(obj_type)
        result["message"] = self._message
        result["code"] = self.code or self.status_code
        return result


# ------------------------------
# Helper functions for common errors
# ------------------------------

def bad_request(title: str = "Bad Request", msg: str = "Bad request"):
    """400 - Bad Request"""
    raise CustomHTTPError(
        status=falcon.HTTP_400,
        title=title,
        msg=msg,
    )

def unauthorized(title: str = "Unauthorized", msg: str = "Unauthorized"):
    """401 - Unauthorized"""
    raise CustomHTTPError(
        status=falcon.HTTP_401,
        title=title,
        msg=msg,
    )

def forbidden(title: str = "Forbidden", msg: str = "Forbidden"):
    """403 - Forbidden"""
    raise CustomHTTPError(
        status=falcon.HTTP_403,
        title=title,
        msg=msg,
    )

def not_found(title: str = "Not Found", msg: str = "Resource not found"):
    """404 - Not Found"""
    raise CustomHTTPError(
        status=falcon.HTTP_404,
        title=title,
        msg=msg,
    )

def conflict(title: str = "Conflict", msg: str = "Conflict"):
    """409 - Conflict"""
    raise CustomHTTPError(
        status=falcon.HTTP_409,
        title=title,
        msg=msg,
    )

def unprocessable(title: str = "Unprocessable Entity", msg: str = "Unprocessable entity"):
    """422 - Unprocessable Entity"""
    raise CustomHTTPError(
        status=falcon.HTTP_422,
        title=title,
        msg=msg,
    )
