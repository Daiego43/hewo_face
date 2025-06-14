import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point, Vector3

from std_msgs.msg import Empty, UInt32
from hewo_face_interfaces.msg import Emotion, AdjustEmotionPoint, AdjustPosition

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import pygame
import numpy as np
import pathlib
import psutil
import os

from hewo_face.hewo.main.window import MainWindow
from hewo_face.hewo.settings import SettingsLoader
from hewo_face.hewo.objects.hewo import HeWo
from hewo_face.hewo.objects.multimedia import MultimediaLayout



class HeWoMainNode(Node):
    def __init__(self):
        super().__init__('hewo_main_node')
        self.bridge = CvBridge()
        self.process = psutil.Process(os.getpid())
        self.frame_count = 0
        self.time_accum = 0.0

        # Load all settings
        loader = SettingsLoader()
        self.window_settings = loader.load_settings("hewo_face.hewo.settings.window")
        self.hewo_settings = loader.load_settings("hewo_face.hewo.settings.hewo")
        print(self.window_settings)
        print(self.hewo_settings)
        # Setup layouts and window
        self.window = MainWindow(settings=self.window_settings)
        self.hewo_layout = HeWo(settings=self.hewo_settings)
        self.window.layout_dict = {"hewo": self.hewo_layout}
        self.window.active_layout = self.window_settings["active_layout"]  # 'hewo'

        # Setup publishers
        self.emotion_pub = self.create_publisher(String, 'hewo/emotion', 10)
        self.position_pub = self.create_publisher(Point, 'hewo/position', 10)
        self.size_pub = self.create_publisher(Vector3, 'hewo/size', 10)
        self.frame_pub = self.create_publisher(Image, 'hewo/frame', 10)

        # self.create_timer(5.0, self.log_performance)

        # Setup subscribers
        self.create_subscription(Emotion, 'hewo/set_emotion_goal', self.handle_set_emotion_goal, 10)
        self.create_subscription(AdjustEmotionPoint, 'hewo/adjust_emotion_point', self.handle_adjust_emotion_point, 10)
        self.create_subscription(AdjustPosition, 'hewo/adjust_position', self.handle_adjust_position, 10)
        self.create_subscription(UInt32, 'hewo/set_size', self.handle_set_size, 10)
        self.create_subscription(Empty, 'hewo/trigger_blink', self.handle_trigger_blink, 10)
        self.create_subscription(Empty, 'hewo/toggle_talk', self.handle_toggle_talk, 10)

    # ------------------------Publisher actions------------------------
    def publish_emotion(self):
        try:
            layout = self.window.get_active_layout()
            emotion = layout.get_emotion()
            msg = String()
            msg.data = str(emotion)
            self.emotion_pub.publish(msg)
        except Exception as e:
            self.get_logger().warn(f"Emotion publish failed: {e}")

    def publish_position(self):
        try:
            layout = self.window.layout_dict.get('hewo')
            pos = Point(
                x=float(layout.position[0]),
                y=float(layout.position[1]),
                z=0.0
            )
            self.position_pub.publish(pos)
        except Exception as e:
            self.get_logger().warn(f"Position publish failed: {e}")

    def publish_size(self):
        try:
            layout = self.window.get_active_layout()
            size = Vector3(
                x=float(layout.size[0]),
                y=float(layout.size[1]),
                z=0.0
            )
            self.size_pub.publish(size)
        except Exception as e:
            self.get_logger().warn(f"Size publish failed: {e}")

    def publish_frame_img(self):
        try:
            # Draw entire main window instead of just layout
            self.window.draw()
            frame = pygame.surfarray.array3d(self.window.screen)
            frame = np.transpose(frame, (1, 0, 2))
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="rgb8")
            self.frame_pub.publish(img_msg)
        except Exception as e:
            self.get_logger().warn(f"Frame publish failed: {e}")

    def publish_all(self):
        self.publish_emotion()
        self.publish_position()
        self.publish_size()
        # self.publish_frame_img()

    # ------------------------Subscriber actions------------------------
    def handle_set_emotion_goal(self, msg: Emotion):
        data = dict(zip(msg.keys, msg.values))
        self.window.layout_dict['hewo'].set_emotion_goal(data)
        self.get_logger().info(f"[ROS] Emotion goal set: {data}")

    def handle_adjust_emotion_point(self, msg: AdjustEmotionPoint):
        self.window.layout_dict['hewo'].adjust_emotion(msg.param, msg.value)
        self.get_logger().info(f"[ROS] Adjusted emotion: {msg.param} → {msg.value}")

    def handle_adjust_position(self, msg: AdjustPosition):
        self.window.layout_dict['hewo'].adjust_position(msg.dx, msg.dy)
        self.get_logger().info(f"[ROS] Adjusted position by ({msg.dx}, {msg.dy})")

    def handle_set_size(self, msg: UInt32):
        self.window.layout_dict['hewo'].set_face_size(msg.data)
        self.get_logger().info(f"[ROS] Set face size: {msg.data}")

    def handle_trigger_blink(self, msg: Empty):
        self.window.layout_dict['hewo'].trigger_blink()
        self.get_logger().info("[ROS] Triggered blink")

    def handle_toggle_talk(self, msg: Empty):
        self.window.layout_dict['hewo'].toggle_talk()
        self.get_logger().info("[ROS] Toggled talk")

    # Helper methods for main loop
    def step_frame(self, dt_ms):
        self.frame_count += 1
        self.time_accum += dt_ms / 1000.0

    def log_performance(self):
        cpu = self.process.cpu_percent(interval=None)
        mem = self.process.memory_info().rss / (1024 * 1024)
        fps = self.frame_count / self.time_accum if self.time_accum > 0 else 0
        self.get_logger().info(f"[Perf] CPU: {cpu:.1f}% — RAM: {mem:.2f} MB — FPS: {fps:.1f}")
        self.frame_count = 0
        self.time_accum = 0.0


def main(args=None):
    rclpy.init(args=args)
    node = HeWoMainNode()
    clock = pygame.time.Clock()

    try:
        while rclpy.ok():
            node.window.handle_events()
            dt_ms = clock.tick(node.window.fps)
            node.step_frame(dt_ms)
            node.window.update(dt_ms)
            node.window.draw()
            node.publish_all()
            rclpy.spin_once(node, timeout_sec=0.001)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        pygame.quit()


if __name__ == '__main__':
    main()
