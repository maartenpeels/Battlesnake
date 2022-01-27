import json
from bot import choose_move


def info(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({
            "apiversion": "1",
            "author": "maartenpeels",
            "color": "#118811",
            "head": "beluga",
            "tail": "curled",
            "version": "0.0.1-beta"
        }),
    }


def handler(event, context):
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
            'body': json.dumps({
                'move': move
            })
        }

    return {
        'statusCode': 200,
        'body': 'What do you want?!',
    }
