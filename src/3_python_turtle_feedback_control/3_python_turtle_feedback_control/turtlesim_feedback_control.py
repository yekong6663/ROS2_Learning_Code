import rclpy
from rclpy.node import Node
# 导入小海龟位置的Pose类型与控制其位置的Twist类型
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class TurtlesimFeedbackControl(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        # 创建订阅器订阅小海龟位置，创建发布器发布目标速度
        # 使用ros2 topic list查看话题
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.subscription = self.create_subscription(Pose, "turtle1/pose", self.feedbackcontrol,10)

        # 目标位置
        self.target_x = 7.0
        self.target_y = 7.0

        # 用于PID控制的比例系数与最大速度
        self.max_linear_speed = 2.0
        self.max_angular_speed = 5.0
        self.k = 2.0

    # 订阅器的回调函数，注意一个变量必须是msg用于存放订阅数据
    def feedbackcontrol(self, msg):
        # 计算误差
        ex = self.target_x - msg.x
        ey = self.target_y - msg.y

        # 将误差转化为距离与角度
        distance = math.sqrt(ex*ex + ey*ey)
        theta = math.atan2(ey, ex) - msg.theta
        # 角度归一化
        theta = math.atan2(math.sin(theta), math.cos(theta))

        # 乘以比例系数作为PID控制的输出，并且进行限幅
        vx = min(distance*self.k, self.max_linear_speed)
        vz = min(theta*self.k, self.max_angular_speed)

        # 创建发布对象进行发布
        speed = Twist()
        # 修改linear.x和angular.z即可实现运动
        speed.linear.x = vx
        speed.angular.z = vz
        self.publisher.publish(speed)

def main():
    rclpy.init()
    node = TurtlesimFeedbackControl("yozora")
    rclpy.spin(node)
    rclpy.shutdown()
