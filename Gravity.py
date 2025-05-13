# import potentially useful libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


##### Version 2 (functional programming) ##################################################################################

#### Settings
isTest = 1;
testTolerance = 1e-8; 
inputFile = 'dataInput';
outputFile = 'dataOutput';
arrowScale = 0; # set to 0 for unit vectors
accelerationMode = 'naive' # Options: 'naive' or 'bh' (Barnes--Hut)

#### (Global) Constants
gravitationalConstant = 6.7e-11;
astronomicalUnit = 1.5e11
solarMass = 2e30;

accelerationScale = gravitationalConstant * solarMass / (astronomicalUnit * astronomicalUnit); # Convert units to SI (scales by ~e-3)

myPath = os.path.dirname(os.path.abspath(__file__)) + r'/';



#### Functions ############################################################################################################

### Load in data from csv file
def loadData(chosenInputFile):
    # Change input file to test version if selected
    if isTest != 0:
        chosenInputFile = 'dataTest'
    
    # Import data from file (allows for large number of objects)
    loadPath = myPath + chosenInputFile + '.csv';
    dataFrame = pd.read_csv(loadPath);
    print('data imported from ' + loadPath);
    return dataFrame, chosenInputFile;
      
###  Convert dataFrame to dict 
def dataFrameToNumpyDict(dataFrame):
    data = dataFrame.to_dict(orient='list');
    for key in data:
        data[key] = np.array(data[key]);   
    return data;
   
### Rescale quantities
def dataRescale(dataDict, scale):
    for key in dataDict:
        dataDict[key]*= scale;
      
### Plot vectors on graph
# TODO maybe zip positions, data, acceleration etc into tuples then unzip at end...
def plotVectors(xPosition, yPosition, xData, yData, labels, vectorScale):
    fig, ax = plt.subplots();
    figurePath = myPath + inputFile + r'_' + labels[3] + '.png';
    
    if vectorScale == 0:
        vectorScale = (xData*xData + yData*yData)**(-0.5);

    for i in range (0,len(xPosition)):
        ax.quiver(xPosition, yPosition, vectorScale*xData,vectorScale*yData, angles='xy',scale_units='xy',scale=1,color='r');
        
    plt.grid();
    plt.title(labels[0]);
    plt.xlabel(labels[1]);
    plt.ylabel(labels[2]);
        
    fig.gca().set_aspect("equal");
    fig.savefig(figurePath);
    plt.close(fig);
    print('figure saved to ' + figurePath);
    
### Unit test against data provided in exercise (pass if all true)
def testData(dataActual, dataTest):  

    a = abs(dataActual - dataTest) <= testTolerance;
    print(a);
    if (np.prod(a) == 0):
        print("Test failed");
    else:
        print("Test passed");
        
### Output data to csv file
def saveData(dataFrame, chosenOutputFile):
    savePath = myPath + chosenOutputFile + '.csv';
    df.to_csv(savePath, encoding='utf-8', index=True, header=True);
    print('data saved to ' + savePath);
    
   
   
### Acceleration Code #####################################################################################################

## Naive algorithm for computing acceleration with O(n^2) complexity

# Compute acceleration (in non SI units)
def naiveAcceleration(xPosition, yPosition, masses): 
    
    numberObjects = len(masses)
    xAcceleration = np.zeros(numberObjects);
    yAcceleration = np.zeros(numberObjects);
    
    for i in range(1,numberObjects):
        for j in range(0,i):
            # note typo in problem, can we do this using numpy operations to improve efficiency...
            changeInX = xPosition[j] - xPosition[i];
            changeInY = yPosition[j] - yPosition[i];
            radiusCubed = (changeInX * changeInX + changeInY * changeInY)**(-1.5); # could use fast inverse sqrt in c++
            
            xAcceleration[i] += masses[j] * changeInX * radiusCubed;
            xAcceleration[j] -= masses[i] * changeInX * radiusCubed;
            yAcceleration[i] += masses[j] * changeInY * radiusCubed;
            yAcceleration[j] -= masses[i] * changeInY * radiusCubed;  
      
    print('acceleration computed');
    return {"xAcceleration (ms^-2)": xAcceleration, "yAcceleration (ms^-2)":yAcceleration};
  

## Barnes Hut Algorithm
# TODO add code
def barnesHutAcceleration(xPosition, yPosition, masses):
    



# Wrapper function (compute, test, plot, rescale)
def accelerationWrapper(data, mode):
    
    if mode == 'naive':
        acceleration = naiveAcceleration(data["xPosition (au)"],data["yPosition (au)"],data["mass (M0)"]);
    elif mode == 'bh':
        acceleration = barnesHutAcceleration(data["xPosition (au)"],data["yPosition (au)"],data["mass (M0)"]);

    if isTest != 0:
        testData(np.concatenate((acceleration["xAcceleration (ms^-2)"], acceleration["yAcceleration (ms^-2)"])),np.concatenate((data["xAccelerationTest"], data["yAccelerationTest"])));
        
    accelerationFigureLabels = ['Acceleration vectors of particles in ' + str(len(data["xPosition (au)"])) + '-body system', 'x Position (au)', 'y Position (au)', 'acceleration']
    
    plotVectors(data["xPosition (au)"],data["yPosition (au)"],acceleration["xAcceleration (ms^-2)"], acceleration["yAcceleration (ms^-2)"],accelerationFigureLabels,arrowScale);
    
    dataRescale(acceleration, accelerationScale);
    return acceleration;

  
#### Execution

# load data, clean, then convert to numpy
df, inputFile = loadData(inputFile); 
df = dataFrameToNumpyDict(df);

# Perform computations
df.update(accelerationWrapper(df,accelerationMode));

# Convert back to dataFrame and export
df = pd.DataFrame.from_dict(df);
saveData(df, outputFile);

