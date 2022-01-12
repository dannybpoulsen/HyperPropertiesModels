# Statistical Model Checking for Probabilistic Hyperproperties of Real-Valued Signals

This is the companion repository for the article _Statistical Model
Checking for Probabilistic Hyperproperties of Real-Valued Signals_. It
contains the models used throughout the paper and python scripts for reproducing the results. 


## Requirements  
### Uppaal  
The reproduction package relies on a development version of Uppaal. 
A stable release from [Uppaal](https://uppaal.org) will not work. 

- The uppaal binary can be downloaded from [Here]("https://people.cs.aau.dk/~bc37lv/uppaal/uppaal-hyper/uppaal-DEV-stratego-hyper-linux64.zip") and must be unpacked in the `bin` sub-directory of this repository.  
- If the python script cannot find uppaal-distribution in `bin` it tries to download and unpack it itself.



## Python  
The Python scripts requires the packages

- cycler==0.11.0
- fonttools==4.28.5
- kiwisolver==1.3.2
- matplotlib==3.5.1
- numpy==1.22.0
- packaging==21.3
- Pillow==9.0.0
- pyparsing==3.0.6
- python-dateutil==2.8.2
- scipy==1.7.3
- six==1.16.0
- tabulate==0.8.9

## Reproduction
Reproducing the graphs and tables of the paper is merely a matter of running `python generate.py`. 
This will find the  binary of Uppaal, and run all the experiments of the paper (and a few extra). 

After running the scripts the results are available in the created results sub-folder. 
The figure of the paper and the generated plots / results can mapped according to the table below:

|------------|---------------------------------------------|
| Figure     | File                                        |
|------------|---------------------------------------------|
| Figure 2a  | `results/Login/example3/login_sucesfil.pdf` |
| Figure 2b  | `results/Login/example3/login_failed.pdf`   |
|------------|---------------------------------------------|
| Table 1a   | `results/Login/example4/table.txt`          |
| Table 1a   | `results/Login/example5/table.txt`          |
|------------|---------------------------------------------|
| Figure 6 a | `results/rsa/rsa/iteration/probs.png`       |
| Figure 6   | `results/rsa/rsa/iteration/runtime.png`     |
|------------|---------------------------------------------|

## Models  
The models used in the paper is available in the `./models` subdirectory of the repository. 

