# EZ Class Writeup

There are no parenthasees or dots allowed, so calling functions and attribute access is not possible.
Also, you can only put code inside of functions, and no newline is allowed, so decorators are not possible.

The solution is to use metaclasses.
Class in python is just syntactic sugar for calling the mataclass, arg1 as class name, arg2 as tuple of parrent classess, and arg3 as dictionary of class members.
The default metaclass is type, but it can be overriden by specifying metaclass=callable inside of the parenthasees after class name.

If you use a mataclass of the function exec_class, and inherit from the string "flag\2etxt" (the \2e means . because . is banned),
it will call exec_class with a tuple containing flag.txt as the second argument.
Exec_class will iterate through the tuple, try to open flag.txt and exec the contents, then throw an exception due to a syntax error,
and this exception will contain the flag in the error message.