import sys
from subprocess import PIPE, Popen

from nose.tools import assert_equals, assert_in

from .assert_equals_with_unidiff import assert_equals_with_unidiff as assert_equals


class TestScriptsSmoke:
    def test_trash_rm_works(self):
        self.run_script('trash-rm')
        assert_in('Usage:', self.stderr.splitlines())

    def test_trash_put_works(self):
        self.run_script('trash-put')
        assert_in('Usage: trash-put [OPTION]... FILE...', self.stderr.splitlines())

    def test_trash_put_touch_filesystem(self):
        self.run_script('trash-put', 'non-existent')
        assert_equals('trash-put: cannot trash non existent "non-existent"\n', self.stderr)

    def run_script(self, script, *args):
        process = Popen([sys.executable, script] + list(args),
                        env={'PYTHONPATH': '.'},
                        stdin=None,
                        stdout=PIPE,
                        stderr=PIPE)

        (self.stdout, self.stderr) = process.communicate()
        self.stderr = self.stderr.decode('utf-8')
        process.wait()
        self.returncode = process.returncode
