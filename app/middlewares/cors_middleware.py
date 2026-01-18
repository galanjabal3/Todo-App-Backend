import falcon

class CORSMiddleware:
    def process_request(self, req, resp):
        if req.method == 'OPTIONS':
            resp.status = falcon.HTTP_200
            resp.complete = True

    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', 'http://localhost:8080')
        resp.set_header(
            'Access-Control-Allow-Headers',
            'Authorization, Content-Type'
        )
        resp.set_header(
            'Access-Control-Allow-Methods',
            'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        )
        resp.set_header('Access-Control-Allow-Credentials', 'true')
