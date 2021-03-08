"""
Task3.

Некоторое количество человек то наливают воду в бочку, то черпают из бочки. Если человек 
пытается налить больше воды, чем есть свободного объема – это ошибка, при этом объем воды в 
бочке не меняется. Так же если человек пытается зачерпнуть больше воды, чем есть в бочке –
ошибка, объем воды также при этом не меняется. В остальных случаях – успех.
Вам дан лог файл. Напишите программу, которая ответит на следующие вопросы:
- какое количество попыток налить воду в бочку было за указанный период?
- какой процент ошибок был допущен за указанный период?
- какой объем воды был налит в бочку за указанный период?
- какой объем воды был не налит в бочку за указанный период?
- … тоже самое для забора воды из бочки …
- какой объем воды был в бочке в начале указанного периода? Какой в конце указанного 
периода?
Путь к логу, желаемый период – подаются в качестве аргументов командной строки. Результат 
записывается в csv файл (с наименованием столбцов).
Пример строки запуска: java –jar App ./log.log 2020-01-01T12:00:00 2020-01-01T13:00:00
Пример лог файла:
    META DATA:
    200 (объем бочки)
    32 (текущий объем воды в бочке)
    2020-01-01Т12:51:32.124Z – [username1] - wanna top up 10l (успех)
    2020-01-01Т12:51:34.769Z – [username2] - wanna scoop 50l (фейл)
    …

Примечание: для проверки сгенерируйте лог файл объемом 1 Mb, приложите его к решению. 
Обратите внимание, искомого временного интервала может не быть в логе, приложение не 
должно при этом крашиться. Если аргументы поданы не верно, в stdout должен выводится usage.

"""
import csv
import re
import sys
from pathlib import Path

CSV_FILE = 'result.csv'


def analyze_logs(file: str, *period: tuple) -> None:
    try:
        log: list = _get_log_list(file)
        period_log: list = _get_desired_period(log, period)
        if not period_log: return _show_usage('MISC')
    except FileNotFoundError: return _show_usage('FILE')
    except IndexError: return _show_usage('COORDINATES')

    before, after = _get_volume_before_and_after(period_log)
    tries_top_up: int = _get_count_tries('top up', period_log)
    tries_scoop: int = _get_count_tries('scoop', period_log)
    failure_rate_top_up: int = _get_failure_rate(tries_top_up, '(фейл)', period_log)
    failure_rate_scoop: int = _get_failure_rate(tries_scoop, '(фейл)', period_log)
    success_top_up: int = _get_volume_with_actions('top up', '(успех)', period_log)
    failure_top_up: int = _get_volume_with_actions('top up', '(фейл)', period_log)
    success_scoop: int = _get_volume_with_actions('scoop', '(успех)', period_log)
    failure_scoop: int = _get_volume_with_actions('scoop', '(фейл)', period_log)

    _report(**locals())
    _write_csv(**locals())


def _get_log_list(file: str) -> list:
    with open(file) as f: return f.readlines()


def _get_desired_period(log: list, period: tuple) -> list:
    return [line for line in log if period[0] in line or period[1] in line]


def _get_volume_before_and_after(period: list) -> tuple:
    return _get_liters(period[0]), _get_liters(period[-1])


def _get_count_tries(act: str, period: list) -> int:
    return len([p for p in period if act in p])


def _get_failure_rate(tries: int, status: str, period: list) -> int:
    return round(len([p for p in period if status in p]) / tries * 100)


def _get_volume_with_actions(act: str, status: str, period: list) -> int:
    return sum([_get_liters(p) for p in period if act in p and status in p])


def _get_liters(period: str) -> int:
    return int(re.search(r'(\d+)l', period).group()[:-1])


def _write_csv(**kw: dict) -> None:
    for key in ('file', 'log', 'period', 'period_log'): kw.pop(key)

    with open(Path(__file__).with_name(CSV_FILE), 'a') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerows((kw.keys(), kw.values()))


def _show_usage(op_code: str) -> None:
    example = 'Пример строки запуска: python3 task3.py ./log.log 2020-01-01T12:00:00 2020-01-01T13:00:00'
    invalid = {'COORDINATES': 'Вы ввели некорректные координаты, попробуйте еще раз!',
               'MISC': 'Кажется, Вы ввели недостаточное кол-во аргументов.',
               'FILE': 'Файл не найден, введите корректный путь.'}[op_code]
    print(invalid, example, sep='\n')


def _report(**kw: dict) -> None: print(
        f'- [start ] объем воды был в бочке в начале указанного периодa: {kw.get("before")}',
        f'- [top up] количество попыток налить воду в бочку было за указанный период: {kw.get("tries_top_up")}',
        f'- [top up] процент ошибок был допущен за указанный период: {kw.get("failure_rate_top_up")}',
        f'- [scoop ] количество попыток забора воды из бочки было за указанный период: {kw.get("tries_scoop")}',
        f'- [scoop ] процент ошибок был допущен за указанный период: {kw.get("failure_rate_scoop")}',
        f'- [top up] объем воды был налит в бочку за указанный период: {kw.get("success_top_up")}',
        f'- [top up] объем воды был не налит в бочку за указанный период: {kw.get("failure_top_up")}',
        f'- [scoop ] объем воды был изьят из бочки за указанный период: {kw.get("success_top_up")}',
        f'- [scoop ] объем воды не был изьят из бочки за указанный период: {kw.get("failure_top_up")}',
        f'- [finish] объем воды был в бочке в конце указанного периода: {kw.get("after")}',
        sep='\n'
    )

analyze_logs(*sys.argv[1:])
