import threading
from flask import Flask, request, jsonify

SERVER_IP = '0.0.0.0'
SERVER_PORT = 5000


class ServerEndPoint:
    def __init__(self, main_window):
        self.app = Flask(__name__)
        self.main_window = main_window
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/set_emotion_goal', methods=['POST'])
        def set_emotion():
            try:
                data = request.get_json()
                if self.main_window.active_layout is not None:
                    self.main_window.layout_list[self.main_window.active_layout].set_emotion_goal(data)
                return jsonify({"status": "success"}), 200
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400

        @self.app.route('/get_emotion', methods=['GET'])
        def get_emotion():
            if self.main_window.active_layout is not None:
                emotion = self.main_window.layout_list[self.main_window.active_layout].get_emotion()
                return jsonify({"status": "success", "emotion": emotion}), 200
            return jsonify({"status": "error", "message": "No active layout"}), 400

        @self.app.route('/command', methods=['POST'])
        def command():
            try:
                data = request.get_json()
                command = data.get("command")
                if self.main_window.active_layout is not None:
                    layout = self.main_window.layout_list[self.main_window.active_layout]
                    if command == "toggle_mode":
                        layout.toggle_mode()
                        return jsonify({"status": "success"}), 200
                return jsonify({"status": "error", "message": "Invalid command"}), 400
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400

    def start(self, host=SERVER_IP, port=SERVER_PORT):
        def run_server():
            self.app.run(host=host, port=port, debug=True, use_reloader=False)

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()