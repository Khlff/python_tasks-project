import argparse
import os
import sys


def create_parser() -> argparse.ArgumentParser:
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} -path [--port] [--help]',
        description='This is an http server that operates in two modes:'
                    ' 1)Accepts the URL of the site in any encoding'
                    ' and saves all images from it.'
                    ' A gui client is written for this mode. '
                    '2)Accepts the URL of the site in any encoding'
                    ' and sends the html of this site with the cut-out'
                    ' advertisement.',
    )

    parser.add_argument(
        '--port',
        '--port',
        type=int,
        default=8080,
        help='The port on which the server_package will start. '
             '(8080 by default)',
    )
    parser.add_argument(
        '-path',
        '-PATH',
        type=str,
        help='The path where the images will be saved',
    )
    return parser
