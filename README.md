# Training AI to Play Two-Player Snake Game
## Dependencies
The packages needed are listed in requirement.txt. The code was tested with Python 3.7.4
To install the dependencies, you may run the following command:
```
python3 -m pip install -r requirements.txt
```
## Change Parameters
To problem instance size or parameters of the learning algorithm, please check and change file: ```input.py```.
## Training
To train the neural network, run the following command and add the filename you want to store the data in after ```--output```:
```
python3 Genetic_algo.py --output filename 
```
## Playing
###Run Test
To run test and see if AI can beat baseline opponent:
```
python3 game.py --input filename -s generation -f -t
```
###Play with AI
To play with AI of a specific generation:
```
python3 game.py --input filename -s generation -v
```
###Watch AI Fighting
To see what AI can do:
```
python3 game.py --input filename -s generation -t
```
## Acknowledgement
The frame of code is from aliakbar09a/AI_plays_snake. Link : https://github.com/aliakbar09a/AI_plays_snake