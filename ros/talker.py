from std_msgs.msg import String
import rospy
import subprocess
import time


def talker():
    time.sleep(0.1)
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    count = 0
    while not rospy.is_shutdown() and count < 10:
        hello_str = "hello world %s" % count
        #rospy.loginfo(hello_str)
        pub.publish(hello_str)
        count += 1
        rate.sleep()

    rospy.sleep(1)





    
    
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
