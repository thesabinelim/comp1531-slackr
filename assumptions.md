general:
    - Tokens passed to functions will be validated first.
    - Ids don't get reused. e.g If a message_id of 1 gets assigned to an message, deleting that message wouldn't free up 1 for an id again, the next object would be given an id of 2.

auth_register:
    - First name cannot be blank and must contain only alphanumeric characters,
      '-', '_', ''', '/', '(', ')' and '.'.
    - Names cannot contain only punctuation.
    - Returned u_ids cannot be negative.

channels_create:
    - Channel names must contain only alphanumeric characters, '-', '_', '[' and
      ']'.
    - If a channel already exists with a certain name, you cannot create another
      channel with the same name.

channels_list:
    - The list of channels returned is sorted in order of id.

user_profile:
    - For now, the handle_str is assumed by default to be first name and last name concat'd together.

message_remove:
    - The conditions for the AccessError are taken literally
      - Only raises the exception when ALL conditions are not true