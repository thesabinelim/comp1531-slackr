- General
    - We now import individual functions and variables rather than entire
    modules. This prevents namespace conflicts

- db.py
    - The database now persists between server restarts. To accomplish this we
    have a thread that dumps the database to a pickle file every minute
    - The database get functions now throw ValueErrors if no object with a given
    id/other attribute is found. This was preferable to having to throw
    ValueErrors dozens more times in other functions. If return None was
    required, there was an optional named parameter error which when called with
    value False would return None rather than throw an error
    - Added to_dict methods for most database classes. This was preferable to
    having to generate these dictionaries in other functions

- admin.py
    - created a function for the errors so that the overall opacity of the 
    program is far more 'opaque', that is that its easier for the user to
    understand what is happening in the main function. This also allows further
    flexibility when implementing new errors in the future as this can be done
    at a glance.
    - Additionally created a stub function for the validation of tokens and
    the targets id so that its easier to understand whats going on in the main
    function, this is to make the main function take a more 'top down' 
    approach where its easy to understand the overall function
    - This is aided through additional documentation to further understand
    at a glance what is happening.
    - all of this increases complexity however the tradeoffs in readability and 
    flexibility, i believe, outweight this factor.
    
- auth.py
    - validate_token now returns a user rather than a u_id, modules utilising it
    have been updated accordingly. We found that after retrieving u_id from
    validate_token, a db_get_user_by_u_id would be called in most cases anyways
    - once again whereever possible I've added stubs for errors as they don't
    need to be in the main function. This enables both flexibility in
    implementing further checks and increases readability
    - created a function for validating the token and retrieving the payload
    outside validate_token called validate_token_payload to further increase
    readability and maintainability of the main function.
    - increased levels of documentation for error functions to make it easier
    to understand exactly what they try to achieve
    - had to implement line spacing between function classes so that its
    easier to understand where functions stopped and started
    - created a function in auth_register for returning a new token and u_id on
    signup underneath the main function to reduce the complexity in the main
    function once again aiming for high levels of readability in the main
    function
    
- channel.py
    - two small functions at the top for validating users, retrieving channels
    and a target if given. One of the two functions was already found in each
    function so to reduce repetition of code throughout the whole file I
    implemented these two functions under the heading Channel Setup
    - once again created error functions to increase readability and sorted
    these with headings as to not get confused
    - channel messages was originally a large function with low readability with
    multiple while loops and error checks, it had fairly low readability. To fix
    this i broke the iterating loop and the loop in charge of appending a list
    with all found messages and changed them into functions called channel
    message count and channel message accumulate accordingly. These are all
    grouped together and have made the main function far more understandable
    then it was before. Overall this also enables future maintainence to be far
    swifter.
    - Increased the amount of comments overall 
    
- channels.py
    - not very much needed to be done here, just added an error function to
    increase readability in its associated function alongside increasing
    maintainability.
    - just grouped functions under headers to fit with the style of the others
    and make it a bit easier to find functions.

- error.py

- message.py
    - Reused code for ensuring a message text is valid between message_send and
    message_sendlater was moved to its own function
    - There was already a function that checked if messages where valid however
    there was code repetition when validating the user, channel and retrieving
    messages from message_ids. To reduce the overall complexity two functions to
    setup at the start of a function where implemented. These are under the
    header validate channel & message at the top. This increased readability in
    all the functions in this file.
    - as above error functions where implemented for the same reasons.
    - headers where also added to make it easier to find functions
    
- search.py
    - The search function was split into a sub-function that searches in an
    individual channel. This simplifies the logic of the main search function

- standup.py
    - created a setup function at the start that gets the user and channel from
    the token  and channel id. This was used in all functions to reduce code
    repetition. This also made functions more readable.
    - implemented all the above style; headers, error functions and more
    documentation to increase readability.
    
- user.py
    - implemented all the above style; headers, error functions and more
    documentation to increase readability. No substantial code repetition was
    found.

- users.py
    
- utils.py

- upload_photo 12/11/19
    - The initial code was very long and had all of the logic placed into a
    100 line+ function. By refactoring the larger processes into their own
    steps, upload_photo was heavily reduced in size, and easier to test.
    Additionally, the 'imgurls' literals were replaced with constants obtained
    via the database according with DRY principles.
