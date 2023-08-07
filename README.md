# Infection
## Simulation Model of a Disease spreading throughout a population
## Final Project for the Código Facilito's 2023 Advanced Python Bootcamp
#
![infection](https://github.com/Underdoge/pf_bpa_cf_privado/assets/12192446/8463fb75-2873-4556-bc5f-5ac6a7b62b29)

# Installation
Open up a Terminal (Linux/macOS) or PowerShell (Windows) and enter the following commands:
### Cloning the repository
```sh
git clone https://github.com/underdoge/infection

cd infection
```
### Creating the virtual environment
```sh
python -m venv venv
```
### Activating the virtual environment on macOS / Linux
```sh
source venv/bin/activate
```
### Activating the virtual environment on Windows
```powershell
.\venv\Scripts\Activate.ps1
```
### Installing on macOS / Linux
```sh
pip install -r requirements_macos_linux.txt
```
### Installing on Windows
```powershell
pip install -r requirements_win.txt
```
#
# Running the program
```sh
python main.py
```
#
# Running the unit tests
```sh
pytest -v
```
#
# Usage
## Infection Probability
- The Infection Probability value determines how likely a healthy individual is to get infected upon contact with an infected one.
- Adjust the Infection Probability slider to the desired value, the default is 0.2.
- Only new individuals will be created with the selected value, previously created individuals are not affected when changing the slider vaslue.
- Meaning each individual keeps its own infection probability throughout the simulation.
## Adding or Removing Individuals 
- Press the +1 Healthy button to add a new healthy individual to the simulation.
- Press the +1 Infected button to add a new infected individual to the simulation.
- Press the Reset button to remove all individuals and reset the simulation parameters.
#
# Requirements
- Python 3.6 or greater
