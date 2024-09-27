import cv2
import time
import mediapipe as mp
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist

class HandTrackingNode(Node):
    def __init__(self):
        super().__init__('hand_tracking_node')

        # ROS publisherlar
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.publisher_cmd = self.create_publisher(Twist, '/cmd_vel', 10)

        # OpenCV ve Mediapipe ayarları
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)
        self.mp_hand = mp.solutions.hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils

        # Timer ayarı, her 0.1 saniyede bir callback çalışır
        self.timer = self.create_timer(0.1, self.run)

        # Diğer ayarlar
        self.tipIds = [4, 8, 12, 16, 20]
        self.pTime = 0
        self.cTime = 0

    def run(self):
        suc, img = self.cap.read()
        if not suc:
            self.get_logger().error("Kamera görüntüsü alınamadı.")
            return
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.mp_hand.process(img_rgb)

        lm_list = []

        if results.multi_hand_landmarks:
            for i, hand_lms in enumerate(results.multi_hand_landmarks):
                self.mp_draw.draw_landmarks(img, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)
                hand_lm_list = []
                for id, lm in enumerate(hand_lms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_lm_list.append([id, cx, cy])

                # Handedness tespiti ve düzeltme
                handedness = results.multi_handedness[i].classification[0].label

                # Kameraya göre sağ ve sol el tespitini tersine çeviriyoruz
                if handedness == "Right":
                    handedness = "Left"
                else:
                    handedness = "Right"

                # Parmakların açık olup olmadığını kontrol etme
                sayac = 0
                if hand_lm_list[20][2] < hand_lm_list[1][2]:
                    for i in range(1, 5):
                        if hand_lm_list[self.tipIds[i]][2] < hand_lm_list[self.tipIds[i] - 2][2]:
                            sayac += 1
                    # 1 düzgit # 2 geri git # 0 dur # -1 saga don# -2 sola
                    if sayac > 1:  # El açık (ileriye git)
                        self.car_move(1) 
                        if handedness == "Right":
                            cv2.putText(img, f"Right Hand - Duz Git", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)
                        else:
                            cv2.putText(img, f"Left Hand - Duz Git", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
                    else:  # El kapalı (geri git)
                        self.car_move(2)
                        if handedness == "Right":
                            cv2.putText(img, f"Right Hand - Geri Git", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)
                        else:
                            cv2.putText(img, f"Left Hand - Geri Git", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
                else:
                    if hand_lm_list[0][1] > hand_lm_list[13][1]:
                        self.car_move(-1)
                        if handedness == 'Right':
                            cv2.putText(img, f"Right Hand - saga don", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
                        else:
                            cv2.putText(img, f"Left Hand - saga don", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)

                    else:
                        self.car_move(-2)
                        if handedness == 'Right':
                            cv2.putText(img, f"Right Hand - sola don", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
                        else:
                            cv2.putText(img, f"Left Hand - sola don", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
    
        else:
            self.car_move(0)
        # FPS hesapla
        self.cTime = time.time()
        fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime

        cv2.putText(img, f"FPS: {int(fps)}", (10, 75), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        cv2.imshow("img", img)

        # ROS mesajı olarak görüntüyü yayınla
        image_message = self.bridge.cv2_to_imgmsg(img, encoding="bgr8")
        self.publisher_.publish(image_message)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()

    def car_move(self, result):
        msg = Twist()
        if result == 1:
            msg.linear.x = 0.5  # İleri hareket
            msg.angular.z = 0.0
            self.get_logger().info('İleri gidiyor...')
        elif result == 2:
            msg.linear.x = -0.5  # Geri hareket
            msg.angular.z = 0.0
            self.get_logger().info('Geri gidiyor...')
        elif result == 0:
            msg.linear.x = 0.0  # dur
            msg.angular.z = 0.0
            self.get_logger().info('duruyor...')
        elif result == -1:
            msg.linear.x = 0.0  # dur
            msg.angular.z = -0.5
            self.get_logger().info('saga donuyor...')
        elif result == -2:
            msg.linear.x = 0.0  # dur
            msg.angular.z = 0.5
            self.get_logger().info('sola donuyor...')
        self.publisher_cmd.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    hand_tracking_node = HandTrackingNode()
    rclpy.spin(hand_tracking_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
