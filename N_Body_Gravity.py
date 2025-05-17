#### import potentially useful libraries #################################################################################
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


#### Version 2 (functional programming) ##################################################################################

### Settings
isTest = 0;
testTolerance = 1e-8; 
inputFile = 'dataInput';
outputFile = 'dataOutput';
arrowScale = 0; # set to 0 to set all arrows to the same length
accelerationMode = 'naive'; # Options: 'naive' or 'bh' (Barnes--Hut)
isDropDuplicates = 0;

### (Global) Constants
gravitationalConstant = 6.7e-11;
astronomicalUnit = 1.5e11
solarMass = 2e30;

accelerationScale = gravitationalConstant * solarMass / (astronomicalUnit * astronomicalUnit); # Convert units to SI (scales by ~e-3)

myPath = os.path.dirname(os.path.abspath(__file__)) + r'/';


### File I/O ############################################################################################################

## Load in data from csv file
def loadData(chosenInputFile, dropDuplicates):
    # Change input file to test version if selected
    if isTest != 0:
        chosenInputFile = 'dataTest'
    
    # Import data from file (allows for large number of objects)
    loadPath = myPath + chosenInputFile + '.csv';
    
    print("\nLoading data from " + loadPath);
    
    try:
        dataFrame = pd.read_csv(loadPath);
    except FileNotFoundError:
        print("File not found.");
    except pd.errors.EmptyDataError:
        print("No data in file.");
    except pd.errors.ParserError:
        print("Unable to parse file. \nPlease make sure data is formatted correctly.");
    except Exception:
        print("An unknown error occured during loading.");
        
    print("Data imported");
    
    if dropDuplicates:
        df_filtered = dataFrame.drop_duplicates(ignore_index=True);
        if not len(dataFrame) == len(df_filtered):
            print("Warning: duplicate objects removed");
        dataFrame = df_filtered;
        
    return dataFrame, chosenInputFile;
      
## Convert dataFrame to dict 
def dataFrameToNumpyDict(dataFrame):
    data = dataFrame.to_dict(orient='list');
    for key in data:
        data[key] = np.array(data[key]);   
    return data;
    
## Check if file with name filePath.extension exists and ask to overwrite
def doesFileExist(filePath, extension):
    while os.path.isfile(filePath):
        print("\nThe file " + filePath + " already exists. \nWould you like to overwrite it? Y/N");

        user = input();
        if user != "Y" and user != "y":
            print("Please choose an alternative file name:")
            filePath = myPath + input() + extension;  
        else:
            break;  
    return filePath;
        
## Output data to csv file
def saveData(dataFrame, chosenOutputFile):
    savePath = myPath + chosenOutputFile + '.csv';
    savePath = doesFileExist(savePath, '.csv');        
    df.to_csv(savePath, encoding='utf-8', index=True, header=True);
    print('\nData saved to ' + savePath);
      
      
### Utility Functions ############################################################################################################

## Rescale quantities
def dataRescale(dataDict, scale):
    for key in dataDict:
        dataDict[key]*= scale;
       
       
## Check if column headings in dataRequired (list) are present in inputData (dictionary)
def hasRequiredData(inputData, dataRequired):
        for item in dataRequired:
            if item not in inputData:
                raise Exception("Please ensure that the input file has a column with heading: " + item); 
 
 
## Plot vectors on graph
def plotVectors(xPosition, yPosition, xData, yData, labels, vectorScale):
    fig, ax = plt.subplots();
    figurePath = myPath + inputFile + r'_' + labels[3] + '.png';
    figurePath = doesFileExist(figurePath,'.png');
    
    if vectorScale == 0:
        vectorScale = np.sqrt(xData*xData + yData*yData); # entrywise norms
        vectorScale[np.nonzero(vectorScale)] = 15*np.reciprocal(vectorScale[np.nonzero(vectorScale)]); # handle objects with vector zero

    for i in range (0,len(xPosition)):
        ax.quiver(xPosition, yPosition, vectorScale*xData,vectorScale*yData, angles='xy',scale_units='xy',scale=1,color='r');
        
    ax.set_axisbelow(True);
    plt.grid();
    plt.title(labels[0]);
    plt.xlabel(labels[1]);
    plt.ylabel(labels[2]);
        
    fig.gca().set_aspect("equal");
    fig.savefig(figurePath);
    plt.close(fig);
    print('\nfigure saved to ' + figurePath);
 
 
## Unit test against data provided in exercise (pass if all true)
def testData(dataActual, dataTest):  

    a = abs(dataActual - dataTest) <= testTolerance;
    print(dataActual);
    print(a);
    if (np.prod(a) == 0):
        print("Test failed");
    else:
        print("Test passed");
        

### Acceleration Code #####################################################################################################

## Naive algorithm for computing acceleration with O(n^2) complexity (in non SI units)
def naiveAcceleration(xPosition, yPosition, masses): 
    
    numberObjects = len(masses)
    xAcceleration = np.zeros(numberObjects);
    yAcceleration = np.zeros(numberObjects);
    
    for i in range(1,numberObjects):
        for j in range(0,i):
            
            changeInPosition = np.array([xPosition[j] - xPosition[i] ,yPosition[j] - yPosition[i]]);   
            
            # Manage objects being in same position (avoid divide by zero)
            if (np.any(changeInPosition)):
                radiusCubed = np.reciprocal(np.linalg.norm(changeInPosition)); # Could use fast inverse sqrt in c++
                radiusCubed = radiusCubed * radiusCubed * radiusCubed;
            else:
                radiusCubed = 0;
                print("Warning: 2 objects in position (" + str(xPosition[i]) + "," + str(yPosition[i]) + ").");
              
            # Update acceleration from objects i and j interacting
            xAcceleration[i] += masses[j] * changeInPosition[0] * radiusCubed;
            xAcceleration[j] -= masses[i] * changeInPosition[0] * radiusCubed;
            yAcceleration[i] += masses[j] * changeInPosition[1] * radiusCubed;
            yAcceleration[j] -= masses[i] * changeInPosition[1] * radiusCubed;  
      
    print('Acceleration computed.');
    return {"xAcceleration (ms^-2)": xAcceleration, "yAcceleration (ms^-2)":yAcceleration};
  

## Barnes Hut Algorithm (in non SI units)
# TODO add code
def barnesHutAcceleration(xPosition, yPosition, masses):
    return 0;
    



## Wrapper function (compute, test, plot, rescale)
def accelerationWrapper(data, mode):
    
    # Ensure necessary data present in input file
    print("\nComputing acceleration");
    requiredData = ["xPosition (au)","yPosition (au)","mass (M0)"];
    hasRequiredData(data, requiredData);    

    # Set algorithm for computing acceleration
    if mode == 'naive':
        acceleration = naiveAcceleration(data[requiredData[0]],data[requiredData[1]],data[requiredData[2]]);
    elif mode == 'bh':
        acceleration = barnesHutAcceleration(data[requiredData[0]],data[requiredData[1]],data[requiredData[2]]);
    else:
        raise Exception("Parameter accelerationMode must be set to either 'naive' or 'bh' (with quotes)");

    # Run unit test
    if isTest != 0:
        hasRequiredData(data, ["xAccelerationTest","yAccelerationTest"]);
        testData(np.concatenate((acceleration["xAcceleration (ms^-2)"], acceleration["yAcceleration (ms^-2)"])),np.concatenate((data["xAccelerationTest"], data["yAccelerationTest"])));
        
    # Plot acceleration
    accelerationFigureLabels = ['Acceleration vectors of particles in ' + str(len(data["xPosition (au)"])) + '-body system', requiredData[0], requiredData[1], 'acceleration']
    plotVectors(data[requiredData[0]],data[requiredData[1]],acceleration["xAcceleration (ms^-2)"], acceleration["yAcceleration (ms^-2)"],accelerationFigureLabels,arrowScale);
    
    dataRescale(acceleration, accelerationScale);
    return acceleration;

  
#### Execution

# load data, clean, then convert to numpy
df, inputFile = loadData(inputFile, isDropDuplicates); 
df = dataFrameToNumpyDict(df);

# Perform computations
df.update(accelerationWrapper(df,accelerationMode));

# Convert back to dataFrame and export
df = pd.DataFrame.from_dict(df);
saveData(df, outputFile);

input("Press enter to close.");
