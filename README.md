# robotic_hand_control
Bu projede, el hareketlerini kullanarak bir robotun ileri, geri, sağa ve sola hareket etmesini sağladım. ROS ve OpenCV teknolojileriyle, kamera aracılığıyla gerçek zamanlı el hareketi algılaması yaparak robotun hareketlerini kontrol ediyorum. Proje, robotik kontrol ve görüntü işleme konularına ilgi duyanlar için iyi bir başlangıç noktası sunuyor.
El Hareketleri ile Robot Kontrolü
Bu projede, el hareketleriyle bir robotun ileri, geri, sağa ve sola hareket etmesini sağladım. ROS2 (Robot Operating System) ve OpenCV kullanarak el hareketlerinin algılanması ve robotun kontrolü gerçekleştirilmektedir.

# Proje Başlığı

Bu proje, **el hareketleri** ile bir robotu ileri, geri, sağa ve sola hareket ettirmeyi sağlar. ROS2 ve OpenCV kullanarak el hareketlerini algılayıp robotu kontrol ediyoruz.

## Kullanılan Teknolojiler
- Python
- ROS2
- OpenCV
- Colcon

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

   
