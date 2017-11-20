#!/usr/bin/env python
"""Score scraper for Kansas NCAA Basketball team"""

from bs4 import BeautifulSoup
import requests

req = requests.get('http://www.ncaa.com/schools/kansas/basketball-men')
soup = BeautifulSoup(req.text, 'html.parser')

class Game():
    """Game class for storing game data"""
    def __init__(self, gamedate, team):
        self.team = team
        self.gamedate = gamedate
        self.score = GameScore(self)

class GameScore(Game):
    """GameScore class for storing game scores"""
    def __init__(self, game):
        self.game = game
        self.win = None
        self.ku = 0
        self.opp = 0
        self.record = None

def extractTD(td):
    """Determine if TD has a link in it, and extract the text"""
    if getattr(td, 'a', None):
        return td.a.string
    if getattr(td, 'string', None):
        return td.string
    return None

for g in soup.find_all('tbody')[0].find_all('tr'):
    game_stats = '::'.join(extractTD(td) for td in g.find_all('td') if
            extractTD(td)).split('::')
    gamedate = game_stats[0]
    team = game_stats[1]
    game = Game(gamedate, team)
    if len(game_stats) > 2:
        game_score = game_stats[2].split()
        game.score.win = True if game_score[0] == 'W' else False
        game.score.ku = game_score[1].split('-')[0]
        game.score.opp = game_score[1].split('-')[1]
        game.score.record = game_stats[3]
    template = "Date: {} -- Opponent: {}"
    format_items = [gamedate, team]
    if game.score.win: 
        template += " -- {} -- {}-{} -- {}"
        win_loss = "Won" if game.score.win else "Lose"
        format_items += [win_loss, game.score.ku, game.score.opp, game.score.record]
    print(template.format(*format_items))
