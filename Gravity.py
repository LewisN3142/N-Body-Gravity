# import potentially useful libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# settings
isTest = 1;
testTolerance = 1e-8;

# variables (constants and in/out files)
gravitationalConstant = 6.7e-11;
astronomicalUnit = 1.5e11
solarMass = 2e30;

myPath = os.path.dirname(os.path.abspath(__file__));

if isTest == 0:
    inputFile = myPath + r'/dataInput.csv';
else:
    inputFile = myPath + r'/dataTest.csv' 

outputFile = myPath + r'/dataOutput.csv';

# test data (maybe import from file?)
xAccelerationTest = np.array([1.95682e-6,7.05176e-4,-1.06266e-3]);
yAccelerationTest = np.array([1.96991e-6,-7.0910e-4,1.05873e-3]);

# merge constants into overall float scale
accelerationScale = gravitationalConstant * solarMass / (astronomicalUnit * astronomicalUnit);

## import masses and positions from data file and store in arrays (allows for large number of objects)
df = pd.read_csv(inputFile);
numberObjects = len(df);

xPositions_List = df.get("xPosition (au)").to_numpy();
yPositions_List = df.get("yPosition (au)").to_numpy();
masses_List = df.get("mass (M0)").to_numpy();
print('data imported');

## compute the accelerations in O(n^2) and store in numpy arrays
xAcceleration_List = np.zeros(numberObjects);
yAcceleration_List = np.zeros(numberObjects);

for i in range(1,numberObjects):
    for j in range(0,i):
        # note typo in problem
        changeInX = xPositions_List[j] - xPositions_List[i];
        changeInY = yPositions_List[j] - yPositions_List[i];
        
        # in c++ could implement fast inverse square root for speed
        radiusCubed = (changeInX * changeInX + changeInY * changeInY)**(-1.5);
        xAcceleration_List[i] += masses_List[j] * changeInX * radiusCubed;
        xAcceleration_List[j] -= masses_List[i] * changeInX * radiusCubed;
        yAcceleration_List[i] += masses_List[j] * changeInY * radiusCubed;
        yAcceleration_List[j] -= masses_List[i] * changeInY * radiusCubed;  
print('acceleration computed');
        
# unit test against initial data (pass if all true)
if isTest != 0:
    a = abs(xAcceleration_List - xAccelerationTest) <= testTolerance;
    print(a);
    b = abs(yAcceleration_List - yAccelerationTest) <= testTolerance;
    print(b);
    if (np.prod(a) * np.prod(b) == 0):
        print("Test failed");
    else:
        print("Test passed");
        
# rescale acceleration 
xAccelerationRescaled_List = xAcceleration_List * accelerationScale;
yAccelerationRescaled_List = yAcceleration_List * accelerationScale;

# output result of calculation to new csv file 
df['xAcceleration (ms^-2)'] = xAccelerationRescaled_List;
df['yAcceleration (ms^-2)'] = yAccelerationRescaled_List;

df.index += 1;
df.to_csv(outputFile, encoding='utf-8', index=True, header=True);
print('data saved');


# print plot of positions and directions/relative magnitudes of acceleration 
fig, ax = plt.subplots() 

accelerationUnit = 5000; # switch to normalised... (make setting)

for i in range(0,numberObjects):
    ax.quiver(xPositions_List[i],yPositions_List[i],accelerationUnit * xAcceleration_List[i],accelerationUnit * yAcceleration_List[i],angles='xy',scale_units='xy',scale=1, color='r');
    
plt.grid();
plt.title('Acceleration vectors of particles in ' + str(numberObjects) + '-body system');
plt.xlabel('x Position (au)');
plt.ylabel('y Position (au)');
fig.gca().set_aspect("equal");
fig.savefig(myPath + '/figure 1.png');
plt.show();
plt.close(fig);
print('figure saved');


