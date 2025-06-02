# Framework/Frontend/frontend.py
from flask import Flask, send_file
from flask_cors import CORS
from flask_socketio import SocketIO

class Frontend:
    def __init__(self, host: str, port: int):
        self.app = Flask(__name__, static_url_path="/static", static_folder="./.static")
        CORS(self.app)
        self.host = host
        self.port = port
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self._set_routes()
        self._set_events()

    def _set_routes(self):
        @self.app.route("/")
        def index():
            return send_file("./index.html")
        
    def _set_events(self):
        @self.socketio.on("connect")
        def handle_connect():
            print("[Frontend.set_events] Client connected.")

        @self.socketio.on("disconnect")
        def handle_disconnect():
            print("[Frontend.set_events] Client disconnected.")
    
    def push_subtitle(self, subtitle: str):
        self.socketio.emit("subtitle", subtitle)
    
    def run(self):
        print(f"[Frontend.run] Running frontend at {self.host}:{self.port}")
        self.socketio.run(self.app, host=self.host, port=self.port)