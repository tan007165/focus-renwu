#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

class Exploration(Node):
    def __init__(self):
        super().__init__('exploration')
        self.subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('自主探索避障节点已启动！')

    def scan_callback(self, msg):
        front = msg.ranges[len(msg.ranges)//2]
        left = msg.ranges[len(msg.ranges)*3//4]
        right = msg.ranges[len(msg.ranges)//4]

        if math.isinf(front) or math.isnan(front): front = 10.0
        if math.isinf(left) or math.isnan(left): left = 10.0
        if math.isinf(right) or math.isnan(right): right = 10.0

        twist = Twist()

        # 核心逻辑：只要前方没有紧挨着障碍物，就正常速度前进！
        if front > 0.5:
            twist.linear.x = 0.25  # 正常速度（比之前快很多）
            twist.angular.z = 0.0
            self.get_logger().info('前方畅通，正常速度前进...')
        else:
            # 前方有障碍物，停止前进，原地转向寻找出路
            twist.linear.x = 0.0
            # 固定向左转，直到扫到前方没有障碍物为止
            twist.angular.z = 1.0
            self.get_logger().info('前方遇障，正在原地转圈寻找出路...')

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = Exploration()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
