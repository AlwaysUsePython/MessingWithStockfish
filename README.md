# Chess.com Clone

This program uses the python chess.com api to access a given user's most recent game and then walk the user through a step by step analysis.

It uses stockfish 11 to find the best moves and points out where the user made bad moves. At any point, you can see the line the computer has in mind so that you can understand not only which moves were bad but how they could be punished and which moves were better!

# Setup

hahahahahaha good luck. Either I'm stupid or setting up Stockfish in python is a pain in the ass.

First, you need a python IDE with the packages for chess, chess.com, pygame, and stockfish installed. All of that can be done through either pip or the pycharm interpreter interface with little trouble.

Now the fun part: you need to download a version of stockfish. Copy the file path to one of the stockfish executable files into the code where it says stockfish = Stockfish(r'FILEPATH'). I'm using stockfish 11 cause that's the only one that I could get working (translation: that's the one that I could copy paste from an outdated StackOverflow post). And let's be real - both stockfish 11 and stockfish 15 would easily win all my games for me, so it doesn't really matter which one is doing the analysis. Follow this stack exchange post if it isn't working: https://chess.stackexchange.com/questions/31995/unable-to-run-stockfish-on-python

If that all works first try, you're a better programmer than I am!

# Elliot's Todo List / Brainstorming
 
 - create replacement for chess.com's Coach "That game was a gift!" David
     - come up with funny name?
     - message indicating who won - profile picture? updates as game goes on? 
     - practice game feature where you play agianst \[name undecided\]? 
     - replace outdated debug code best move uci display
