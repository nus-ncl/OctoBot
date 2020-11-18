#!/usr/bin/python3

from octoplay_utils import user_commands, utils, user_functions
from octoplay_utils.completer import Completer
import code
import sys
import requests
import readline

console = None
initial_locals = {}

functions = {user_functions.read_file.__name__: user_functions.read_file}

commands = {"currentConfig": user_commands.get_current_config,
            "getName": user_commands.get_name,
            "setName": user_commands.set_name,
            "getBotNumbers": user_commands.get_bot_numbers,
            "setBotNumbers": user_commands.set_bot_numbers,
            "getExecutors": user_commands.get_executors,
            "addExecutor": user_commands.add_executor,
            "deleteExecutor": user_commands.del_executor,
            "openProxy": user_commands.open_proxy,
            "setPort": user_commands.set_port,
            "loadFile": user_commands.load_file,
            "writeFile": user_commands.write_file,
            "runFile": user_commands.run_file,
            "patchFile": user_commands.patch_file,
            "stopFile": user_commands.stop_file,
            "checkStatus": user_commands.check_status,
            "runJob": user_commands.run_job,
            "getShell": user_commands.get_shell,
            "deleteBot": user_commands.delete_bot,
            "getLogs": user_commands.get_logs,
            "getLogsByCmd": user_commands.get_logs_by_command,
            "exit": user_commands.exit
            }


def help(command=None):
    if command is None:
        print("\nList of commands")
        print(list(commands.keys()))

        print("\nList of functions")
        print(list(functions.keys()))

        print('Type help <commandName> for help on syntax\n'
              'Example - help getName\n')
    else:
        # Get the function object
        is_command = True
        fun = commands.get(command, None)
        if fun is None:
            fun = functions.get(command, None)
            is_command = False

        if fun is None:  # If cannot find for such functions
            print(f'No help found for \'{command}\'', file=sys.stderr)
            return

        if is_command:
            # Get all the lines
            lines = fun.__doc__.split("\n")
            print(f'{command} {lines[0].strip()}')

            for line in lines[1:]:
                print("\t" + line.strip())
        else:
            __builtins__.get('help')(fun)


def get_user_vars():
    return {k: console.locals.get(k, None)
            for k in (set(console.locals) - set(initial_locals))}


def parse(cmd, args):
    """Based on the line that the user inputs, run the appropriate command"""

    # Get the function object
    cmd = commands[cmd]

    # Run the function depending on whether how many args it wants
    try:
        if args == '':  # If the function does not accept any parameters,
            # then do not give it any
            output = cmd()
        else:
            output = cmd(args)

        # Prints the output
        if output is not None:
            print(output)

    except Exception as e:
        print(f"Exception: {e}")


def get_prompt():
    # Use filename as prompt header
    curr_filename = sys.argv[0]
    return f"{curr_filename}:~$ "


# Verifies connection with the kubernetes api
def check_connection():
    has_error = False
    resp = None

    # Checks connection to the api
    try:
        resp = requests.get(f"http://localhost:{utils.K8S_PORT}/api")
    except requests.exceptions.ConnectionError as e:
        has_error = True

    # If has error, then notify user
    if resp is None or resp.status_code != 200 or has_error:
        print("Failed to connect to kubernetes api. "
              "Opening proxy...", file=sys.stderr)
        user_commands.open_proxy()


def read_function(prompt):
    """This function is responsible for reading the input
    from the python interpreter"""

    # Read line from input
    line = input(prompt)

    # Sanitize the input
    line = line.rstrip('\r\n')
    orig_line = line  # Saves the original line
    # so that 100% the line won't get modified

    # Checks against any command that is user defined
    # Obtain the command
    line = line.split(" ")
    command = line[0]
    args = " ".join(line[1:])

    # Parse the argument
    if 'help' == command:
        help(args if args.strip() != '' else None)
        return ''
    elif command in commands:
        parse(command, args)
        return ''
    else:
        return orig_line


def interactive():
    """Starts the interactive prompt"""

    # Verifies whether the program can talk to the kubectl api
    check_connection()

    # Defines important variables
    banner = "Type 'help' to display available commands\n" \
             "Type 'exit' to exit the program"
    exit_msg = "Exiting..."
    sys.ps1 = get_prompt()

    # Configures completer
    comp = Completer(list(commands.keys()) + list(functions.keys()))
    readline.set_completer_delims(" \n\t;\"'")  # we want to treat '/'
    # as part of a word, so override the delimiters
    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete)

    # Starts the actual python terminal
    global initial_locals
    initial_locals = dict(globals(), **locals())

    global console
    console = code.InteractiveConsole(locals=dict(globals(), **locals()))
    console.raw_input = read_function
    console.push(f'from {__package__} import *')  # Import own module
    # into the interactive console
    console.interact(banner=banner, exitmsg=exit_msg)
