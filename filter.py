#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import re

import click
import coloredlogs
from libs.decorator import withlog
from libs.predicate import *


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


RE_OEIS_ID = re.compile(r'A\d+')


@cli.command('clean')
@click.argument('folder', type=click.Path(exists=True), default='data/detail')
def _filter_results(folder):
    """Filter results

    Remove all sequences with no valid formula"""

    def check(_single_result: dict) -> bool:
        return 'formula' in _single_result.keys() and 'data' in _single_result.keys()

    @withlog
    def filter_results(_result_folder: str, **kwargs):
        logger = kwargs.get('logger')

        __remove_cnt, __clean_cnt, __total_cnt = 0, 0, sum(
            len(filenames) for _, __, filenames in os.walk(_result_folder))
        __flag: bool = True

        while __flag:
            __flag = False
            __id_set: set = set()
            for dir_path, _, filenames in os.walk(_result_folder):
                __id_set = __id_set.union(
                    x.removesuffix('.json') for x in filter(lambda x: x.endswith('.json'), filenames))

            for dir_path, _, filenames in os.walk(_result_folder):
                for name in filter(lambda x: x.endswith('.json'), filenames):
                    filename = os.path.join(dir_path, name)
                    logger.debug(f'reading {filename}')
                    now_json: dict = json.load(open(filename, 'r'))
                    if not check(now_json):
                        logger.debug(
                            f'remove {filename} because of failing check')
                        os.remove(filename)
                        __remove_cnt += 1
                        __flag = True
                    else:
                        new_formulas: list[str] = list(
                            filter(lambda x: all(i in __id_set for i in re.findall(RE_OEIS_ID, x)),
                                   now_json['formula']))
                        if new_formulas:
                            if now_json['formula'] != new_formulas:
                                __clean_cnt += 1
                                now_json['formula'] = new_formulas
                                json.dump(now_json, open(filename, 'w'))
                        else:
                            logger.debug(
                                f'remove {filename} because of no valid formula')
                            os.remove(filename)
                            __remove_cnt += 1
                            __flag = True

        logger.info(f'{__remove_cnt} / {__total_cnt} result(s) removed')
        logger.info(f'{__clean_cnt} / {__total_cnt} result(s) cleaned')

    filter_results(click.format_filename(folder))


@cli.command('rmbad')
@click.argument('folder', type=click.Path(exists=True), default='data/detail')
def _remove_bad_results(folder):
    """Remove bad results"""

    @withlog
    def remove_bad_results(_result_folder: str, **kwargs):
        logger = kwargs.get('logger')

        __remove_cnt, __total_cnt = 0, 0
        for dir_path, _, filenames in os.walk(_result_folder):
            for name in filter(lambda x: x.endswith('.json'), filenames):
                filename = os.path.join(dir_path, name)
                __total_cnt += 1
                try:
                    if not os.path.getsize(filename):
                        raise Exception(f'Empty file: {filename}')
                    if json.load(open(filename, 'r'))['number'] != int(name.removeprefix('A').removesuffix('.json')):
                        raise Exception('Invalid result')
                except Exception as e:
                    os.remove(filename)
                    __remove_cnt += 1
        logger.info(f'{__remove_cnt} / {__total_cnt} bad result(s) removed')

    remove_bad_results(click.format_filename(folder))


@cli.command('reduce')
@click.option('-k', '--key', required=True, multiple=True, help='Key which will be removed')
@click.argument('folder', type=click.Path(exists=True), default='data/detail')
def _reduce_results(key: tuple[str, ...], folder):
    """Remove some keys in results"""

    @withlog
    def reduce_results(_key_removed: set[str], _result_folder: str, **kwargs):
        logger = kwargs.get('logger')

        for dir_path, _, filenames in os.walk(_result_folder):
            for name in filter(lambda x: x.endswith('.json'), filenames):
                filename = os.path.join(dir_path, name)
                json.dump(dict([(k, v) for k, v in json.load(open(filename, 'r')).items() if k not in _key_removed]),
                          open(filename, 'w'))

    reduce_results(set(key), click.format_filename(folder))


if __name__ == '__main__':
    cli()
