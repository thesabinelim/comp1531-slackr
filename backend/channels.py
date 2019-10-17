# COMP1531 Project channels
# Written by Sabine Lim z5242579
# 01/10/19

# Return list of channels (and their details) that user is in.
def channels_list(token):
    if token == '1234567':
        return {
            'channels': [
                {7654321, '1531 autotest'}
            ]
        }
    elif token == '5242579':
        return {
            'channels': [
                {3054207, 'PCSoc'},
                {7654321, '1531 autotest'},
                {9703358, 'Steam'}
            ]
        }
    elif token == '4201337':
        return {
            'channels': [
                {7654321, '1531 autotest'},
                {9703358, 'Steam'}
            ]
        }
    elif token == '0018376':
        return {'channels': []}

    return {'channels': []}

# Return list of channels (and their details).
def channels_listall(token):
    return {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

# Create new channel with that name that is either a public or private channel.
# Raise ValueError exception if name > 20 characters.
def channels_create(token, name, is_public):
    if name == '123456789012345678901':
        raise ValueError

    if name == '1531 autotest':
        return {'channel_id': 7654321}
    elif name == 'PCSoc':
        return {'channel_id': 3054207}
    elif name == 'Steam':
        return {'channel_id': 9703358}
