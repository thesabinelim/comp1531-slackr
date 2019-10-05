general:
    - Tokens passed to functions will be validated first.
    - Ids don't get reused. e.g If a message_id of 1 gets assigned to an message, deleting that message wouldn't free up 1 for an id again, the next object would be given an id of 2.
    - Code duplication in tests is more acceptable than in implementation code. It's easier to see what a test does when all the setup is there, and coupling together tests is a bad idea - as changing a single failing test could potentially change others if the code is too tightly factored.
    - Assuming marking messages as read will be clarified in iteration 2.

auth_register:
    - First name cannot be blank and must contain only alphanumeric characters,
      '-', '_', ''', '/', '(', ')' and '.'.
    - Names cannot contain only punctuation.
    - Returned u_ids cannot be negative.

channel_details:
    - The list of members returned is sorted in order of id.

channel_leave:
    - Owner can't leave unless they are the last person in channel or they add
      another person as owner beforehand. We assume this is an oversight and
      will be fixed in iteration 2.
    - An owner leaving removes them from the channel's owner list.

channel_join:
    - Owner of slackr is not automatically owner of channels joined.

channel_invite:
    - Owner of slackr is not automatically owner of channels invited to.

channels_list:
    - The list of channels returned is sorted in order of id.

channel_addowner:
    - Assuming that behaviour of attempting to add someone as owner of channel
      they're not in will be clarified in iteration 2.
    - The user being added as owner must already be in the channel.
    - slackr owners can promote themselves to owners of any channel they're in.
    - slackr owners can promote others to owners of channels said others are in,
      even if the slackr owner isn't an owner of the channel themself.

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
    - For now, the handle_str is assumed by default to be first name and last name concat'd together.

message_remove:
    - The conditions for the AccessError are taken literally
        - Only raises the exception when ALL conditions are not true

message_unreact:
    - Users can only unreact to messages they've already reacted to
    - Admins can unreact all messages

standup:
    - assuming that time_finish refers to a time returned in the form of the
      users local time.
    - that if there is only one user in a channel the channel doesnt delete when
      that user is removed
    - standup_start returns the amount of time left in the standup however this
      doesnt get passed to standup_send, because of this I'm assuming that this
      time is saved and can be accessed in standup_send somehow.

admin_userpermission_change:
    - The last digit of token indicates the permission of the user.
    - This function change the token which is in the parameter.
    - This function return a new token.
