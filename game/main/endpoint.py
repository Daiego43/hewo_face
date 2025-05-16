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

        @self.app.route('/toggle_talk', methods=['POST'])
        def toggle_talk():
            layout = self.get_layout()
            layout.toggle_talk()
            return jsonify({"status": "success"}), 200

        @self.app.route('/trigger_blink', methods=['POST'])
        def trigger_blink():
            layout = self.get_layout()
            layout.trigger_blink()
            return jsonify({"status": "success"}), 200

        @self.app.route('/adjust_position', methods=['POST'])
        def adjust_position():
            layout = self.get_layout()
            data = request.get_json()
            dx = int(data.get("dx", 0))
            dy = int(data.get("dy", 0))
            layout.adjust_position(dx, dy)
            return jsonify({"status": "success"}), 200

        @self.app.route('/set_size', methods=['POST'])
        def adjust_size():
            layout = self.get_layout()
            data = request.get_json()
            size = int(data.get("value", 0))
            layout.set_face_size(size)
            return jsonify({"status": "success"}), 200

        @self.app.route('/set_random_emotion', methods=['POST'])
        def set_random_emotion():
            layout = self.get_layout()
            layout.set_random_emotion()
            return jsonify({"status": "success"}), 200

        @self.app.route('/reset_emotion', methods=['POST'])
        def reset_emotion():
            layout = self.get_layout()
            layout.reset_emotion()
            return jsonify({"status": "success"}), 200

        @self.app.route('/adjust_emotion/<param>', methods=['POST'])
        def adjust_emotion(param):
            layout = self.get_layout()
            data = request.get_json()
            try:
                value = int(data.get("value"))
            except (TypeError, ValueError):
                return jsonify({"status": "error", "message": "Missing or invalid 'value' (must be int)"}), 400

            layout.adjust_emotion(param, value)
            return jsonify({"status": "success"}), 200

    def start(self, host=SERVER_IP, port=SERVER_PORT):
        def run_server():
            self.app.run(host=host, port=port, debug=True, use_reloader=False)

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
