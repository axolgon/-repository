import rospy
import numpy as np

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header
import cv2

def BGR(img, arr):
  bgr=[0,0,0]
  musigi='0'

  for i in range(70):
    p1=arr[0]+(arr[1]-arr[0])*(i/70)
    p2=arr[3]+(arr[2]-arr[3])*(i/70)
    for j in range(100):
      q=p1+(p2-p1)*(j/100)
      b,g,r=img[int(q[1]),int(q[0])]
      if (b>=170 and b<=255) and (g>=0 and g<=150) and (r>=0 and r<=150):
        bgr[0]+=1
      elif (b>=0 and b<=150) and (g>=0 and g<=150) and (r>=170 and r<=255):
        bgr[1]+=1
      else:
        bgr[2]+=1
  if np.argmax(bgr)==0:
    musigi='+1'
  elif np.argmax(bgr)==1:
    musigi='-1'    
  elif np.argmax(bgr)==2:
    musigi='0'    
  return musigi


class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        #self.pub=rospy.Publisher('processed_data',np.ndarray,queue_size=10)
        #self.last_published_data=None
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


            draw=image.copy()

            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
           
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(gray, 75, 200)

        
           
            cnts, x = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
            global pts

            for c in cnts :
              peri = cv2.arcLength(c, True)
              verticles=cv2.approxPolyDP(c, 0.02* peri, True)
              if len(verticles) == 4:
                      break
            try:          
                      if cv2.contourArea(c)>(draw.shape[0]*draw.shape[1])/4:
                         pts = verticles.reshape(4, 2)
                      else: 
                         chamshipjo
            except:
                      pass
                             
            

            cv2.imshow('um', draw)
            cv2.waitKey(10)    
            # determine background color
            # TODO
            # determine the color and assing +1, 0, or, -1 for frame_id
            #msg.frame_id = '+1' # CCW (Blue background)
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW (Red background)


            msg.frame_id=BGR(draw, pts)



            # publish color_state
            self.color_pub.publish(msg)

        except CvBridgeError as e:
            print(e)



    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    pts=np.array([[0,0],[0,0],[0,0],[0,0]])
    rospy.init_node('CompressedImages1', anonymous=False)
    detector = DetermineColor()
    rospy.spin()
