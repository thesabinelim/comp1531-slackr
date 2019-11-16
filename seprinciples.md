- admin.py
    - created a stub function for the errors so that the overall opacity of the 
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
    
- 


- upload_photo 12/11/19
    - The initial code was very long and had all of the logic placed into a
    100 line+ function. By refactoring the larger processes into their own
    steps, upload_photo was heavily reduced in size, and easier to test.
    Additionally, the 'imgurls' literals were replaced with constants obtained
    via the database according with DRY principles.
