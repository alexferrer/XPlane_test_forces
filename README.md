# XPlane_test_forces
GUI to Test the effect of drefs forces on the aircract , .csv file configurable
![image1](https://github.com/user-attachments/assets/83dd74f4-6d1c-4402-824d-ff07dbae1d5f)

Create a .csv file  with datarefs and settings, then automatically use to test their effect on your aircraft. 
The default file looks like: 

dataref_path,type,scale,low_limit,high_limit,name

sim/flightmodel/forces/faxil_plug_acf,float,-10,0,100,-Thrust 10x

sim/flightmodel/forces/fnrml_plug_acf,float,-100,-50,50,-Lift 10x

sim/flightmodel/position/local_vy,float,0.01,-50,50,vertical speed x/100

sim/flightmodel/position/local_ay,float,1,-50,50,vertical acceleration 

sim/flightmodel/position/local_y,float,0.1,0,100,vertical position x/10

sim/flightmodel/forces/L_plug_acf,float,1,-50,50,Roll

sim/flightmodel/forces/M_plug_acf,float,10,-50,50,Pitch 10x

Add your own to do your own testing  from (https://developer.x-plane.com/datarefs/) 


Installation
------------

( https://xppython3.readthedocs.io/en/latest/index.html )
This is XPPython3 version 4 and includes both the X-Plane plugin as well as a private version of Python3. Unlike previous versions of XPPython3, you no longer need to install your own copy of Python.

For installation copy the XPLANE Test forces Python files to the X-Plane Resources/plugins/PythonPlugins folder so that the Python plugin can find them.
