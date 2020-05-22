#!python
from __future__ import print_function
import rospy
from std_msgs.msg import String
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import animation
import numpy as np
import mpl_toolkits.mplot3d as a3

class Fusion:
    def __init__(self):
        # Class variables init
        self.counter = 0 ; self.msg = "0|0|0|0|0|0|0|0|0" ;
        self.fig = plt.figure(linewidth='10', figsize=(6,6)) ;
        self.ax = plt.axes(projection='3d')
        # Values
        self.a = None ; self.g = None ; self.g_raw = None; self.m = None
        # Rot matrix using accel and mag
        self.R_a_m  = None

    def fireup(self):
        rospy.init_node('viz_node', anonymous=True) ; rospy.Subscriber("agm", String, self.ros_callback)
        self.anim_object = animation.FuncAnimation(self.fig, self.animate_cb)
        plt.show()
        rospy.spin()

    def ros_callback(self,resp):
        self.counter += 1 ; self.msg = resp.data

    # Animation callback ; update all plots here
    def animate_cb(self,i):
        values = [float(i) for i in self.msg.split("|")]
        # Nomalize vectors
        self.a = np.array(values[0:3])/np.linalg.norm(values[0:3])
        self.g = np.array(values[3:6])/np.linalg.norm(values[3:6])
        self.g_raw = np.array(values[3:6])
        self.m = np.array(values[6:])/np.linalg.norm(values[6:])

        # Estimate and draw post based on only accel and mag values; set self.R_a_m rotation matrix
        R_am = self.pose_acc_mag()
        self.visualize(self.ax, R_am)
        print("Rotation matrix : \n", R_am)

        # Madgwick algorithm < TODO >


    # Return rotation matrix using just accel and mag
    def pose_acc_mag(self):
        temp_mg = np.cross(self.m,self.a)
        mg = np.array(temp_mg)/np.linalg.norm(temp_mg) ;
        temp_gmg = np.cross(self.a,mg) ; gmg = temp_gmg/np.linalg.norm(temp_gmg)

        self.R_a_m = np.zeros((3,3));
        self.R_a_m[0,:] = mg ; self.R_a_m[1,:] = gmg ; self.R_a_m[2,:] = self.a # THis is the rotation matrix using accel and mag

        return self.R_a_m.copy()

    # input rotation matrix, returns (rotated) unit cube faces and vertices in original frame 
    def cubepts(self,Rt):
        R = Rt.T 
        s = 0.25
        # Line mesh
        pts = [[s,s,-s],[s,-s,-s],[-s,-s,-s],[-s,s,-s],[s,s,-s]]
        pts += [[s,s,s],[s,-s,s],[-s,-s,s],[-s,s,s],[s,s,s]]
        mesh = np.array([R*(np.matrix(i).T) for i in pts])
        # Surface plot
        f1 = mesh[0:4, :,:].reshape((4,3)) # || to z axis
        f2 = mesh[5:9,:,:].reshape((4,3)) # || to z axis
        # || to y axis
        p_temp1 = [[s,s,s],[-s,s,s],[-s,s,-s],[s,s,-s]] ; p_temp2 = [[s,-s,s],[-s,-s,s],[-s,-s,-s],[s,-s,-s]]
        f3 = np.array([R*(np.matrix(i).T) for i in p_temp1]).reshape((4,3)) ; f4 = np.array([R*(np.matrix(i).T) for i in p_temp2]).reshape((4,3))
        # || to x axis
        p_temp3 = [[s,s,s],[s,-s,s],[s,-s,-s],[s,s,-s]] ; p_temp4 = [[-s,s,s],[-s,-s,s],[-s,-s,-s],[-s,s,-s]]
        f5 = np.array([R*(np.matrix(i).T) for i in p_temp3]).reshape((4,3)) ; f6 = np.array([R*(np.matrix(i).T) for i in p_temp4]).reshape((4,3))

        return [f1,f2,f3,f4,f5,f6]

    # Input Axis to plot on and Rotation matrix --> draws the 3d stuff, cube rotating etc 
    def visualize(self,ax,R):
        # Cleanup axes
        ax.clear() ; ax.axis("equal")
        # Draw Co-ord axes
        L = 1.5
        ax.set_xlim(-L, L) ; ax.set_ylim(-L, L) ; ax.set_zlim(-L, L)
        ax.plot3D(np.array([0,1.5]), np.array([0,0]), np.array([0,0]), marker='>')
        ax.plot3D(np.array([0,0]), np.array([0,1.5]), np.array([0,0]), marker='>')
        ax.plot3D(np.array([0,0]), np.array([0,0]), np.array([0,1.5]), marker='>')

        # Putting text
        ax.text(L+0.5,0,0, "X"); ax.text(0,L+0.5,0, "Y"); ax.text(0,0,L+0.5, "Z") ;
        plt.title("Pose estimation using Accelerometer and Magnetometer", fontsize='10')

        # ******* Cube plot3D ---------- mg, gmg, a are 3 mutually perpendicular unit vectors, hence define a coordinate system uniquely
        f = self.cubepts(R.copy()) ; c = ['blue','green', 'orange','pink','purple','red']
        for face,clr in zip(f,c) : ax.add_collection3d(a3.art3d.Poly3DCollection([face],facecolors=clr,edgecolors='black'))

        # Draw vectors
        ax.plot3D(np.array([0,R[2,0]]), np.array([0,R[2,1]]), np.array([0,R[2,2]]),marker='o',zorder=10)
        ax.plot3D(np.array([0,R[0,0]]), np.array([0,R[0,1]]), np.array([0,R[0,2]]),marker='o',zorder=10)
        ax.plot3D(np.array([0,R[1,0]]), np.array([0,R[1,1]]), np.array([0,R[1,2]]),marker='o',zorder=10)

        # Workaround for aspect ratio
        ax.plot3D(np.array([-L,L,L,-L,-L,-L]), np.array([-L,-L,L,L,-L,-L]), np.array([L,L,L,L,L,-L]), color='w')
        ax.plot3D(np.array([-L,L,L,-L,-L]), np.array([-L,-L,L,L,-L]), np.array([-L,-L,-L,-L,-L]), color='w')
        ax.plot3D(np.array([L,L]), np.array([L,L]), np.array([L,-L]), color='w')
        ax.plot3D(np.array([-L,-L]), np.array([L,L]), np.array([L,-L]), color='w')
        ax.plot3D(np.array([L,L]), np.array([-L,-L]), np.array([L,-L]), color='w')


if __name__ == "__main__":
    F = Fusion() ; F.fireup()
