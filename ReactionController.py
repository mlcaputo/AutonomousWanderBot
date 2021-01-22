#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ForceMapper(): 
    def __init__(self):
        self.r = rospy.Rate(250) # 250hz
        self.x = 0
        self.linear_speed = 1.25
        self.angular_speedR = -.8
        self.angular_speedL = .8
        self.move_cmd = Twist()
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callBack)
        #self.pub_obs = rospy.Publisher('obstacle', String, queue_size=10)
        self.cmd_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=1)
        self.start()

    def forward(self):
        self.move_cmd.linear.x = self.linear_speed

    def stopturn(self):
        self.move_cmd.angular.z = 0

    def turnR(self):
        self.move_cmd.angular.z = self.angular_speedR
    
    def turnL(self):
        self.move_cmd.angular.z = self.angular_speedL

    def stop(self):
        self.move_cmd.linear.x = 0

    def behavior1(self, msg):
        size = len(msg.ranges)
        right = msg.ranges[0]
        front = msg.ranges[size/2]
        left = msg.ranges[size-1]
        print("l,f,r: ", left, front, right)
        if (front > 0.5 and .9 > right > 0.5):
            self.forward()
            self.stopturn()
        elif(front > 0.5 and right > .9):
            self.stop()
            self.turnR()
        elif(front > 0.5 and right < 0.5):
            self.stop()
            self.turnL()
        elif(front < 0.5):
            self.stop()
            self.turnL()
        
        
    def behavior2(self, msg):
        size = len(msg.ranges)
        right = msg.ranges[0]
        front = msg.ranges[size/2]
        left = msg.ranges[size-1]
        print("l,f,r: ", left, front, right)
        if (front > 0.5 and .9 > left > 0.5):
            self.forward()
            self.stopturn()
        elif(front > 0.5 and left > .9):
            self.stop()
            self.turnL()
        elif(front > 0.5 and left < 0.5):
            self.stop()
            self.turnR()
        elif(front < 0.5):
            self.stop()
            self.turnR()

    def behavior3(self, msg):
        size = len(msg.ranges)
        right = msg.ranges[0]
        front = msg.ranges[size/2]
        left = msg.ranges[size-1]
        print("l,f,r: ", left, front, right)
        if(front > 0.85 and left > .25):
            self.forward()
            self.stopturn()
        else:
            self.stop()
            self.turnL()
    
    def behavior4(self, msg):
        size = len(msg.ranges)
        right = msg.ranges[0]
        front = msg.ranges[size/2]
        left = msg.ranges[size-1]
        print("l,f,r: ", left, front, right)
        self.stop()
        self.turnR()

    def behavior5(self, msg):
        size = len(msg.ranges)
        right = msg.ranges[0]
        front = msg.ranges[size/2]
        left = msg.ranges[size-1]
        print("l,f,r: ", left, front, right)
        self.forward()
        self.turnL()
        

    def start(self):
        while not rospy.is_shutdown():
            #self.pub_obs.publish(self.obstacle)
            self.cmd_pub.publish(self.move_cmd)
            self.r.sleep()

    def callBack(self, msg):
        if(self.x<25):
            self.behavior4(msg)

        elif(self.x<50):
            self.behavior3(msg)

        elif(self.x<400):
            self.behavior1(msg)

        elif(self.x<405):
            self.behavior5(msg)
        
        elif(self.x<760):
            self.behavior2(msg)
        
        elif(self.x<770):
            self.behavior5(msg)
        
        self.x = self.x + 1
        
        if(self.x>770):
            self.x = 50
        


def main():
    rospy.init_node('ForceMapper')
    try:
        force = ForceMapper()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()