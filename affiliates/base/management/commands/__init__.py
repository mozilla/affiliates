from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand


class QuietCommand(BaseCommand):
    """Command class that supports supressing output with a -q flag."""
    option_list = NoArgsCommand.option_list + (
        make_option('-q', '--quiet', action='store_true', dest='quiet', default=False,
                    help='If no error occurs, swallow all output.'),
    )

    def handle(self, *args, **kwargs):
        self.quiet = kwargs.get('quiet', False)
        return self.handle_quiet(*args, **kwargs)

    def handle_quiet(self, *args, **kwargs):
        raise NotImplementedError()

    def output(self, msg):
        if not self.quiet:
            print msg
