import tkinter as tk
from gui import PDFCompilerGUI
import threading
import http.server
import socketserver

def start_http_server():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"PDF Compiler is running!")

    port = 8080
    handler = Handler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.daemon = True
    server_thread.start()

    # Start the GUI
    root = tk.Tk()
    app = PDFCompilerGUI(root)
    root.mainloop()
