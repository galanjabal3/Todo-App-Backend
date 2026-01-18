from pony.orm import db_session
from app.utils.logger import logger

class PonyDbSessionMiddleware:

    def process_request(self, req, resp):
        # open transaction
        db_session.__enter__()

    def process_response(self, req, resp, resource, req_succeeded):
        # commit / rollback
        try:
            if req_succeeded:
                db_session.__exit__(None, None, None)
            else:
                db_session.__exit__(Exception, Exception("Request failed"), None)
        except Exception:
            logger.exception("Error closing db_session")
            raise
