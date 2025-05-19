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


#### Version 4 (Barnes-Hutt algorithm) ################################

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
        
    # Check if all columns of data are same length i.e. data is complete (could do some cleanup here at later date)
    if dataFrame.isnull().values.any():
        raise Exception("Parsed file has missing data. Ensure that you provide positions, masses, etc for all objects.");
        
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
def hasRequiredData(inputData: dict[Hashable,Any], dataRequired: list[str]) -> None:
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
            
            changeInPosition: npt.NDArray[np.float64] = np.array([xPosition[j] - xPosition[i], yPosition[j] - yPosition[i]]);   
            
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
  
  
## Barnes Hut Algorithm (in non SI units) ###########################################################################################
class Node:
    position = None; # position of centre of mass of node
    mass = None;
    children = None;
    sideLength = None;
    centre = None; # physical centre of box bounding node
    
    def __init__(self, position: npt.NDArray[np.float64], mass: float, sideLength:float, centrePoint: npt.NDArray[np.float64]) -> None:
        self.position = position;
        self.mass = mass;
        self.sideLength = sideLength;
        self.centre = centrePoint;
    
# function to compute overall bounding box (returns side-length and centre)
def boundingBox(xPosition: npt.NDArray[np.float64], yPosition: npt.NDArray[np.float64]) -> tuple[float,float]:
    coordinates: npt.NDArray[np.float64] = np.concatenate((xPosition,yPosition));
    maxCoord: float = np.amax(coordinates);
    minCoord: float = np.amin(coordinates); 
    centreCoord: float = 0.5 * (maxCoord + minCoord);
    boxWidth = abs(maxCoord - minCoord);
    return boxWidth, centreCoord;

# function to work out what quadrant object should go in (returns quadrant, signs of x and y relative to 'origin')
def whatQuadrant(position:npt.NDArray[np.float64], centreCoord: npt.NDArray[np.float64]) -> tuple[int, npt.NDArray[np.int64]]:
    quadrantNumber: int = 1;
    quadrantDirection: npt.NDArray[np.int64] = np.array([1,1]); # top right or centre
    if (position[0] < centreCoord[0]) and (position[1] >= centreCoord[1]): # top left
        quadrantNumber = 0;
        quadrantDirection = np.array([-1,1]);
    elif (position[0] > centreCoord[0]) and (position[1] <= centreCoord[1]): # bottom right
        quadrantNumber = 2;
        quadrantDirection = np.array([1,-1]);
    elif (position[0] <- centreCoord[0]) and (position[1] < centreCoord[1]): #bottom left
        quadrantNumber = 3;
        quadrantDirection = np.array([-1,-1]);
    return quadrantNumber, quadrantDirection;
    
# Add each object to the quadtree
def insertNode(root: Node, nodePosition: npt.NDArray[np.float64], nodeMass: float) -> Node:
    # if node is empty, node stores single object
    if root.mass == None: 
        root.mass = nodeMass;
        root.position = nodePosition;
        return root;
      
    # raise exception if two objects in same position
    elif (root.mass == nodeMass and (root.position == nodePosition).all()):
        raise Exception("Two objects in same position, unable to use Barnes--Hut algorithm.");    
        
    # if node is not empty but has no children, create children and move parent object to child
    elif root.children == None:
        root.children = [None,None,None,None];
        
        # position object originally in parent node as child
        oldNodeQuadNumber, oldNodeQuadDirection = whatQuadrant(root.position,root.centre);
        oldNodeCentre = root.centre + oldNodeQuadDirection * np.full(2,0.25*root.sideLength);
        root.children[oldNodeQuadNumber] = Node(root.position, root.mass, 0.5*root.sideLength, oldNodeCentre);
        
    # position new object either as child, or as grandchild of root node
    newNodeQuadNumber, newNodeQuadDirection = whatQuadrant(nodePosition,root.centre);
    newNodeCentre = root.centre + newNodeQuadDirection * np.full(2,0.25*root.sideLength);
    if root.children[newNodeQuadNumber] == None: 
        root.children[newNodeQuadNumber] = Node(None, None, 0.5*root.sideLength, newNodeCentre);
    insertNode(root.children[newNodeQuadNumber], nodePosition, nodeMass); 
        
    # update mass and position of root node
    root.position = (root.mass * root.position + nodeMass * nodePosition) / (root.mass + nodeMass);
    root.mass = root.mass + nodeMass;
    return root;
    
    
# Compute acceleration of single object using Barnes--Hut algorithm
def barnesHutAccelerationObject(root: Node, objectPosition: npt.NDArray[np.float64], theta:float) -> npt.NDArray[np.float64]:
    if (root.position == objectPosition).all():
        return 0, 0;
        
    sideLength: float = root.sideLength;
    directionToRoot: npt.NDArray[np.float64] = root.position - objectPosition;
    distanceToRoot: float = np.linalg.norm(directionToRoot);
    accelerationFromNode: npt.NDArray[np.float64] = np.zeros(2);
    
    if (sideLength / distanceToRoot < theta or root.children is None): # if node far away or a single object
        accelerationFromNode = root.mass * directionToRoot * np.reciprocal(distanceToRoot*distanceToRoot*distanceToRoot)
    else:
        for child in root.children:
            if child is not None:
                accelerationFromNode += barnesHutAccelerationObject(child,objectPosition,theta);
    return accelerationFromNode;
    

# Compute acceleration of all objects using Barnes--Hut algorithm
def barnesHutAcceleration(xPosition: npt.NDArray[np.float64], yPosition: npt.NDArray[np.float64], masses: npt.NDArray[np.float64], theta: float) -> dict[Hashable,Any]:
    
    numberObjects = len(xPosition);
    xAcceleration: npt.NDArray[np.float64] = np.zeros(numberObjects);
    yAcceleration: npt.NDArray[np.float64] = np.zeros(numberObjects);
    
    # Create quadtree
    boundingBoxWidth, centreCoordinate = boundingBox(xPosition,yPosition);
    quadtree: Node = Node(None, None, boundingBoxWidth, np.full(2,centreCoordinate));
    
    for i in range(0,numberObjects):
        quadtree: Node = insertNode(quadtree, np.array([xPosition[i], yPosition[i]]), masses[i]);
        
    if quadtree.mass == None:
        return {"xAcceleration (ms^-2)": np.empty(numberObjects), "yAcceleration (ms^-2)":np.empty(numberObjects)} 
    
    # Compute accelerations 
    for i in range(0,numberObjects):
        objectAcceleration = barnesHutAccelerationObject(quadtree, np.array([xPosition[i],yPosition[i]]), theta);
        xAcceleration[i] = objectAcceleration[0];
        yAcceleration[i] = objectAcceleration[1];
        
    print('Acceleration computed.');
    return {"xAcceleration (ms^-2)": xAcceleration, "yAcceleration (ms^-2)":yAcceleration};
    


## Wrapper function (compute, test, plot, rescale) ###############################################################################################
def accelerationWrapper(data: dict[Hashable,Any], mode: str, checkIfTest: bool, toleranceForTest: float, vectorScale: int, outputFileName: str, theta:float) -> dict[Hashable, Any]:
    
    # Ensure necessary data present in input file
    print("\nComputing acceleration");
    requiredData = ['xPosition (au)','yPosition (au)','mass (M0)'];
    hasRequiredData(data, requiredData);    

    # Set algorithm for computing acceleration
    if mode == 'naive':
        acceleration = naiveAcceleration(data[requiredData[0]],data[requiredData[1]],data[requiredData[2]]);
    elif mode == 'bh':
        acceleration = barnesHutAcceleration(data[requiredData[0]],data[requiredData[1]],data[requiredData[2]], theta);
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
    parser.add_argument("--BarnesHutTheta", type=float, default=0.2, help="(type=float, default=0.5) Parameter to tune the distance from an object at which other objects are deemed far away. Higher values increase speed but decrease accuracy, with typical values being around 0.5. A value of 0 results in no grouping of objects and is functionally the same as the naive approach.");
    
    args = parser.parse_args();
    
    ## Set global values to use defaults or user input 
    isTest: bool = args.isTest;
    testTolerance: float = args.testTolerance; 
    inputFile: str = args.inputFile;
    outputFile: str = args.outputFile;
    accelerationMode: str = args.accelerationMode; 
    isDropDuplicates: bool = args.isDropDuplicates;
    arrowScale: int = args.arrowScale;
    BarnesHutTheta: float = args.BarnesHutTheta;
    


# load data, clean, then convert to numpy
df, inputFile = loadData(inputFile, isTest); 
df = removeDuplicates(df, isDropDuplicates);
dfDict: dict[Hashable,Any] = dataFrameToNumpyDict(df);

# Perform computations
dfDict = accelerationWrapper(dfDict, accelerationMode, isTest, testTolerance, arrowScale, outputFile, BarnesHutTheta); 

# Convert back to dataFrame and export
df = pd.DataFrame.from_dict(dfDict);
saveData(df, outputFile);

input("Press enter to close.");
