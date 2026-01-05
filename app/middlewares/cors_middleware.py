class CORSMiddleware:
    def process_request(self, req, resp):
        # Handle preflight request
        if req.method == 'OPTIONS':
            resp.status = 200
            return

    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', 'http://localhost:5173')
        resp.set_header(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization'
        )
        resp.set_header(
            'Access-Control-Allow-Methods',
            'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        )
        resp.set_header('Access-Control-Allow-Credentials', 'true')
