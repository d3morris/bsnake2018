import bottle
import os
import random



@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


game_id = 0
board_width = 0
board_height = 0
last_move = null

@bottle.post('/start')
def start(self):
    data = bottle.request.json
    self.game_id = data.get('game_id')
    self.board_width = data.get('width') - 1
    self.board_height = data.get('height') - 1

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#0011ff',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': '',
        'head_type': 'sand-worm',
        'tail_type' : 'fat-rattle'
    }


@bottle.post('/move')
def move(self):
    data = bottle.request.json

    # TODO: Do things with data
    
    mySnake = data['you']
    mySnakeLen = mySnake['length']   

    mySnakeHeadx = mySnake['body']['data'][0]['x']
    mySnakeHeady = mySnake['body']['data'][0]['y']
    mySnakeTailx = mySnake['body']['data'][mySnakeLen-1]['x']
    mySnakeTaily = mySnake['body']['data'][mySnakeLen-1]['y']

    if self.last_move == null:
        if (mySnakeHeadx == mySnakeTailx):
            if mySnakeHeady > mySnakeTaily:
                self.last_move = 3
            else:
                self.last_move = 1
                    
        elif (mySnakeHeady == mySnakeTaily):
            if mySnakeHeadx > mySnakeTailx:
                self.last_move = 2
        else:
                self.last_move = 0
            pass 
    }

    wall0 = mySnakeHeadx
    wall1 = self.board_width - mySnakeHeady
    wall2 = self.board_height - mySnakeHeadx
    wall3 = mySnakeHeady

    if self.last_move == 0:
        if mySnakeHeadx > 0:
            dir = 0
        else:
            if mySnakeHeady < self.board_width/2:
                dir = 1
            else:
                dir = 3

    elif self.last_move == 1:
        if mySnakeHeady < self.board_width:
            dir = 1
        else:
            if mySnakeHeadx < self.board_height/2:
                dir = 2
            else:
                dir = 0

    elif self.last_move == 2:
        if mySnakeHeadx < self.board_height:
            dir = 2
        else:
            if mySnakeHeady < self.board_width/2:
                dir =3
            else:
                dir = 1

    elif self.last_move == 3:
        if mySnakeHeady > 0:
            dir = 3
        else:
            if mySnakeHeadx < self.board_height/2:
                dir = 0
            else:
                dir = 2
    else:
        dir = 0
    


    directions = ['up', 'down', 'left', 'right']
 #   direction = random.choice(directions)
    print direction
    return {
        'move': directions[dir],
        'taunt': 'tried to think outside the box .. kept on running into walls!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
