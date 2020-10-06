# Reconfigurable genetic inverters using contextual dependencies

This repository contains the codes used in the manuscript.
  
## Obtaining the code

Get git https://git-scm.com/
`git clone https://github.com/lgrozinger/pyolin.git`
`cd pyolin`

### Dependencies

These dependencies are often found in the official package repositories for nix systems.

## Required
- Get Python3.6+ https://www.python.org/downloads/release/python-380/

## Optional (for plotting)
- Get gnuplot 5+ http://www.gnuplot.info/
- Get texlive https://www.tug.org/texlive/ (or equivalent LaTeX)
- Get imagemagick https://imagemagick.org/index.php

on debian-based systems these dependencies are available from the official package repositories, and can be installed with:

`apt-get update && apt-get install python3 python3-pip gnuplot texlive-base texlive-fonts-recommended imagemagick`

the required python packages can then be installed with

`python3 -m pip install --upgrade pip && python3 -m pip install jupyter pandas scipy matplotlib similaritymeasures seaborn`

### OR

A Dockerfile is provided for convenience:

Get Docker https://docs.docker.com/engine/docker-overview/

Build once with `docker build -t pyolin .`
Run with `docker run -it -v "$(pwd)":/pyolin pyolin /bin/bash`

## Running the code

after `cd pyolin`, running `python3 produce_figures.py full-update` will do the analysis from the manuscript and produce the plots found there.

The code can also be used as a python package. See https://github.com/lgrozinger/pyolin/blob/master/notebooks/example.ipynb for example usage.

### Data Files
The preprocessed cytometry data is located at  https://github.com/lgrozinger/pyolin/blob/master/standardised_cheeky.csv . This data was processed using the FlowScatt package https://github.com/rstoof/FlowScatt . The analysis in the paper can be performed on other datasets, providing it follows the format in the example dataset, by modifying the variable `CYTODATA` in `__init__.py` to point at the filename of the data to be analysed.

## SBOL Files
SBOL files for the constructs used in the study are found in the `results/sbol/` directory with the extension `.xml`
