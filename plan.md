Number of allocated developers is only a minimum rule.

In order of implementation:

auth.py
    - As every other module relies on a working authentication system that can
      generate tokens, we will implement this module first.
    - Implementing auth_register will constitute the majority of development
      time for this module. Because it is such a critical component that we must
      ensure is functioning correctly before attempting other modules, we'll
      allocate 5 hours for its implementation, not including time spent getting
      familiar with Python and writing backends. For the same reason however,
      since work on other modules cannot begun until auth_register is complete,
      we'll set a deadline of 1 day after iteration 2 begins to implement it.

channels.py
    - As message.py relies on this module, we will implement parts of this
      module immediately after finishing auth.py. We'll delegate two people to
      work on this module, then reassign one person to message.py after critical
      functions are complete.
    - Due to being relied upon by message.py, we'll set a deadline of 3 days
      after iteration 2 begins to implement the relied upon functionality.
    - 

message.py
    - Can only be implemented after some of channels.py is implemented. We'll
      delegate one person for this module (reassigned from channels.py).
    - 

admin.py
    - Less relied upon by other modules but still very important functionality
      that will be highly valuable for testing other modules. Since it is a
      smaller module we'll allocate one person to work on it while others work
      on channels.py and message.py. Once they're done we'll reassign them to
      user.py.
    - Because this module will aid in testing other modules (but is not too
      critical), we'll set a deadline of 3 days after iteration 2 begins to
      implement it fully. This also allows the developer to move on to more
      important modules sooner.

user.py
    - Can be implemented as soon as auth.py is complete, but since channels.py
      is more critical due to message.py relying on it, we will implement this
      after channels.py. To save development time we'll delegate a few people to
      work on channels.py and message.py while one person works on this module.
    - 

"Extras" (to be started at least 5 days before the final deadline)

search.py
    - Less relied upon component but still important functionality, so this is
      the first of the extras that we'll implement. It's a very small module
      so we'll allocate one person to it once core functionality is mostly done.
    - Because this module consists of only one function, we anticipate it will
      take 2 hours at the very most to implement it.

standup.py
    - 
