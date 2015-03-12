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
    @param multipleStaticOptions <dict> - A dictionary for multiple static arguments that resolve to one value. Key is the "name", values are all potential values. Ex: {'cheese' : ['--cheddar', 'gouda'] } presence of either 'gouda' or '--cheddar' in results would set cheese to True, otherwise False.
    @param allowOtherArguments <bool> default False - if False, consider non-specified arguments as errors. Regardless of value, unmatched params will be in 'unmatched' key of return value.


Functions:

    def parse(args)
        parse - Parses provided arguments and returns information on them. If using sys.argv, omit the first argument.

    @return - dict keys are
                'result' => dictionary of result name->value
                'errors'  => list of strings of errors or empty list
                'warnings' => list of strings of warnings, or empty list
                'unmatched' => list of strings of unmatched params, in order



Example
=======


    In [1]: from ArgumentParser import ArgumentParser

    In [2]: parser = ArgumentParser(['firstName', 'lastName', 'birthday'], 
       ...:     ['f', 'l', 'b'], 
       ...:     ['first-name', 'last-name', 'birthday'], 
       ...:     ['--citizen'] 
       )

    In [3]: parser.parse('-f Tim --last-name=savannah --birthday 6/28'.split(' '))
    Out[3]:
    {'errors': [],
      'result': {'--citizen': False,
      'birthday': '6/28',
      'firstName': 'Tim',
      'lastName': 'savannah'},
      'warnings': [],
      'unmatched' : []}

    In [4]: parser.parse('-f Tim --last-name=savannah --citizen'.split(' '))
    Out[4]:
    {'errors': [],
     'result': {'--citizen': True, 'firstName': 'Tim', 'lastName': 'savannah'},
     'warnings': [],
     'unmatched': []}



Example2
========

      >>> from ArgumentParser import ArgumentParser
      >>> parser = ArgumentParser(['name'], ['n'], ['name'], None, False)
      >>> parser.parse('-n hello some other args'.split(' '))
      {'errors': ["Unknown argument 'some' (at position 2)", "Unknown argument 'other' (at position 3)", "Unknown argument 'args' (at position 4)"], 'result': {'name': 'hello'}, 'unmatched': ['some', 'other', 'args'], 'warnings': []}
      >>> parser = ArgumentParser(['name'], ['n'], ['name'], None, True)
      >>> parser.parse('-n hello some other args'.split(' '))
      {'errors': [], 'result': {'name': 'hello'}, 'unmatched': ['some', 'other', 'args'], 'warnings': []}
 
Example3
========
        
      >>> import ArgumentParser
      >>> parser = ArgumentParser.ArgumentParser( ('one', 'two'), ('o', 't'), ('uno', 'dos'), ('x'), {'cheese' : ['cheddar', 'gouda'], 'baby' : {'child', 'infant'}} )
      >>> parser.parse(['-o', '1', 'cheddar'])
      {'errors': [], 'result': {'baby': False, 'cheese': True, 'x': False, 'one': '1'}, 'unmatched': [], 'warnings': []}
