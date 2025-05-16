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
  
- An IDE 

- Additional libraries
  - Numpy
  - Matplotlib
  - Pandas

### Installation

Before downloading the `N_Body_Systems` script, please ensure that you have all of the necessary requirements, beginning with an installation of Python ver. 3.9.6 or newer. Older versions are not supported but may still work. For more information on installing Python, see the <a href="https://www.python.org/downloads/">Official Python Website</a> or refer to the <a href="https://github.com/PackeTsar/Install-Python/blob/master/README.md">Handy Guide</a> provided by PackeTsar. 

Once you have installed Python, you will also need an IDE (Integrated Development Environment). The standard Python installation comes with its own, namely IDLE, which is sufficient to run the code in this repository. However you may wish to install another, for example <a href="https://notepad-plus-plus.org/">Notepad++</a> or <a href="https://www.spyder-ide.org/">Spyder</a>, to aid in your own development. 

Note: an IDE is only required if you wish to specify your own input and output files, add your own functions to compute other derived quantities, or change the settings detailed below. If you simply wish to demo the code, simply double clicking on the file `N_Body_Systems.py` will run the code on the test file `dataTest.csv`.


### Configuring Settings

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
