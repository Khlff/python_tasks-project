import argparse
import os
import sys


def create_parser() -> argparse.ArgumentParser:
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} PATH [--port] [-h]',
        description='It`s server_directory that accepts the url to the site '
                    'in any encoding and saves all images from it.',
    )

    parser.add_argument(
        '--port',
        '--port',
        type=int,
        default=8080,
        help='The port on which the server_directory will start. '
             '(8080 by default)',
    )
    parser.add_argument(
        '-path',
        '-PATH',
        type=str,
        help='The path where the images will be saved',
    )
    return parser
