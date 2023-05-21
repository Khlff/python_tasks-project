import argparse
import os
import sys


def create_parser() -> argparse.ArgumentParser:
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} -path -mode [--port] [--help]',
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
    parser.add_argument(
        "-mode",
        "-MODE",
        type=str,
        help="Flag that sets the server operation mode.\n"
             "[adblocker] - the mode of operation of the server in which\n"
             "the html page is sent to the client without advertising.\n"
             "[downloader] - the mode of operation of the server in which\n"
             "it downloads images from the specified url.\n"
             "[vk_downloader]] - the mode of operation of the server in which\n"
             "it downloads images from the specified album in vk."
    )
    return parser
