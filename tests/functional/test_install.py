from pip_inside import _build_install_cmd
from pip_inside import install

"""
TODO(RJR) implement the following tests

install("pip install --target /tmp//target_dir_without_spaces ''")
install("pip install --target '/tmp//target dir with spaces' ''")
install("<full-path-to-v1.0-sample-wheel>", target="/tmp//") followed by install("<full-path-to-v2.0-sample-wheel>", target="/tmp//", upgrade=True)  # noqa: E501
"""


def test_build_install_cmd_plain():
    assert (_build_install_cmd('pip install some_pkg')
            == ['pip', 'install', 'some_pkg'])
    assert (_build_install_cmd('some_pkg')
            == ['pip', 'install', 'some_pkg'])


def test_build_install_cmd_user():
    assert (_build_install_cmd('pip install --user some_pkg')
            == ['pip', 'install', '--user', 'some_pkg'])
    assert (_build_install_cmd('some_pkg', user=True)
            == ['pip', 'install', '--user', 'some_pkg'])


def test_build_install_cmd_kwarg():
    assert (_build_install_cmd('pip install -r requirements.txt')
            == ['pip', 'install', '-r', 'requirements.txt'])
    assert (_build_install_cmd(r='requirements.txt')
            == ['pip', 'install', '-r', 'requirements.txt'])


def test_build_install_cmd_underscores():
    assert (_build_install_cmd('pip install --find-links /local/dir/ some_pkg')
            == ['pip', 'install', '--find-links', '/local/dir/', 'some_pkg'])
    assert (_build_install_cmd('some_pkg', find_links='/local/dir/')
            == ['pip', 'install', '--find-links', '/local/dir/', 'some_pkg'])


def test_install_simplewheel():
    wheel_path = 'tests/data/packages/'
    wheel1 = wheel_path + 'simplewheel-1.0-py2.py3-none-any.whl'
    assert install(wheel1) == 0
    # the following tests were suggested by @ncoghlan
    # install("pip install --target /tmp//target_dir_without_spaces ''")
    # install("pip install --target '/tmp//target dir with spaces' ''")
    # install(wheel1, target="/tmp//")
    # install(wheel2, target="/tmp//", upgrade=True)


def test_already_loaded():
    wheel_path = 'tests/data/packages/'
    wheel1 = wheel_path + 'simplewheel-1.0-py2.py3-none-any.whl'
    wheel2 = wheel_path + 'simplewheel-2.0-py2.py3-none-any.whl'
    assert install(wheel1) == 0
    import simplewheel  # noqa: F401
    assert install(wheel2) == 0
