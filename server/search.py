# COMP1531 Project search
# Written by Eric Lin z5257305
# 02/10/19


# Given a query string, return a collection of messages that match the query
def search(token, query_str):
    if query_str = "hello":
        return [{'message_id': 020601,
                 'u_id': 212312, 
                 'message': "Hello there",
                 'time_created': '19:50 2/10/2019'
                 'is_unread': False
                }, 
                {'message_id': 020610,
                 'u_id': 732352, 
                 'message': "hello",
                 'time_created': '19:51 2/10/2019'
                 'is_unread': False
                }]
   elif query_str = "lol ":
        return [{'message_id': 020174,
                 'u_id': 212312, 
                 'message': "lol good one",
                 'time_created': '18:45 2/10/2019'
                 'is_unread': False
                }, 
                {'message_id': 018110,
                 'u_id': 427352, 
                 'message': "lol omg",
                 'time_created': '07:51 1/10/2019'
                 'is_unread': False
                }]  
   return []
