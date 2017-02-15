import json

"""
   pick moments ending in a shot, or a steal.
   do not pick moments where the previous moment was a steal.
   pick after timeout/violation/substitution/foul moments.
"""
def pick_possessions(pbp):
    data = json.load(open(pbp))
    headers = data['resultSets'][0]['headers']
    row_set = data['resultSets'][0]['rowSet']
    #EVENTMSGTYPE
    #1 - Make 
    #2 - Miss 
    #3 - Free Throw 
    #4 - Rebound 
    #5 - out of bounds / Turnover / Steal 
    #6 - Personal Foul 
    #7 - Violation 
    #8 - Substitution 
    #9 - Timeout 
    #10 - Jumpball 
    #12 - Start Q1 
    #13 - Start Q2
