import threading
from flask import Flask, request, jsonify

SERVER_IP = '0.0.0.0'
SERVER_PORT = 5000


class ServerEndPoint:
    def __init__(self, main_window):
        self.app = Flask(__name__)
        self.main_window = main_window
        self.setup_routes()

    def get_layout(self):
        if self.main_window.active_layout is not None:
            return self.main_window.layout_dict[self.main_window.active_layout]
        return None

    def setup_routes(self):
        @self.app.route('/set_emotion_goal', methods=['POST'])
        def set_emotion():
            layout = self.get_layout()
            if not layout or not hasattr(layout, 'set_emotion_goal'):
                return jsonify({"status": "error", "message": "No valid layout for setting emotion"}), 400
            try:
                data = request.get_json()
                layout.set_emotion_goal(data)
                return jsonify({"status": "success"}), 200
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400

        @self.app.route('/get_emotion', methods=['GET'])
        def get_emotion():
            layout = self.get_layout()
            if not layout or not hasattr(layout, 'get_emotion'):
                return jsonify({"status": "error", "message": "No valid layout for getting emotion"}), 400
            try:
                emotion = layout.get_emotion()
                return jsonify({"status": "success", "emotion": emotion}), 200
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 400

    def start(self, host=SERVER_IP, port=SERVER_PORT):
        def run_server():
            self.app.run(host=host, port=port, debug=True, use_reloader=False)

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
