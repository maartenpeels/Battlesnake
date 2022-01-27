import json
from bot import choose_move


def handler(event, _):
    if event['path'] == '/start':
        return {
            'statusCode': 200,
            'body': 'Hello from Lambda!',
        }
    if event['path'] == '/end':
        return {
            'statusCode': 200,
            'body': 'Bye from Lambda!',
        }

    if event['path'] == '/move':
        body = json.loads(event['body'])
        move = choose_move(body)
        return {
            'statusCode': 200,
            'body': {
                'move': move
            }
        }

    return {
        'statusCode': 200,
        'body': 'What do you want?!',
    }
