general:
    - Tokens passed to functions will be validated first.

auth_register:
    - First name cannot be blank and must contain only alphanumeric characters,
      '-', '_', ''', '/', '(', ')' and '.'.
    - Names cannot contain only punctuation.
    - Returned u_ids cannot be negative.

channel_leave:
    - Owner can't leave unless they are the last person in channel or they add
      another person as owner beforehand. We assume this is an oversight and
      will be fixed in iteration 2.

channels_create:
    - Channel names must contain only alphanumeric characters, '-', '_', '[' and
      ']'.
    - If a channel already exists with a certain name, you cannot create another
      channel with the same name.

channels_list:
    - The list of channels returned is sorted in order of id.

user_profile:
    - For now, the handle_str is assumed by default to be first name and last
      name concat'd together.
    
standup:
    - assuming that time_finish refers to a time returned in the form of the
      users local time.
    - that if there is only one user in a channel the channel doesnt delete when
      that user is removed
    - standup_start returns the amount of time left in the standup however this
      doesnt get passed to standup_send, because of this I'm assuming that this
      time is saved and can be accessed in standup_send somehow.
