# Infection
## Simulation Model of a Disease spreading throughout a population
## Final Project for the Código Facilito's 2023 Advanced Python Bootcamp
<img src="https://github.com/Underdoge/infection/assets/12192446/3184df7e-d5b9-4775-8adb-05457733a40f" width="800px">

# Installation
Open up a Terminal (macOS/Linux) or PowerShell (Windows) and enter the following commands:
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
### Activating the virtual environment on Windows (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```
### Installing on macOS / Linux
```sh
pip install -r requirements_macos_linux.txt
```
### Installing on Windows (PowerShell)
```powershell
pip install -r requirements_win.txt
```
#
# Running the program
### Running the program on macOS / Linux
```sh
python3 main.py
```
### Running the program on Windows (PowerShell)
```powershell
python main.py
```
#
# Running the unit tests
Important: Running the unit tests using 'pytest -v' won't work because it doesn't add the 'infection' module to the current path, only 'python -m pytest -v' does.
### Running the unit tests on macOS / Linux
```sh
python3 -m pytest -v
```
### Running the unit tests on Windows (Powershell)
```powershell
python -m pytest -v
```
#
# Usage
### Infection Probability
- The Infection Probability value determines how likely a healthy individual is to get infected upon contact with an infected one.
- Adjust the Infection Probability slider to the desired value, the default is 0.2.
- Only new individuals will be created with the selected value, previously created individuals are not affected when changing the slider value. In other words, each individual keeps its own infection probability throughout the simulation.
### Adding or Removing Individuals 
- Press the "+1 Healthy" button to add a new healthy individual to the simulation.
- Press the "+1 Infected" button to add a new infected individual to the simulation.
- Press the Reset button to remove all individuals and reset the simulation parameters.
### Changing the Color of Individuals
- Press the "Healthy Color" button to change the color of new healthy individuals.
- Press the "Infected Color" button to change the color of new infected individuals.
- Press the "Recovered Color" button to change the color of new recovered individuals.
- Only new individuals will be created with the new color, previously created individuals are not affected when changing the color. In other words, each individual keeps its infection status color throughout the simulation until it updates its infection status.
#
# Requirements
- Python 3.7 or greater
- Git (to clone the repo)
#
# Unsupported
- The use of the Windows Subsystem for Linux (WSL) is not supported because it provides very poor performance for the Kivy module and causes several graphical glitches, however, you can run this program in Windows with Python natively without any issues.
