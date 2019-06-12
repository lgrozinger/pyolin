### Dockerised Notebook

Get Docker https://docs.docker.com/engine/docker-overview/
Get git https://git-scm.com/
`git clone https://github.com/lgrozinger/pyolin.git`
`cd pyolin`

Build once with `./docker_build.sh`
Run every time with `./docker_notebook_run.sh <PATH/TO/DATA/DIR>`
Point your web browser at the URL jupyter gives on stdout.

### Un-dockerised Notebook

Install Python3.6 or newer. 
Install Jupyter.
`git clone https://github.com/lgrozinger/pyolin.git`
Run the notebook.

### Data Files

Scripts expect flow cyto .csv files, with a certain naming convention, which follows the conventions in the UCF files.

`cd <PATH/TO/CSV/DATAFILES/>`
`mkdir <PATH/TO/PYOLIN/data> ; ./<PATH/TO/PYOLIN/file_standardise.sh <PATH/TO/PYOLIN/data>`

Should sort them out and put new files in `<PATH/TO/PYOLIN/data>` directory.
