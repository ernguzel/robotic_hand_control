# robotic_hand_control
**Bu projede, el hareketlerini kullanarak bir robotun ileri, geri, sağa ve sola hareket etmesini sağladım. ROS ve OpenCV teknolojileriyle, kamera aracılığıyla gerçek zamanlı el hareketi algılaması yaparak robotun hareketlerini kontrol ediyorum. Proje, robotik kontrol ve görüntü işleme konularına ilgi duyanlar için iyi bir başlangıç noktası sunuyor.**

## Kullanılan Teknolojiler
- Python
- ROS2
- OpenCV


## Kurulum
1. Projeyi klonlayın:
   ```bash
   cd ~/ros2_ws/src
   git clone https://github.com/kullaniciadi/proje-adi.git

2. Workspace'i derleyin:
   ```bash
    cd ~/ros2_ws
    colcon build

3. ROS2 workspace'inizi kaynak (source) yapın:
   ```bash
   source install/setup.bash

4. Robot ve el hareketi kontrol sistemini başlatın:
   ```bash
   ros2 launch eren_bot_camera eren_bot_launch.py  

   
