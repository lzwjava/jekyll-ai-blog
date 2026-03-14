import http.server
import json
import base64


class CaptureHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        # Capture headers and body to a file
        capture_data = {
            "headers": dict(self.headers),
            "body": post_data.decode("utf-8") if content_length > 0 else "",
        }

        with open("scripts/try/captured_request.json", "w") as f:
            json.dump(capture_data, f, indent=4)

        print(f"\n--- Request Captured ---")
        print(f"Content-Length: {content_length}")

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Captured"}
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        self.do_POST()


if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", 8080), CaptureHandler)
    print("Server starting on http://127.0.0.1:8080...")
    server.handle_request()
