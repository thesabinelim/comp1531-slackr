general:
    - Tokens passed to functions will be validated first.

auth_register:
    - First name cannot be blank and must contain only alphanumeric characters,
      '-', '_', ''', '/', '(', ')' and '.'.
    - Names cannot contain only punctuation.

channels_create:
    - Channel names must contain only alphanumeric characters, '-', '_', '[' and
      ']'.
    - If a channel already exists with a certain name, you cannot create another
      channel with the same name.

channels_list:
    - The list of channels returned is sorted in order of id.

user_profile:
    - Can't verify anything as there is no actual backend for iteration 1.
    - Placeholder return values are used instead to be changed in the next iteration.
    - Similarly, an 'invalid' user id depends on the backend, and it has been
    taken for now to just be that an id can't be negative.