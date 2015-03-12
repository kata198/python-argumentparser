# Copyright 2015 (c) Tim Savannah
# GPL License

class ArgumentParser(object):
	'''
		A utility class for parsing command-line arguments.

		@param names list<string> - This is a list of "names" which should reflect each argument.
		@param shortOptions list<string>  - This is a list of short (-x val) options. Length should match names. If no short option is available, use 'None'. Omit the leading -
		@param longOptions  list<string>  - This is a list of long (--xyz val or --xyz= val) options. If no long option is available, use 'None'. Omit the leading --
		@param staticOptions list<string> - This is a list of static options (arguments that have meaning just being present, without taking an additional value).
												Any members of this list will be present in the results of #parse, set to True is present, otherwise False.

        @param multipleStaticOptions <dict> - A dictionary for multiple static arguments that resolve to one value. Key is the "name", values are all potential values. Ex: {'cheese' : ['--cheddar', 'gouda'] } presence of either 'gouda' or '--cheddar' in results would set cheese to True, otherwise False.
		@param allowOtherArguments <bool> default False - if False, consider non-specified arguments as errors.

	    @example
In [1]: from ArgumentParser import ArgumentParser

In [2]: parser = ArgumentParser(['firstName', 'lastName', 'birthday'],
   ...:     ['f', 'l', 'b'],
   ...:     ['first-name', 'last-name', 'birthday'],
   ...:     ['--citizen']
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

>>> import ArgumentParser
>>> parser = ArgumentParser.ArgumentParser( ('one', 'two'), ('o', 't'), ('uno', 'dos'), ('x'), {'cheese' : ['cheddar', 'gouda'], 'baby' : {'child', 'infant'}} )
>>> parser.parse(['-o', '1', 'cheddar'])
{'errors': [], 'result': {'baby': False, 'cheese': True, 'x': False, 'one': '1'}, 'unmatched': [], 'warnings': []}

	'''

	def __init__(self, names, shortOptions, longOptions, staticOptions=None, multipleStaticOptions=None, allowOtherArguments=False):
		namesLen = len(names)
		if namesLen != len(shortOptions) or namesLen != len(longOptions):
			raise ValueError('names, shortOptions, longOptions must all have the same length. use None of there is no equivlant.')

		self.names = names
		self.shortOptions = shortOptions
		self.longOptions = longOptions
		self.staticOptions = staticOptions or []
		self.multipleStaticOptions = multipleStaticOptions
		self.allowOtherArguments = allowOtherArguments


	def parse(self, args):
		'''
			parse - Parses provided arguments and returns information on them. If using sys.argv, omit the first argument.

			@return - dict keys are
						'result' => dictionary of result name->value
						'errors'  => list of strings of errors or empty list
						'warnings' => list of strings of warnings, or empty list
						'unmatched' => all unmatched params, in order
		'''
		result = {}
		errors = []
		warnings = []
		unmatched = []
		
		argsLen = len(args)
		i = 0
		while i < argsLen:
			arg = args[i]

			if self.multipleStaticOptions is not None:
				foundIt = False
				for optionName, possibleValues in self.multipleStaticOptions.items():
					if arg in possibleValues:
						if optionName in result:
							warnings.append("Argument '%s' specified more than once (at position %d)" %(arg, i))
						else:
							result[optionName] = True
						foundIt = True
						break
				if foundIt is True:
					i += 1
					continue
							
			if arg in self.staticOptions:
				if arg in result:
					warnings.append("Argument '%s' specified more than once (at position %d)" %(arg, i))
				else:
					result[arg] = True
				i += 1
				continue
			
			if arg.startswith('--'):
				try:
					equalSignIdx = arg.index('=')
					argName = arg[2:equalSignIdx]
				except ValueError:
					equalSignIdx = False
					argName = arg[2:]
				try:
					argIdx = self.longOptions.index(argName)
				except ValueError:
					errors.append("Unknown argument '%s' (at position %d)" %(arg, i,))
					i += 1
					continue
				
				name = self.names[argIdx]
				if name in result:
					warnings.append("Option '%s' specified more than once. Using latter value (at position %d)" %(name, i))

				if equalSignIdx is not False:
					val = arg[equalSignIdx+1:]
					if len(val) == 0:
						errors.append('Equal sign used and no value on \'%s\' (at position %d)' %(arg, i))
						i += 1
						continue
					result[name] = val
					i += 1
					continue
				else:
					if i+1 >= argsLen:
						errors.append('No equal sign provided on assignment option, and no more arguments to try with \'%s\' (at position %d)' %(arg, i))
						i += 2
						continue
					val = args[i+1]
					result[name] = val
					i += 2
					continue

			elif arg.startswith('-'):
				argName = arg[1:]
				if i+1 >= argsLen:
					errors.append('No assignment on short option %s (at position %d)' %(arg, i))
					i += 2
					continue
				
				try:
					argIdx = self.shortOptions.index(argName)
				except ValueError:
					errors.append("Unknown option '%s' (at position %d)" %(arg, i))
					i += 1
					continue

				name = self.names[argIdx]
				if name in result:
					warnings.append("Argument \'%s\' specified more than once, using latter value (at position %d)" %(name, i))

				result[name] = args[i+1]
				i += 2
				continue
			
			else:
				if self.allowOtherArguments is False:
					errors.append('Unknown argument \'%s\' (at position %d)' %(arg, i))

				unmatched.append(arg)
					
				i += 1
				continue

		for staticOption in self.staticOptions:
			if staticOption not in result:
				result[staticOption] = False

		if self.multipleStaticOptions is not None:
			foundItems = set(result.keys())
			multipleOptions = set(self.multipleStaticOptions.keys())

			for optionName in multipleOptions.difference(foundItems):
				result[optionName] = False
		
		return { 'result' : result, 'errors' : errors, 'warnings' : warnings, 'unmatched' : unmatched }

				
				
# vim: sw=4 ts=4 noexpandtab
