from chessdotcom import get_player_game_archives
import pprint
import requests
from stockfish import Stockfish

stockfish = Stockfish(r'C:\Users\ellio\Downloads\stockfish-11-win\stockfish-11-win\Windows\stockfish_20011801_x64.exe')
printer = pprint.PrettyPrinter()

def get_most_recent_game(username):
    data = get_player_game_archives(username).json
    url = data['archives'][-1]
    games = requests.get(url).json()
    game = games['games'][-1]
    return game['pgn']

white = {
    "a": [2],
    "b": [2],
    "c": [2],
    "d": [2],
    "e": [2],
    "f": [2],
    "g": [2],
    "h": [2],
    "R": ["a1", "h1"],
    "N": ["b1", "g1"],
    "B": ["c1", "f1"],
    "Q": ["d1"],
    "K": ["e1"]
}

black = {
    "a": [7],
    "b": [7],
    "c": [7],
    "d": [7],
    "e": [7],
    "f": [7],
    "g": [7],
    "h": [7],
    "R": ["a8", "h8"],
    "N": ["b8", "g8"],
    "B": ["c8", "f8"],
    "Q": ["d8"],
    "K": ["e8"]
}

game = get_most_recent_game("elichtman1")
