# Acceleration of Objects in N-Body Systems (N-Body Gravity)

<a id="readme-top"></a>

<details>
  <summary>Table of Contents</summary>
  <ol>
  <li> <a href="#about">About</a></li>
  <li> <a href="#getting-started">Getting Started</a>
    <ul>
      <li> <a href="#requirements">Requirements</a></li>
      <li> <a href="#installation">Installation</a></li>
      <li> <a href="#configuring-settings">Configuring Settings</a></li>
    </ul>  </li>
  <li> <a href="#contact">Contact</a></li>
  <li> <a href="#acknowledgements-and-references">Acknowledgements and References</a></li>
  </ol>
</details>

## About

This project allows for the computation of acceleration of objects within many object systems, given the masses and positions of said objects in a `.csv` file. The code has been designed using functional programming paradigms, such that the end-user may easily add functions to compute additional derived quantities. The contents of this repository were developed as part of an interview assessment for the role of Scientific Software Engineer at the Met Office, UK and may be made private at their request.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

This section details all you need to know about downloading and using the `N_Body_Systems.py` script. To get a local copy of this code up and running, simply follow thte steps below.

### Requirements

- Python (3.9.6 or newer)

- Additional libraries
  - Numpy
  - Matplotlib
  - Pandas
 
- An IDE 

### Installation

1. Before downloading the `N_Body_Systems` script, please ensure that you have all of the necessary requirements, beginning with an installation of Python ver. 3.9.6 or newer. Older versions are not supported but may still work. For more information on installing Python, see the <a href="https://www.python.org/downloads/">Official Python Website</a> or refer to the <a href="https://github.com/PackeTsar/Install-Python/blob/master/README.md">Handy Guide</a> provided by PackeTsar. 

2. Now that you have Python installed, you will need to install the additional libraries listed above. This can be done using the following pip command in the system terminal/command prompt:

    ```sh
        python -m pip install "name-of-package"
    ```
    where "name-of-package" should be repaced with "numpy", "matplotlib" and "pandas" respectively (with quotes). In order to update existing packages, use the command
    
    ```sh
        python -m pip install --upgrade "name-of-package"
    ```

3. Once you have installed Python and the required libraries, you will also need an IDE (Integrated Development Environment). The standard Python installation comes with its own, namely IDLE, which is sufficient to run the code in this repository. However you may wish to install another, for example <a href="https://notepad-plus-plus.org/">Notepad++</a> or <a href="https://www.spyder-ide.org/">Spyder</a>, to aid in your own development.
   
    Note: an IDE is only required if you wish to specify your own input and output files, add your own functions to compute other derived quantities, or change the settings detailed below. If you only wish to demo the code, simply double clicking on the file `N_Body_Systems.py` will run the code on the file `dataInput.csv` and save the output to `dataOutput.csv` and `dataInput_acceleration.png`.

4. Finally, you will need to either download or clone this repository, or download the files. In order to clone the repository, use the following command:
    ```sh
        git clone https://github.com/LewisN3142/N_Body_Gravity.git
    ```
    Alternatively, by clicking the green "code" button on the top right of the repository window, you can choose to either download the repository as a `.zip` folder, open with Github desktop, or clone via https.
   
    Note: it is important that the files in this repository are stored in the *same* folder, so that they have the same relative path.

5. Now you're ready to use the script! To view the demo code, simply double click the `N_Body_Gravity.py` file you downloaded, or call the script in the terminal/command prompt. 


### Configuring Settings

The `N_Body_Gravity.py` script comes with a number of easily customisable parameters, listed at the top of the script file, which can be edited in your IDE of choice. These parameters are:

``` sh
    isTest
    testTolerance
    inputFile
    outputFile
    arrowScale
    accelerationMode
    isDropDuplicates
```

 - The `isTest` parameter is a boolean which triggers testing mode when set `1` and standard mode when set to `0`. Testing mode takes input data from the `dataTest.csv` and computes the acceleration of the bodies listed there. The result of the computation is then compared to a pre-computed solution (stored in `dataTest.csv`) and checked to see if it is within tolerance. The results of the test will be output to the terminal/command prompt/console. Note that the unit test utilises duplicate objects, so will fail if `isDropDuplicates` is set to `1`.

 - The `testTolerance` parameter allows the user to set the tolerance for the above unit test. That is, how close the output of the script has to be to the pre-computed solution for the code to pass the test. The default value is `1e-8`.

 - The `inputFile` parameter allows the user to set the name of the file which should be read for the positions and masses of the objects in the systems. The file must be of `.csv` type (comma separated value) and should be stored in the same folder as the `N_Body_System.py` file. In order to compute the acceleration, the `.csv` file must contain columns with headings `xPosition (au)`, `yPosition (au)`, and `mass (M0)` and will return an exception if this is not the case. The default value is the string `'dataInput'`.

 - The `outputFile` parameter allows the user to set the name of the `.csv` file to which the data should be saved. The default value is the string `'dataOutput'`. If the file does not already exist, it will be created, whereas if the file does already exist, you will be prompted to overwrite it or provide an alternative file name. 

Note: Thie `inputFile` and `outputFile` parameters also take relative paths (taken relative to the `N_Body_System.py` file) if you do not wish to store your input and output files in this folder. 

 - The `arrowScale` parameter allows the user to increase or decrease the arrows in the plot produced by an overall scale factor. Setting `arrowScale` to `0` sets all of the arrows to the same length (namely 15 units). The plot is saved to the file `inputFile_acceleration.png`, where inputFile is replaced by the value of the `inputFile` parameter, unless this file already exists, in which case you will be prompted to overwrite it or provide an alternative file name.

 - The `accelerationMode` parameter allows the user to choose between two means of computing the acceleration of the objects, namely `"naive"` and `"bh"`. The default value is the string `"naive"`, which causes the code to compute the acceleration of each object explicitly using nested for loops at time complexity `O(n^2)`. The value `"bh"` causes the script to compute the acceleration using the Barnes--Hut approximation algorithm, which, given an accelerating object and several source objects, groups source objects which are far away together, representing their contribution to the acceleration of the accelerating object by that of a hypothetical object with their total mass, situated at their center of mass.

 -  The `isDropDuplicates` parameter is a boolean, which, when set to `1`, removes duplicate objects from the input data. Note that if the objects are in the same position but have different masses, the code will still execute regardless of the value of `isDropDuplicates`, but will also print a warning to console with the position at which the two objects coincide. The default value is `0`.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Should you have any comments, queries, or requests, please feel free to contact me using the form on my <a href="https://lewisn3142.github.io/contact_page/contact.html">website</a>.
Alternatively, you may raise an issue on this project's <a href="https://github.com/LewisN3142/N-Body-Gravity/issues">issues page</a>.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgements and References

I would like to thank the staff at the Met Office for inviting me to interview and setting the exercise that led to me producing this programme. The experience of diving back into python and solving this problem, while keeping in mind software engineering principles such as unit testing, versioning, and modularity was a great way to learn and consolidate my knowledge.

The references below were particularly useful in my research &mdash; I recommend reading these for more context on the problem itself, especially the Barnes&ndash;Hut algorithm:

- Ventimiglia, T. and Wayne, K., \emph{The Barnes-Hut Algorithm}, arborjs, (2011): <a href="https://arborjs.org/docs/barnes-hut">link</a>.
- BaGreal2, \emph{gravitation-particles}, Github, (2023): <a href="https://github.com/BaGreal2/gravitation-particles">link</a>.
-

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License and Terms

The material contained within this repository (including but not limited to code, program files, and their documentation) is distributed under a CC-BY-NC-SA license. The material contained within this repository is believed to be safe, true, and accurate. We accept no responsibility for losses incurred, whether directly or indirectly, resulting from incorrect use of this material. Should you wish to license this material under any other terms, claim copyright to any material presented herein, or have any issue with the material herein, please [Contact Us](https://lewisn3142.github.io/contact_page/contact.html).

<p align="right">(<a href="#readme-top">back to top</a>)</p>
