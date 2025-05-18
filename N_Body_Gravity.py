#### import potentially useful libraries #################################################################################
import math
import argparse
import numpy as np
import numpy.typing as npt
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Any
from typing import Hashable


#### Version 3 (argparse and type hinting) ################################

### (Global) Constants 
gravitationalConstant: float = 6.7e-11;
astronomicalUnit: float = 1.5e11
solarMass: float = 2e30;

accelerationScale: float = gravitationalConstant * solarMass / (astronomicalUnit * astronomicalUnit); # Convert units to SI (scales by ~e-3)

myPath: str = os.path.dirname(os.path.abspath(__file__)) + r'/';


### File I/O ############################################################################################################

## Load in data from csv file
def loadData(chosenInputFile: str, checkIfTest: bool) -> tuple[pd.DataFrame,str]:
    # Change input file to test version if selected
    if checkIfTest != 0:
        chosenInputFile = 'dataTest'
    
    # Import data from file (allows for large number of objects)
    loadPath: str = myPath + chosenInputFile + '.csv';
    
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
    return dataFrame, chosenInputFile;
    
## Clean up data (remove duplicates)
def removeDuplicates(dataFrame: pd.DataFrame, dropDuplicates: bool) -> pd.DataFrame:
    if dropDuplicates:
        df_filtered = dataFrame.drop_duplicates(ignore_index=True);
        if not len(dataFrame) == len(df_filtered):
            print("Warning: duplicate objects removed");
        dataFrame = df_filtered;
    return dataFrame;
      
## Convert dataFrame to dict 
def dataFrameToNumpyDict(dataFrame: pd.DataFrame) -> dict[Hashable,Any]:
    data: dict[Hashable,Any] = dataFrame.to_dict(orient='list');
    for key in data:
        data[key] = np.array(data[key]);   
    return data;
    
## Check if file with name filePath.extension exists and ask to overwrite
def doesFileExist(filePath: str, extension: str) -> str:
    while os.path.isfile(filePath):
        print("\nThe file " + filePath + " already exists. \nWould you like to overwrite it? Y/N");

        user: str = input();
        if user != "Y" and user != "y":
            print("Please choose an alternative file name:")
            filePath = myPath + input() + extension;  
        else:
            break;  
    return filePath;
        
## Output data to csv file
def saveData(dataFrame: pd.DataFrame, chosenOutputFile: str) -> None:
    savePath: str = myPath + chosenOutputFile + '.csv';
    savePath = doesFileExist(savePath, '.csv');        
    df.to_csv(savePath, encoding='utf-8', index=True, header=True);
    print('\nData saved to ' + savePath);
      
      
### Utility Functions ############################################################################################################

## Rescale quantities
def dataRescale(dataDict: dict[Hashable, Any], scale: float) -> dict[Hashable,Any]:
    for key in dataDict:
        dataDict[key]*= scale;
    return dataDict;
       
## Check if column headings in dataRequired (list) are present in inputData (dictionary)
def hasRequiredData(inputData, dataRequired: list[str]) -> None:
        for item in dataRequired:
            if item not in inputData:
                raise Exception("Please ensure that the input file has a column with heading: " + item); 
 
## Plot vectors on graph
def plotVectors(xPosition: npt.NDArray[np.float64], yPosition: npt.NDArray[np.float64], xData: npt.NDArray[np.float64], yData: npt.NDArray[np.float64], labels: list[str], scaleOfArrow: int) -> None:
    fig, ax = plt.subplots();
    figurePath = myPath + labels[4] + r'_' + labels[3] + '.png';
    figurePath = doesFileExist(figurePath,'.png');
    
    vectorScale: npt.NDArray[np.float64] = np.full(len(xPosition),scaleOfArrow);
    if scaleOfArrow == 0:
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
def testData(dataActual: npt.NDArray[np.float64], dataTest: npt.NDArray[np.float64], toleranceForTest: float) -> None:  
    a = abs(dataActual - dataTest) <= toleranceForTest;
    print(dataActual);
    print(a);
    if (np.prod(a) == 0):
        print("Test failed");
    else:
        print("Test passed");
        

### Acceleration Code #####################################################################################################

## Naive algorithm for computing acceleration with O(n^2) complexity (in non SI units)
def naiveAcceleration(xPosition: npt.NDArray[np.float64], yPosition: npt.NDArray[np.float64], masses:npt.NDArray[np.float64]) -> dict[Hashable, Any]: 
    
    numberObjects: int = len(masses)
    xAcceleration: npt.NDArray[np.float64] = np.zeros(numberObjects);
    yAcceleration: npt.NDArray[np.float64] = np.zeros(numberObjects);
    
    for i in range(1,numberObjects):
        for j in range(0,i):
            
            changeInPosition: npt.NDArray[np.float64] = np.array([xPosition[j] - xPosition[i] ,yPosition[j] - yPosition[i]]);   
            
            # Manage objects being in same position (avoid divide by zero)
            radiusCubed: float = 0;
            if (np.any(changeInPosition)):
                radiusCubed = np.reciprocal(np.linalg.norm(changeInPosition)); # Could use fast inverse sqrt in c++
                radiusCubed = radiusCubed * radiusCubed * radiusCubed;
            else:
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
def barnesHutAcceleration(xPosition: npt.NDArray[np.float64], yPosition: npt.NDArray[np.float64], masses: npt.NDArray[np.float64]) -> dict[Hashable,Any]:
    return {'None': np.array(0)};
    

## Wrapper function (compute, test, plot, rescale)
def accelerationWrapper(data: dict[Hashable,Any], mode: str, checkIfTest: bool, toleranceForTest: float, vectorScale: int, outputFileName: str) -> dict[Hashable, Any]:
    
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
    if checkIfTest != 0:
        hasRequiredData(data, ["xAccelerationTest","yAccelerationTest"]);
        testData(np.concatenate((acceleration["xAcceleration (ms^-2)"], acceleration["yAcceleration (ms^-2)"])),np.concatenate((data["xAccelerationTest"], data["yAccelerationTest"])), toleranceForTest);
        
    # Plot acceleration
    accelerationFigureLabels = ['Acceleration vectors of particles in ' + str(len(data["xPosition (au)"])) + '-body system', requiredData[0], requiredData[1], 'acceleration',outputFileName];
    plotVectors(data[requiredData[0]],data[requiredData[1]],acceleration["xAcceleration (ms^-2)"], acceleration["yAcceleration (ms^-2)"],accelerationFigureLabels,vectorScale);
    
    acceleration = dataRescale(acceleration, accelerationScale);
    data.update(acceleration);
    return data;

  
#### Execution
if __name__ == "__main__":
    
    ## Get custom parameter values from command line call
    parser = argparse.ArgumentParser(description="Script for computing properties (e.g. acceleration) of solar objects, with input and output data in .csv files. All arguments are optional and will use default values unless otherwise specified.");
    
    parser.add_argument("--isTest", type=bool, default=False, help="(type=boolean, default=False) Runs script in test mode if set to True.");
    parser.add_argument("--testTolerance", type=float, default=1e-8, help="(type=float, default=1e-8) Amount of error allowed in test computation before the test fails.");
    parser.add_argument("--inputFile", type=str, default='dataInput', help="(type=string, default='dataInput') Name of csv file, without extension, from which data should be read. Must contain position and mass data with appropriate headings. See readme for more information. Also accepts paths relative to script location.");
    parser.add_argument("--outputFile", type=str, default='dataOutput', help="(type=string, default='dataOutput') Name of csv file, without extension, to which the results of the computation should be saved. Also accepts paths relative to script location.");
    parser.add_argument("--accelerationMode", type=str, default='naive', help="(type=string, default='naive') Algorithm to be used when computing acceleration of objects. Options are 'naive' which uses nested for loops, and 'bh' which uses the Barnes--Hut algorithm.");
    parser.add_argument("--isDropDuplicates", type=bool, default=False, help="(type=boolean, default=False) Removes duplicate rows from the imported data when performing computations if set to true. Note, if only positions of objects match, returns a warning but does not remove duplicates.");
    parser.add_argument("--arrowScale", type=int, default=0, help="(type=integer, default=0) Allows users to scale the arrows in vector plots produced. Setting to zero normalises all arrows to the same length.");
    
    args = parser.parse_args();
    
    ## Set global values to use defaults or user input 
    isTest: bool = args.isTest;
    testTolerance: float = args.testTolerance; 
    inputFile: str = args.inputFile;
    outputFile: str = args.outputFile;
    accelerationMode: str = args.accelerationMode; 
    isDropDuplicates: bool = args.isDropDuplicates;
    arrowScale: int = args.arrowScale; 
    


# load data, clean, then convert to numpy
df, inputFile = loadData(inputFile, isTest); 
df = removeDuplicates(df, isDropDuplicates);
dfDict = dataFrameToNumpyDict(df);

# Perform computations
dfDict = accelerationWrapper(dfDict, accelerationMode, isTest, testTolerance, arrowScale, outputFile); 

# Convert back to dataFrame and export
df = pd.DataFrame.from_dict(dfDict);
saveData(df, outputFile);

input("Press enter to close.");
