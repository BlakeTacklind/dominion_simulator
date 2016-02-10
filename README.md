# Dominion Card Game Learner

This program is ment to learn how to play the card game known as dominon and play in a tornament against other bots.

### Process

Data is collected by running a pseudo-random strategy against a standard stategy. It then logs the turn by turn data of wins into a csv file. 

Linear regression on cards left in bank is used to approximate nearness to the end of the game. Then regress on all data to find card usage given situations. These numbers are weigthed based on how much they win by. 

Choosing the card to play is done by finding the most valueable buy and choosing that one. 

### Results

With a learning set of 5 million games (~4000 voctories or near victories) There was a significant increase in number of victories from the psedo-random. However it is still not better then the default stragetgy

### Issues

So far the program only trys to figure out buys (the most important part of the game) and plays actions psedo-randomly

99.9% of games are not used in the leanring process.

Features are based off personal opinion rather then data.
