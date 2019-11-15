# COMP1531 Project search tests
# Written by Eric Lin z5257305
# 02/10/19

import pytest

from .auth import auth_register
from .channel import channel_join
from .channels import channels_create
from .message import message_send, message_sendlater
from .search import search
from .db import reset_data
from .error import ValueError, AccessError

def test_search_none():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    message_send(reg_dict1['token'], create_dict1['channel_id'], "Hello there!")
    message_send(reg_dict2['token'], create_dict1['channel_id'], "Hello")
    message_send(reg_dict3['token'], create_dict1['channel_id'], "hi everyone")
    # SETUP END

    search_dict1 = search(reg_dict1['token'], "a")
    assert search_dict1['messages'] == []

    search_dict2 = search(reg_dict2['token'], "b")
    assert search_dict2['messages'] == []

    search_dict3 = search(reg_dict3['token'], "c")
    assert search_dict3['messages'] == []

def test_search_simple():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    message_send(reg_dict1['token'], create_dict1['channel_id'], "Hello there!")
    message_send(reg_dict2['token'], create_dict1['channel_id'], "Hello")
    message_send(reg_dict3['token'], create_dict1['channel_id'], "hi everyone")

    m_id = []
    u_id = []
    msg = []
    # SETUP END

    search_dict1 = search(reg_dict1['token'], "Hello")
    search_dict2 = search(reg_dict2['token'], "Hello")
    search_dict3 = search(reg_dict3['token'], "Hello")

    for entry in search_dict1['messages']:
        assert 'message_id' in entry
        assert 'u_id' in entry
        assert 'time_created' in entry
        m_id.append(entry['message_id'])
        u_id.append(entry['u_id'])
        msg.append(entry['message'])

    assert search_dict1['messages']
    assert search_dict1 == search_dict2 and search_dict2 == search_dict3
    assert len(m_id) == 2
    assert m_id[0] != m_id[1]
    assert reg_dict1['u_id'] in u_id
    assert reg_dict2['u_id'] in u_id
    assert "Hello there!" in msg
    assert "Hello" in msg

def test_search_case():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    message_send(reg_dict1['token'], create_dict1['channel_id'], "Hello there!")
    message_send(reg_dict2['token'], create_dict1['channel_id'], "Hello")
    message_send(reg_dict3['token'], create_dict1['channel_id'], "hi everyone")

    m_id1 = []
    u_id1 = []
    msg1 = []

    m_id2 = []
    u_id2 = []
    msg2 = []
    # SETUP END

    search_dict1 = search(reg_dict1['token'], "H")
    search_dict2 = search(reg_dict2['token'], "h")

    for entry in search_dict1['messages']:
        assert 'message_id' in entry
        assert 'u_id' in entry
        assert 'time_created' in entry
        m_id1.append(entry['message_id'])
        u_id1.append(entry['u_id'])
        msg1.append(entry['message'])

    for entry in search_dict2['messages']:
        assert 'message_id' in entry
        assert 'u_id' in entry
        assert 'time_created' in entry
        m_id2.append(entry['message_id'])
        u_id2.append(entry['u_id'])
        msg2.append(entry['message'])

    assert search_dict1['messages']
    assert search_dict2['messages']
    assert search_dict1 == search_dict2
    
    assert len(m_id1) == 3
    assert m_id1[0] != m_id1[1]
    assert m_id1[1] != m_id1[2]
    assert reg_dict1['u_id'] in u_id1
    assert reg_dict2['u_id'] in u_id1
    assert reg_dict3['u_id'] in u_id1
    assert "Hello there!" in msg1
    assert "Hello" in msg1
    assert "hi everyone" in msg1

def test_search_notinchannel():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_send(reg_dict1['token'], create_dict1['channel_id'], "Hello there!") 
    # SETUP END

    search_dict1 = search(reg_dict2['token'], "Hello")

    assert search_dict1['messages'] == []
                                                                                                         
def test_search_multi_channel():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])

    message_send(reg_dict1['token'], create_dict2['channel_id'], "Hello there!")
    message_send(reg_dict2['token'], create_dict1['channel_id'], "Hello")

    m_id1 = []
    u_id1 = []
    msg1 = []

    m_id2 = []
    u_id2 = []
    msg2 = []
    # SETUP END
    
    search_dict1 = search(reg_dict1['token'], "Hello")
    search_dict2 = search(reg_dict2['token'], "Hello")
    
    for entry in search_dict1['messages']:
        assert 'message_id' in entry
        assert 'u_id' in entry
        assert 'time_created' in entry
        m_id1.append(entry['message_id'])
        u_id1.append(entry['u_id'])
        msg1.append(entry['message'])
     
    for entry in search_dict2['messages']:
        assert 'message_id' in entry
        assert 'u_id' in entry
        assert 'time_created' in entry
        m_id2.append(entry['message_id'])
        u_id2.append(entry['u_id'])
        msg2.append(entry['message'])
            
    assert search_dict1['messages']
    assert search_dict2['messages']
    assert search_dict1 != search_dict2
    
    assert len(m_id1) == 2
    assert m_id1[0] != m_id1[1]
    assert reg_dict1['u_id'] in u_id1
    assert reg_dict2['u_id'] in u_id1
    assert "Hello there!" in msg1
    assert "Hello" in msg1
    
    assert len(m_id2) == 1
    assert reg_dict2['u_id'] in u_id2
    assert "Hello" in msg2
