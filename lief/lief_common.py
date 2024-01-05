import argparse
from lief.logging import LOGGING_LEVEL

LOG_LEVEL_MAP = {
        'critical': LOGGING_LEVEL.CRITICAL,
        'debug': LOGGING_LEVEL.DEBUG,
        'error': LOGGING_LEVEL.ERROR,
        'info': LOGGING_LEVEL.INFO,
        'trace': LOGGING_LEVEL.TRACE,
        'warning': LOGGING_LEVEL.WARNING,
}

def argparse_default(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('--log-level', choices=[l for l in LOG_LEVEL_MAP], default='info')
    return parser

def log_level_lookup(level: str) -> LOGGING_LEVEL:
    return LOG_LEVEL_MAP[level]
