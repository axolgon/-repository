import rospy
import numpy as np

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header
import cv2


def apply_filter(input_, filter_):
    input_height= input_.shape[0]
    input_width = input_.shape[1]
    filter_height= filter_.shape[0]
    filter_width = filter_.shape[1]


    output_height = input_height-filter_height+1
    output_width = input_width-filter_width+1
    output = np.zeros((output_height, output_width))

    for i in range(output_height):
        for j in range(output_width):
            k=np.sum(filter_*input_[i:i+filter_height,j:j+filter_width])
            if np.abs(k)>10:
                output[i,j]=255
            else:
                output[i,j]=0

    return output

def BGR(img):
  bgr=[0,0,0]
  musigi='0'
  for i in range(80):
    for j in range(100):
      b,g,r=img[int((i/80)*img.shape[0]*16/27+img.shape[0]*5/42),int((j/100)*img.shape[1]*13/18+img.shape[1]*1/9)]
      if (b>=180 and b<=255) and (r>=0 and r<=60):
       bgr[0]+=1
      elif (b>=0 and b<=60) and (g>-0 and g<=150) and (r>=190 and r<=255):
       bgr[1]+=1
      else:
       bgr[2]+=1
  if np.argmax(bgr)==0:
    musigi='1'
  elif np.argmax(bgr)==1:
    musigi='-1'     
  elif np.argmax(bgr)==2:
    musigi='0'    
  return musigi
  
x=np.array([[1,0,-1],[1,0,-1],[1,0,-1]])

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

            #image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('um',apply_filter(image_gray,x))
            
            
            # determine background color
            # TODO
            # determine the color and assing +1, 0, or, -1 for frame_id
            #msg.frame_id = '+1' # CCW (Blue background)
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW (Red background)
            

            cv2.imshow('Image',image)
            cv2.waitKey(1)
            
            #print(image[int(image.shape[0]*0.5),int(image.shape[1]*0.3)])
            print(BGR(image))

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
