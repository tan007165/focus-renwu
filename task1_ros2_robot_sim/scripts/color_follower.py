#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class ColorFollower(Node):
    def __init__(self):
        super().__init__('color_follower')
        self.subscription = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()
        self.get_logger().info('颜色追踪节点已启动，正在等待摄像头数据...')

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f'CvBridge 转换错误: {e}')
            return

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # 定义红色范围
        lower_red1 = np.array([0, 100, 100]); upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100]); upper_red2 = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)

        M = cv2.moments(mask)
        twist = Twist()

        # 判断逻辑：是否找到了足够大的红色目标
        if M["m00"] > 1000: 
            # ---- 发现目标，进入跟随模式 ----
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            h, w = cv_image.shape[:2]
            error_x = cx - w // 2
            
            twist.angular.z = -float(error_x) / 200.0  # 比例控制转向
            twist.linear.x = 0.15                      # 保持前进速度
            
            self.get_logger().info(f'识别到红色目标! 误差x={error_x}, 转向={twist.angular.z:.2f}')
        else:
            # ---- 没有发现目标，进入搜索模式（自主转向寻找）----
            twist.linear.x = 0.0
            twist.angular.z = 0.5  # 原地旋转寻找
            self.get_logger().info('未发现红色目标，正在原地旋转搜索...', throttle_duration_sec=2.0)

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ColorFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
