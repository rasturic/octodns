#
#
#

from os import environ
from unittest import TestCase

from octodns.context import ContextDict
from octodns.secret.environ import EnvironSecretException, EnvironSecrets


class TestEnvironSecrets(TestCase):
    def test_environ_secrets(self):
        # put some secrets into our env
        environ['THIS_EXISTS'] = 'and has a val'
        environ['THIS_IS_AN_INT'] = '42'
        environ['THIS_IS_A_FLOAT'] = '43.44'

        es = EnvironSecrets('env')

        source = ContextDict({}, context='xyz')
        self.assertEqual('and has a val', es.fetch('THIS_EXISTS', source))
        self.assertEqual(42, es.fetch('THIS_IS_AN_INT', source))
        self.assertEqual(43.44, es.fetch('THIS_IS_A_FLOAT', source))

        with self.assertRaises(EnvironSecretException) as ctx:
            es.fetch('DOES_NOT_EXIST', source)
        self.assertEqual(
            'Incorrect provider config, missing env var DOES_NOT_EXIST, xyz',
            str(ctx.exception),
        )
