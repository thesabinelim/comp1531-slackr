general:
    - Tokens passed to functions will be validated first.
    - Ids don't get reused. e.g If a message_id of 1 gets assigned to a message, 
      deleting that message wouldn't free up 1 for an id again, the next object
      would be given an id of 2.
    - Code duplication in tests is more acceptable than in implementation code.
      It's easier to see what a test does when all the setup is there, and
      coupling together tests is a bad idea - as changing a single failing test
      could potentially change others if the code is too tightly factored.
    - Assuming marking messages as read will be clarified in iteration 2.
    - If a token is invalid a TokenError will be raised.
    - Slackr owners/admins are only owners of channels they are members of.
    - Timestamps are in Unix time.

auth_register:
    - First name cannot be blank and must contain only alphanumeric characters,
      '-', '_', ''', '/', '(', ')' and '.'.
    - Names cannot contain only punctuation.
    - Returned u_ids cannot be negative.

channel_messages:
    - If the number of messages in a channel is zero, an empty list should be returned instead of throwing a ValueError constantly.
    
channel_details:
    - The list of members returned is sorted in order of id.

channel_leave:
    - An owner leaving removes them from the channel's owner list.
    - If an owner is the last owner (not inherited owner like with slackr admin/owner) of a channel, then they can't leave unless they are the only member left.

channel_join:
    - Owner of slackr is not automatically owner of channels joined.

channel_invite:
    - Owner of slackr is not automatically owner of channels invited to.
    - ValueError is raised for channel not existing whereas AccessError is
      raised when user is not in channel that exists.

channels_list:
    - The list of channels returned is sorted in order of id.

channel_addowner:
    - slackr owners can promote themselves to owners of any channel they're in.
    - slackr owners can promote others to owners of channels said others are in,
      even if the slackr owner isn't an owner of the channel themself.
    - If the target user wasn't in the channel, then they will be in addition to being an owner

channel_removeowner:
    - Assuming that behaviour of attempting to remove someone as owner of
      channel they're not in will be clarified in iteration 2.
    - Assuming that slackr owners are not immune from being removed as owners by
      channel owners.

channels_create:
    - Channel names must contain only alphanumeric characters, '-', '_', '[' and
      ']'.
    - If a channel already exists with a certain name, you cannot create another
      channel with the same name.

user_profile:
    - Any valid user can see the profile of any other valid user, the token
      supplied is not necessarily the same user from the u_id.

message_send:
    - Users cannot send messages to channels they are not members of. Raise
      AccessError if this is attempted.
    - Message cannot be empty.

message_sendlater:
    - Users cannot send messages to channels they are not members of. Raise
      AccessError if this is attempted.
    - time_sent is a Unix timestamp.
    - Message cannot be empty.

message_remove:
    - The conditions for the AccessError are probably wrong for this iteration
        - Only raises the exception when ALL conditions are not true
    - It's trying to say you can edit the message if:
        - You are the original sender
        - OR You are a channel owner
        - OR You are the slackr admin
message_edit:
    - Similarly to message_remove, the conditions seem erroneous.
    - It's trying to say you can edit the message if:
        - You are the original sender.
        - OR You are a channel owner.
        - OR You are the slackr admin.
    - For example of what's wrong with the original logic, any user can edit any
      post. For an owner of the slack and channel, they can't edit any of their
      own posts.
    - The 'new' text can be the same as the original.
    - The new text still must be under the original send limit of 1000 chars.
    - The new text can't be empty.

message_react:
    - Valid react_ids will be clarified in Iteration 3.

message_unreact:
    - Users can only unreact to messages they've already reacted to.
    - Admins can unreact all messages.
    - Valid react_ids will be clarified in Iteration 3.

standup_send:
    - The standup buffer can contain an arbitrarily long number of characters.

admin_userpermission_change:
    - The first user is an owner (as opposed to admin as the spec says).
    - Admins can't promote themselves or others to owners. An AccessError will
      be raised if this is attempted.
    - Admins can't demote owners to admins. An AccessError will be raised if
      this is attempted.
      
search:
    - Only the channels that a user is in to are searched.
    - The search function will not be case sensitive.
    - Spaces at the end of a query will be included.
