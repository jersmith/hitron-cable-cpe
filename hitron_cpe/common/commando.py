"""A templatized command-line parser.

  Pass in a template string and optional documentation and you get command line
  parsing, validation and help for free.

  Command line arguments are treated as one of three types:

  - Positional parameters
  - Options
  - Flags

  Positional parameters are strings that do not begin with a hyphen. They are treated
  in the order they appear.

  Options are specified with one hyphen and a letter, or two hyphens and a string, followed by
  '=' and another string (no spaces). Options can be required or optional.

  Flags are specified with one hyphen and a letter, or two hyphens and a string (no spaces).
  The presence of a flag means the value for that flag is True. The absence of a flag means
  that value is false.

  Options and flags can be located anywhere, even between positional parameters.

  Here's an example:

  command positional1 -f --key=abc positional2

  Template strings are a way to specify what the valid command line structure is. The
  template string follows the format:

  positional1 positional2 ... [option1|optional2|<option3>...] (flag1|flag2|flag3...)

  The command line is parsed and each name in the template is matched with it's value
  in the command arguments and placed in a dictionary. If required items are missing,
  or unknown items are found, an error is returned.

  """


def parse_template(template):
  """Parse a template spec for command line arguments into a tuple of list and
    dictionary values.
  """
  commands = template.split(' ')
  positional_parameters = []
  options = []
  flags = []

  for command in commands:
    if len(command) > 0:
      if command[0] == '[':
        opts = command[1:len(command) - 1].split('|')
        # need to validate the options; first char must be unique
        options.extend(opts)
      elif command[0] == '(':
        flgs = command[1:len(command) - 1].split('|')
        flags.extend(flgs)
      else:
        positional_parameters.append(command)

  return (positional_parameters, options, flags)


def parse_arguments(arguments):
  """Parse command line arguments into positional parameters, options and flags."""
  positional_arguments = []
  option_values = {}
  flag_values = []

  for arg in arguments:
    if arg[0] != '-':
      positional_arguments.append(arg)
    else:
      if '=' in arg:
        pair = arg.split('=')
        value = pair[1]
        if value[0] == "'" or value[0] == '"':
          value = value[1:-1]
        if pair[0][1] == '-':
          option_values[pair[0][2:]] = value
        else:
          option_values[pair[0][1]] = value
      else:
        if arg[1] == '-':
          flag_values.append(arg[2:])
        else:
          flag_values.append(arg[1:])

  return (positional_arguments, option_values, flag_values)

def set_positional_arguments(positional_parameters, positional_arguments, command_line_options):
  """ Validate and set positional command line arguments.  """
  if len(positional_parameters) < len(positional_arguments):
    return (True, 'Too many parameters')

  if len(positional_parameters) > len(positional_arguments):
    return (True, 'Not enough required parameters')

  for i, parm  in enumerate(positional_parameters):
    command_line_options[parm] = positional_arguments[i]

  return None

def set_optional_arguments(options, option_values, command_line_options):
  """ Validate and set optional command cline arguments. """
  option_value_keys = option_values.keys()

  for option in options:
    if option[0] == '<':
      non_required_option = option[1:len(option) - 1]
      if non_required_option in option_value_keys:
        command_line_options[non_required_option] = option_values[non_required_option]
      elif non_required_option[0] in option_value_keys:
        command_line_options[non_required_option] = option_values[non_required_option[0]]

    else:
      if option in option_value_keys:
        command_line_options[option] = option_values[option]
      elif option[0] in option_value_keys:
        command_line_options[option] = option_values[option[0]]
      else:
        return (True, f'Missing required option: {option}')

  return None

def set_flag_arguments(flags, flag_values, command_line_options):
  """ Set flag command line arguments. """
  for flag in flags:
    if flag in flag_values:
      command_line_options[flag] = True
    elif flag[0] in flag_values:
      command_line_options[flag] = True
    else:
      command_line_options[flag] = False

def parse(template, arguments):
  """ Given a parsed template and arguments, create a dictionary with the template
    values assigned.

    TODO: Handle unknown arguments.
  """

  (positional_parameters, options, flags) = parse_template(template)
  (positional_arguments, option_values, flag_values) = parse_arguments(arguments)

  command_line_options = {}

  # Positionals
  val = set_positional_arguments(positional_parameters, positional_arguments, command_line_options)
  if val is not None:
    return val

  # Options
  val = set_optional_arguments(options, option_values, command_line_options)
  if val is not None:
    return val

  # Flags
  set_flag_arguments(flags, flag_values, command_line_options)

  return (False, command_line_options)
