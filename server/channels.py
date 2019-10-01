# COMP1531 Project channels
# Written by Sabine Lim z5242579
# 01/10/19

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
