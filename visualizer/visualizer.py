# converts moments to videos

# import some libraries
# from __future__ import print_function

import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib
matplotlib.use('TKAgg')

mpl.rcParams['font.family'] = ['Bitstream Vera Sans']

# data = json opened already
def visualize(data, eventid, label):
    # import the data from wherever you saved it.
    # json_data = open('data/sportvu/' + gameid + '.json')
    # data = json.load(json_data)  # load the data

    def acquire_gameData(data):
        import requests
        header_data = {  # I pulled this header from the py goldsberry library
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'\
            ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 '\
            'Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'\
            ',image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
        }
        game_url = ('http://stats.nba.com/stats/playbyplayv2?' +
                    'EndPeriod=0&EndRange=0&GameID=' + data['gameid'] +
                    '&RangeType=0&StartPeriod=0&StartRange=0')
        response = requests.get(game_url, headers=header_data)
        # get headers of data
        headers = response.json()['resultSets'][0]['headers']
        # get actual data from json object
        gameData = response.json()['resultSets'][0]['rowSet']
        # turn the data into a pandas dataframe
        df = pd.DataFrame(gameData, columns=headers)
        # there's a ton of data here, so I trim  it doown
        df = df[
               [df.columns[1],
                df.columns[2],
                df.columns[7],
                df.columns[9],
                df.columns[18]]]
        df['TEAM'] = df['PLAYER1_TEAM_ABBREVIATION']
        df = df.drop('PLAYER1_TEAM_ABBREVIATION', 1)
        return df

    player_fields = data['events'][0]['home']['players'][0].keys()
    home_players = pd.DataFrame(
        data=[i for i in data['events'][0]['home']['players']],
        columns=player_fields)
    away_players = pd.DataFrame(
        data=[i for i in data['events'][0]['visitor']['players']],
        columns=player_fields)
    players = pd.merge(home_players, away_players, how='outer')
    jerseydict = dict(zip(players.playerid.values, players.jersey.values))

    #  Animation function / loop
    def draw_court(axis):
        import matplotlib.image as mpimg
        # read image. I got this image from gmf05's github.
        img = mpimg.imread('visualizer/nba_court_T.png')
        plt.imshow(img, extent=axis, zorder=0)  # show the image.

    # matplotlib's animation function loops through a function n times that
    # draws a different frame on each iteration
    def animate(n):
        for i, ii in enumerate(player_xy[n]):  # loop through all the players
            # change each players xy position
            player_circ[i].center = (ii[1], 50 - ii[2])
            # draw the text for each player.
            player_text[i].set_text(str(jerseydict[ii[0]]))
            player_text[i].set_x(ii[1])  # set the text x position
            player_text[i].set_y(50 - ii[2])  # set text y position
        # change ball xy position
        ball_circ.center = (ball_xy[n, 0], 50 - ball_xy[n, 1])
        # i could change the size of the ball according to its height,
        # but chose to keep this constant
        ball_circ.radius = 1.1
        frame_text.set_text(str(n))
        frame_text.set_x(50)
        frame_text.set_y(52)
        return (tuple(player_text) + tuple(player_circ) +
                (ball_circ,) + (frame_text,))

    # this is what matplotlib's animation will create before drawing the first
    # frame.
    def init():
        for i in range(10):  # set up players
            player_text[i].set_text('')
            ax.add_patch(player_circ[i])
        ax.add_patch(ball_circ)  # create ball
        ax.axis('off')  # turn off axis
        dx = 5
        plt.xlim([0 - dx, 100 + dx])  # set axis
        plt.ylim([0 - dx, 50 + dx])
        frame_text.set_text('0')
        return (tuple(player_text) + tuple(player_circ) +
                (ball_circ,) + (frame_text,))

    # the order of events does not match up, so we have to use the eventIds.
    # This loop finds the correct event for a given id# .
    search_id = eventid

    def find_moment(search_id):
        for i, events in enumerate(data['events']):
            if events['eventId'] == str(search_id):
                return i
        raise Exception("Moment not found")

    event_num = find_moment(search_id)

    # create matrix of ball data
    ball_xy = np.array([x[5][0][2:5]
                       for x in data['events'][event_num]['moments']])
    player_xy = np.array([np.array(x[5][1:])[:, 1:4] for x in
                         data['events'][event_num]['moments']])

    #  ==============================ANIMATION=================

    fig = plt.figure(figsize=(15, 7.5))  # create figure object
    ax = plt.gca()  # create axis object

    draw_court([0, 100, 0, 50])  # draw the court
    player_text = range(10)  # create player text vector
    player_circ = range(10)  # create player circle vector
    # create circle object for ball
    ball_circ = plt.Circle((0, 0), 1.1, color=[1, 0.4, 0])
    for i in range(10):  # create circle object and text object for each player
        # color scheme   home if i < 5 else away
        col = ['w', 'k'] if i < 5 else ['k', 'w']
        player_circ[i] = plt.Circle(
            (0, 0), 2.2, facecolor=col[0], edgecolor='k')  # player circle
        # player jersey  #  (text)
        player_text[i] = ax.text(0, 0, '', color=col[1],
                                 ha='center', va='center')
    frame_text = ax.annotate('', xy=[50, 52],
                             color='black', horizontalalignment='center',
                             verticalalignment='center')

    ani = animation.FuncAnimation(fig, animate,
                                  frames=np.arange(0, np.size(ball_xy, 0)),
                                  init_func=init, blit=False,
                                  interval=5, repeat=False, save_count=0)

    folder = "zone" if label == 1 else "man"
    # instead of gameid, get data['gameid']
    ani.save('data/videos/events/%s/%s_%d.mp4' % (folder, data['gameid'],
             search_id), dpi=100, fps=25)
    plt.close('all')
