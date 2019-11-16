- admin.py
    - created a function for the errors so that the overall opacity of the 
    program is far more 'opaque', that is that its easier for the user to
    understand what is happening in the main function. This also allows further
    flexibility when implementing new errors in the future as this can be done at
    a glance.
    - Additionally created a stub function for the validation of tokens and
    the targets id so that its easier to understand whats going on in the main
    function, this is to make the main function take a more 'top down' 
    approach where its easy to understand the overall function
    - This is aided through additional documentation to further understand
    at a glance what is happening.
    - all of this increases complexity however the tradeoffs in readability and 
    flexibility, i believe, outweight this factor.
    
- auth.py
    - once again whereever possible I've added stubs for errors as they don't
    need to be in the main function. This enables both flexibility in implementing 
    further checks and increases readability
    - created a function for validating the token and retrieving the payload
    outside validate_token called validate_token_payload to further increase
    readability and maintainability of the main function.
    - increased levels of documentation for error functions to make it easier
    to understand exactly what they try to achieve
    - had to implement line spacing between function classes so that its
    easier to understand where functions stopped and started
    - created a function in auth_register for returning a new token and u_id on signup
    underneath the main function to reduce the complexity in the main function
    once again aiming for high levels of readability in the main function
    

    



- upload_photo 12/11/19
    - The initial code was very long and had all of the logic placed into a
    100 line+ function. By refactoring the larger processes into their own
    steps, upload_photo was heavily reduced in size, and easier to test.
    Additionally, the 'imgurls' literals were replaced with constants obtained
    via the database according with DRY principles.
