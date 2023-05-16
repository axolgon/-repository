import rospy
import numpy as np

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header
import cv2

def BGR(image):
  musigi='0'
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  hist, _ = np.histogram(hsv[:,:,0], bins=180, range=[0, 180]) 
  color_most = np.argmax(hist) 

  if (0<=color_most <=15) or (165<color_most <=180)   :  
           musigi='-1' 
  elif (90<=color_most<=135): 
           musigi='+1' 
  else:
           musigi='0'  
  return musigi

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count=0

    def callback(self, data):
        try:
            # listen image topic
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')

            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP

            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
           
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 75, 200)

            cnts, x = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

            peri = cv2.arcLength(cnts, True)
            verticles=cv2.approxPolyDP(cnts, 0.02* peri, True)    
            
            seat= np.zeros(gray.shape, dtype=np.uint8)
            cv2.drawContours(seat, [verticles],0,(255,255,255))
            tv = cv2.bitwise_and(image, image, seat)

            cv2.imshow('um', image)
            cv2.waitKey(10)    

            msg.frame_id=BGR(tv)



            # publish color_state
            self.color_pub.publish(msg)

        except CvBridgeError as e:
            print(e)



    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    rospy.init_node('CompressedImages1', anonymous=False)
    detector = DetermineColor()
    rospy.spin()
  
