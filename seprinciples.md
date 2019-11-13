
- upload_photo 12/11/19
    - The initial code was very long and had all of the logic placed into a
    100 line+ function. By refactoring the larger processes into their own
    steps, upload_photo was heavily reduced in size, and easier to test.
    Additionally, the 'imgurls' literals were replaced with constants obtained
    via the database according with DRY principles.