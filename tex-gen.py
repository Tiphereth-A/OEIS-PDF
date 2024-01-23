#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os

import click
import coloredlogs
from libs.decorator import withlog
from libs.CommandGenerator import CommandGenerator


@click.group()
@click.option('-l', '--level', type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']), help='log level',
              default='INFO')
def cli(level: str):
    coloredlogs.install(milliseconds=True,
                        level=level,
                        fmt='%(asctime)s:%(msecs)03d %(levelname)s %(programname)s::%(name)s [%(process)d] %(message)s',
                        field_styles={'asctime': {'color': 'green'},
                                      'msecs': {'color': 'green'},
                                      'hostname': {'color': 'red'},
                                      'levelname': {'bold': True, 'color': 'magenta'},
                                      'name': {'faint': True, 'color': 'blue'},
                                      'programname': {'bold': True, 'color': 'cyan'},
                                      'process': {'faint': True, 'color': 'green'},
                                      'username': {'color': 'yellow'}},
                        level_styles={'critical': {'bold': True, 'color': 'red'},
                                      'debug': {'color': 'cyan'},
                                      'error': {'color': 'red'},
                                      'info': {'bright': True, 'color': 'white'},
                                      'notice': {'color': 'magenta'},
                                      'spam': {'color': 'green', 'faint': True},
                                      'success': {'bold': True, 'color': 'green'},
                                      'verbose': {'color': 'blue'},
                                      'warning': {'bright': True, 'color': 'yellow'}})


@cli.command('gen')
@click.option('-o', '--out', type=click.Path(exists=True), default='tex', help='Output folder, default "tex"')
@click.argument('data', default='data/detail', type=click.Path(exists=True))
def _gen_tex_commands(out, data):
    """Generate LaTeX commands"""

    @withlog
    def gen_tex_commands(_out_folder: str, _data_folder: str, **kwargs):
        logger = kwargs.get('logger')

        with open(os.path.join(_out_folder, 'oeis.tex'), 'w') as f_out:
            for dir_path, _, filenames in os.walk(_data_folder):
                l: list = sorted(CommandGenerator(*i) for i in [(name.removesuffix('.json'), json.load(open(
                    os.path.join(dir_path, name), 'r'))) for name in filter(lambda x: x.endswith('.json'), filenames)])
            f_out.writelines(i.str_tex() + '\n\n' for i in l)

    gen_tex_commands(click.format_filename(out), click.format_filename(data))


if __name__ == '__main__':
    cli()
