# FOCUS 2026年秋季招新控制组考核任务提交

## 环境与依赖
- 系统：Windows 11 + WSL2 (Ubuntu 22.04)
- ROS版本：ROS 2 Humble
- 仿真环境：Gazebo Classic 11 + RViz2
- 依赖库：SLAM Toolbox、OpenCV、cv_bridge

安装命令：
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-slam-toolbox ros-humble-teleop-twist-keyboard ros-humble-cv-bridge python3-opencv -y

工程构建与运行：
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch recruit_robot_sim bringup.launch.py
ros2 launch recruit_robot_sim slam.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard

## 任务完成情况
- TASK1-2：完成了基础配置和自定义机器人模型修改。
- TASK3-4：完成了SLAM建图，并修改参数进行了地图对比，成功保存了地图文件。
- TASK5：编写了避障代码，实现了自主移动测试。
- TASK6：编写了颜色追踪代码，实现了目标搜索和跟随逻辑。
- TASK7：说明了Nav2导航的设计思路。

## 遇到的问题与尝试
由于WSLg图形界面频繁崩溃，无法查看完整画面。我采用了终端数据流调试方法，成功保存了地图和代码日志。所有截图和录屏已放在对应文件夹中，证明了有效的尝试过程。
