import http.server
import json
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == "/api/save":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse the incoming JSON data
                data = json.loads(post_data.decode('utf-8'))
                
                # Write to portfolio-data.js
                js_content = f"// Centralized Portfolio Database\n// This file is loaded by the website and can be edited using admin.html\n\nconst PORTFOLIO_DATA = {json.dumps(data, indent=2)};\n"
                
                js_path = os.path.join(DIRECTORY, "portfolio-data.js")
                with open(js_path, "w", encoding="utf-8") as f:
                    f.write(js_content)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "Saved successfully!"}).encode('utf-8'))
                print("[Server] portfolio-data.js saved successfully via Admin Panel.")
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                print(f"[Server] Error saving portfolio data: {e}")
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    # Ensure correct working directory
    os.chdir(DIRECTORY)
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    print(f"\n========================================================")
    print(f" SADAK PORTFOLIO LOCAL DEVELOPMENT SERVER")
    print(f"========================================================")
    print(f" Running at: http://localhost:{PORT}")
    print(f" Open http://localhost:{PORT}/index.html to view website")
    print(f" Open http://localhost:{PORT}/admin.html to edit portfolio!")
    print(f" Press Ctrl+C to stop the server.")
    print(f"========================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        sys.exit(0)
