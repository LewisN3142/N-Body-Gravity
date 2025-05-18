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

This project allows for the computation of acceleration of objects within many object systems, given the masses and positions of said objects in a `.csv` file. Running the code also produces a `.png` graphic showing the direction of the acceleration of each object. The code has been designed using functional programming paradigms, such that the end-user may easily add functions to compute additional derived quantities. The contents of this repository were developed as part of an interview assessment for the role of Scientific Software Engineer at the Met Office, UK and may be made private at their request.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

This section details all you need to know about downloading and using the `N_Body_Systems.py` script. To get a local copy of this code up and running, simply follow thte steps below.

### Requirements

- Python (3.9.6 or newer)

- Additional libraries

  - Numpy
  - Matplotlib
  - Pandas
  - Pandas Stubs (if you use mypy)
  - argparse

### Installation

1. Before downloading the `N_Body_Systems` script, please ensure that you have all of the necessary requirements, beginning with an installation of Python ver. 3.9.6 or newer. Older versions are not supported but may still work. For more information on installing Python, see the <a href="https://www.python.org/downloads/">Official Python Website</a> or refer to the <a href="https://github.com/PackeTsar/Install-Python/blob/master/README.md">Handy Guide</a> provided by PackeTsar.

2. Now that you have Python installed, you will need to install the additional libraries listed above. This can be done using the following pip command in the system terminal/command prompt:

   ```sh
       python -m pip install "name-of-package"
   ```

   where "name-of-package" should be repaced with "numpy", "matplotlib", "pandas", and "pandas-stubs" respectively (with quotes). In order to update existing packages, use the command

   ```sh
       python -m pip install --upgrade "name-of-package"
   ```

3. Once you have installed Python and the required libraries, you may also wish to install an IDE (Integrated Development Environment), to edit the code itself. The standard Python installation comes with its own, namely IDLE, which is sufficient, however alternatives, such as <a href="https://notepad-plus-plus.org/">Notepad++</a> or <a href="https://www.spyder-ide.org/">Spyder</a>, also exist.

4. Finally, you will need to either download or clone this repository, or download the files. In order to clone the repository, use the following command:

   ```sh
       git clone https://github.com/LewisN3142/N_Body_Gravity.git
   ```
   
   Alternatively, by clicking the green "code" button on the top right of the repository window, you can choose to either download the repository as a `.zip` folder, open with Github desktop, or clone via https.

   Note: it is important that the files in this repository are stored in the _same_ folder, so that they have the same relative path.

5. Now you're ready to use the script! To view the demo code, simply double click the `N_Body_Gravity.py` file you downloaded, or call the script in the terminal/command prompt.

### Configuring Settings

The `N_Body_Gravity.py` script includes a number of easily customisable parameters, which can be specified as optional arguments when calling the script from command prompt/terminal/console. This is done to aid the execution of the script on a large number of input files using, say, a bash script.
In particular, the script supports argparse syntax and can be called with optional arguments in the following manner

```sh
  python N_Body_Gravity.py --name_of_variable = value_of_variable --name_of_another_variable = another_value
```
where `name_of_variable` and `name_of_another_variable` are replaced with the names of the arguments you wish to specify the values of. Similarly, `value_of_variable` and `another_value` should be replaced with the values themselves. You can specify as many variables in one call as you would like by adding them to the end of the call in the same manner as above.

Note: When running the script from your preferred console, ensure that your directory is set to wherever the `N_Body_Gravity.py` script is saved or alternatively provide the relative path to `N_Body_Gravity.py` from your current active directory in the call above.

For details of the available optional arguments, their types, and their default values if not specified, run the following help command:

```sh
  python N_Body_Gravity.py -h
```

Details of the available arguments can also be found in the list below:

- `isTest` (type = bool, default = `False`): triggers testing mode when set to `True`. In testing mode, the script takes input data from `dattaTest.csv` and computes the acceleration of the bodies listed there. The result of the computation is compared to a pre-computed solution (stored in `dataTest.csv`) and checked to see if it is within tolerance. The results of the test will be output to the console. Note: the unit test utilises duplicate objects, so will fail if `isDropDuplicates` is set to `True`.

- `testTolerance` (type = float, default = `1e-8`): tolerance for unit tests, that is, how close the output of the script has to be to the pre-computede solution for the code to pass the test.

- `inputFile` (type = string, default = `'dataInput'`): allows the user to set the name of the file from which the data should be loaded. The file must be of `.csv` type and should be stored in the same folder as the `N_Body_System.py` file (or be a relative path from the script). In order to compute the acceleration, the `.csv` file must contain columns with headings `xPosition (au)`, `yPosition (au)`, and `mass (M0)` and will return an exception if this is not the case.
  
- `outputFile` (type = string, default = `'dataOutput'`): allows the user to set the name of the `.csv` file to which the data should be saved. If the file does not already exist, it will be created, whereas if the file does already exist, you will be prompted to overwrite it or provide an alternative file name.
  
-  `arrowScale` (type = int, default = `0`): allows the user to increase or decrease the length of the arrows in `.png` vector plots by an overall scale factor. Setting `arrowScale` to `0` normalises all arrows to the same length (namely 15 units). The plot is saved to the file `outputFile_acceleration.png`, where outputFile is replaced by the value of the `outputFile` parameter, unless this file already exists, in which case you will be prompted to overwrite it or provide an alternative file name.
  
- `accelerationMode` (type = string, default = `'naive'`): allows the user to choose between two means of computing the acceleration of the objects, namely `'naive'`, which uses nested for loops with time complexity `O(n^2)`, and `'bh'` which uses the Barnes--Hut approximation algorithm with time complexity `O(n log(n))`. The Barnes--Hut algorithm optimises computation of the acceleration of an object by grouping together source objects which are far enough away and replacing them with an object of the same total mass, situated at their centre of mass.

- `isDropDuplicates` (type = boolean, default = `False`): removes duplicate objects from input data when set to `True`. If the objects are in the same position but have different masses, the code will still execute regardless of the value of `isDropDuplicates`, but will also print a warning to console with the position at which the two objects coincide. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Should you have any comments, queries, or requests, please feel free to contact me using the form on my <a href="https://lewisn3142.github.io/contact_page/contact.html">website</a>.
Alternatively, you may raise an issue on this project's <a href="https://github.com/LewisN3142/N-Body-Gravity/issues">issues page</a>.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgements and References

I would like to thank the staff at the Met Office for inviting me to interview and setting the exercise that led to me producing this programme. The experience of diving back into python and solving this problem, while keeping in mind software engineering principles such as unit testing, versioning, and modularity was a great way to learn and consolidate my knowledge.

The references below were particularly useful in my research &mdash; I recommend reading these for more context on the problem itself, especially the Barnes&ndash;Hut algorithm:

- Ventimiglia, T. and Wayne, K., <em>The Barnes-Hut Algorithm</em>, arborjs, (2011): <a href="https://arborjs.org/docs/barnes-hut">link</a>.
- BaGreal2, <em>gravitation-particles</em>, Github, (2023): <a href="https://github.com/BaGreal2/gravitation-particles">link</a>.
- Wangari, E., <em>Running Python script with Arguments in the command line</em>, Medium, (2023): <a href="https://medium.com/@evaGachirwa/running-python-script-with-arguments-in-the-command-line-93dfa5f10eff">link</a>.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License and Terms

The material contained within this repository (including but not limited to code, program files, and their documentation) is distributed under a CC-BY-NC-SA license. The material contained within this repository is believed to be safe, true, and accurate. We accept no responsibility for losses incurred, whether directly or indirectly, resulting from incorrect use of this material. Should you wish to license this material under any other terms, claim copyright to any material presented herein, or have any issue with the material herein, please [Contact Us](https://lewisn3142.github.io/contact_page/contact.html).

<p align="right">(<a href="#readme-top">back to top</a>)</p>
