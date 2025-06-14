import rclpy
from rclpy.node import Node
from std_msgs.msg import Empty, UInt32
from geometry_msgs.msg import Point, Vector3
from hewo_face_interfaces.msg import Emotion, AdjustPosition
import time


class HeWoTestNode(Node):
    def __init__(self):
        super().__init__('hewo_test_node')

        # Subs
        self.create_subscription(Emotion, 'hewo/emotion', self.cb_emotion, 10)
        self.create_subscription(Point, 'hewo/position', self.cb_position, 10)
        self.create_subscription(Vector3, 'hewo/size', self.cb_size, 10)

        # Pubs
        self.emotion_goal_pub = self.create_publisher(Emotion, 'hewo/set_emotion_goal', 10)
        self.set_position_pub = self.create_publisher(AdjustPosition, 'hewo/adjust_position', 10)
        self.set_size_pub = self.create_publisher(UInt32, 'hewo/set_size', 10)
        self.toggle_talk_pub = self.create_publisher(Empty, 'hewo/toggle_talk', 10)

        self.emotion_latest = None
        self.sent = False

        self.timer = self.create_timer(2.0, self.test_sequence)

    def cb_emotion(self, msg: Emotion):
        self.emotion_latest = dict(zip(msg.keys, msg.values))
        # self.get_logger().info(f"[✓] Emotion received: {self.emotion_latest}")

    def cb_position(self, msg: Point):
        pass
        # self.get_logger().info(f"[✓] Position received: ({msg.x}, {msg.y})")

    def cb_size(self, msg: Vector3):
        pass # self.get_logger().info(f"[✓] Size received: ({msg.x}, {msg.y})")

    def test_sequence(self):
        if self.sent:
            return

        self.get_logger().info("▶ Sending test Emotion goal...")
        print(self.emotion_latest)
        keys = list(self.emotion_latest.keys())
        values = list(self.emotion_latest.values())
        msg = Emotion(keys=keys, values=values)
        self.emotion_goal_pub.publish(msg)

        time.sleep(1.0)

        self.get_logger().info("▶ Sending AdjustPosition...")
        pos_msg = AdjustPosition(dx=25, dy=15)
        self.set_position_pub.publish(pos_msg)

        time.sleep(1.0)

        self.get_logger().info("▶ Sending new face size...")
        size_msg = UInt32()
        size_msg.data = 220
        self.set_size_pub.publish(size_msg)

        time.sleep(1.0)

        self.get_logger().info("▶ Sending Toggle Talk...")
        self.toggle_talk_pub.publish(Empty())

        self.sent = True
        self.get_logger().info("✅ All test messages sent.")


def main(args=None):
    rclpy.init(args=args)
    node = HeWoTestNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
