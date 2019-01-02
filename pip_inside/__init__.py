from glob import glob
import os
from pprint import pprint
import shlex
import six
from subprocess import check_call
import sys
from warnings import warn

try:
    from pip._internal.commands import InstallCommand
    install_cmd = InstallCommand()
except ModuleNotFoundError:
    raise ModuleNotFoundError('Please install pip for the current '
                              'interpreter: (%s).' % sys.executable)

pipfiles = []
for i in range(4):  # 4 is completely arbitrary here
    pipfiles.extend(glob(('..' + os.sep) * i + 'Pipfile'))
if pipfiles:
    pipfiles = [os.path.abspath(f) for f in pipfiles]
    msg = ('Warning: the following Pipfiles will be bypassed by '
           'pip_inside.install:\n\t' + '\n\t'.join(pipfiles))
    warn(msg, stacklevel=2)


def install(*args, **kwargs):
    """Install packages into the current environment.

    Equivalent examples of command-line pip and pip_inside are grouped below.

    METHOD 1: Single argument is exactly the same as command line interface,
    beginning with 'pip install ...'

    $ pip install --user --upgrade some_pkg
    >>> install('pip install --user --upgrade some_pkg')

    METHOD 2: Arguments from command-line implementation split on spaces

    $ pip install some_pkg
    >>> install('some_pkg')

    $ pip install --user --upgrade some_pkg
    >>> install('--user', '--upgrade', 'some_pkg')
    >>> install(*'--user --upgrade some_pkg'.split())

    If preferred, keyword-value arguments can also be used:

    $ pip install -r requirements.txt
    >>> install(r='requirements.txt')
    >>> install('-r', 'requirements.txt')
    >>> install(*'-r requirements.txt'.split())

    $ pip install --no-index --find-links=/local/dir/ some_pkg
    # Note the use of '_' in the following keyword example.
    >>> install('--no-index', 'some_pkg', find_links='/local/dir/')
    >>> install('--no-index', '--find-links=/local/dir/', 'some_pkg')
    >>> install(*'--no-index --find-links=/local/dir/ some_pkg'.split())

    """
    if len(args) == 1 and args[0].startswith('pip install '):
        cli_args = shlex.split(args[0])
    else:
        cli_args = ['pip', 'install']
        for k, v in kwargs.items():
            if len(k) == 1:  # short flag
                cli_args.append("-" + k)
                if isinstance(v, six.string_types):  # Non-string = boolean
                    cli_args.append(v)
            else:  # long flag
                cli_args.append("--" + k.replace('_', '-'))
                if isinstance(v, six.string_types):  # Non-string = boolean
                    cli_args.append(v)
        cli_args += args
    # use pip internals to isolate package names
    opt_dict, targets = install_cmd.parse_args(cli_args)
    assert targets[:2] == ['pip', 'install']
    targets = set(targets[2:])
    already_loaded = {n: mod for n, mod in sys.modules.items() if n in targets}
    print('Trying  ', ' '.join(cli_args), '  ...')
    result = check_call([sys.executable, "-m", *cli_args])
    print(result)

    if result == 0 and already_loaded:
        print('The following modules were already loaded. You may need to '
              'restart python to see changes: ')
        pprint(already_loaded)
