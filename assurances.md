# Assurances
###### Written by Bridget McCarthy z5255505
### Verification
Our team made sure to consider the verification and validation of our system as we wrote it.

To verify that our system was correct we always made sure to follow the reference implementation and ensured that at least one other person reviewed the structure and code for a new commit.

Any assumptions we had made that had become obsolete from Iteration 1 due to an updated specification were removed and the code pertaining to them rewritten to follow the Iteration 2 specification.

This validation process came before we actually tested the code, as we can't test code properly if it doesn't actually match what the specification wants in terms of input, output and changes to the data.
### Validation
After the verification process for the implementation was complete and we were sure that everything had matched the specification, we began the validation of our system via the testing procedure.

This went as follows:
- Run `python3-coverage` on a test file - where they are seperated into the subsets of functions
- If any tests failed, inspect the error that rose up, and see if our tests were still wrong based off of the assumptions from Iteration 1, or if there was an issue with the validity of our implementation
- Fix up the issue (whether it be an invalid test or invalid code) and continue this process until all tests pass
- Check the coverage report and if the coverage is less than 100% for our target subset of functions, then write more tests to ensure that we can validate as much of the system as possible

# Acceptance Criteria
The development of appropriate acceptance criteria was largely done by Jake Tyler, and for each User Story, we would check if the criteria have been met.

Unfortunately a lot of our criteria depends upon everything working - including the frontend. Since we were notified that the frontend working was not part of this current iteration, our acceptance criteria is filled on the backend side, but not completely - as the frontend is not fully functional.

Overall, having the acceptance criteria was very helpful in ensuring that we weren't just writing for the spec, but for the User Stories as well. This kept us on track in writing features based off of what was wanted, rather than assumptions.

# Tools Used
### Gitlab Boards
The boards feature on GitLab was extremely useful in organising our tasks in an easy to read format, and ensuring that everybody knew whose responsibility a function was to implement.

And if people could not do their work in time, we were able to shift around responsibilities to others to get them completed in time.

### Git
Git is naturally required for us to use GitLab, and being able to keep all our code on seperate feature branches greatly assisted in being able to do easy code reviews.

All merges into master branch had to be preceded by a code review from another person in the group, who would make sure that the commits made sense and didn't have conflicts

### Python3-coverage
The coverage tool for python was immensely helpful in making sure that we actually tested all the code on a basic level.

Through the use of this tool we uncovered many cases that weren't actually being tested, and improved the validity of our system.

### Pytest
Pytest was a key part of our workflow as shown above, and identified many issues with our assumptions from Iteration 1 compared to the updated spec and fixed quite a few bugs that manual inspection glossed over.

### Pylint
By linting our code, we ensured that we were following good practices relatively well. Though, there are still some cases that we decided to ignore pylints warnings against. These include:

- Putting the docstring comments for a function in every single one
  - We felt these were largely unneccessary and contributed to a lot of code bloat
- Unused variables in test
  - Due to the nature of testing with a database, creating a user can cause differences in the way certain operations will work, without even actually touching the variable containing the data. Therefore we elected to ignore these concerns.