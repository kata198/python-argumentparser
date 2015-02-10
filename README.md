# python-argumentparser
A python2/3 compatible commandline argument parser.

Usage
=====

A utility class for parsing command-line arguments.

Constructor:

@param names list<string> - This is a list of "names" which should reflect each argument.
@param shortOptions list<string>  - This is a list of short (-x val) options. Length should match names. If no short option is available, use 'None'. Omit the leading -
@param longOptions  list<string>  - This is a list of long (--xyz val or --xyz= val) options. If no long option is available, use 'None'. Omit the leading --
@param staticOptions list<string> - This is a list of static options (arguments that have meaning just being present, without taking an additional value).
                                                Any members of this list will be present in the results of #parse, set to True is present, otherwise False.

Functions:
def parse(args)
	parse - Parses provided arguments and returns information on them. If using sys.argv, omit the first argument.

	@return - dict keys are
				'result' => dictionary of result name->value
				'errors'  => list of strings of errors or empty list
				'warnings' => list of strings of warnings, or empty list



Example
=======

In [1]: from ArgumentParser import ArgumentParser

In [2]: parser = ArgumentParser(['firstName', 'lastName', 'birthday'], \
   ...:     ['f', 'l', 'b'], \
   ...:     ['first-name', 'last-name', 'birthday'], \
   ...:     ['--citizen'] \
   ...: )

In [3]: parser.parse('-f Tim --last-name=savannah --birthday 6/28'.split(' '))
Out[3]:
{'errors': [],
 'result': {'--citizen': False,
  'birthday': '6/28',
  'firstName': 'Tim',
  'lastName': 'savannah'},
 'warnings': []}

In [4]: parser.parse('-f Tim --last-name=savannah --citizen'.split(' '))
Out[4]:
{'errors': [],
 'result': {'--citizen': True, 'firstName': 'Tim', 'lastName': 'savannah'},
 'warnings': []}

