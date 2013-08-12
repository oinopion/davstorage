import sys
import optparse
import unittest


def parse_options(argv):
    parser = optparse.OptionParser()
    parser.add_option(
        '-i', '--integration', action='store_true', default=False,
        help='run only integration tests',
    )
    parser.add_option(
        '-a', '--all', action='store_true', default=False,
        help='run integration and unit tests',
    )
    options, args = parser.parse_args(argv)
    return options

if __name__ == '__main__':
    options = parse_options(sys.argv)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if options.all or options.integration:
        integration = loader.discover('.', pattern='integration*.py')
        suite.addTest(integration)
    if options.all or not options.integration:
        unit = loader.discover('.', pattern='test*.py')
        suite.addTest(unit)

    runner = unittest.TextTestRunner()
    runner.run(suite)

