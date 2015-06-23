#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by lingjiao.lc

"""
Note, in my script, a tab equals four blanks.
You must have a check of your indentation.
"""

import os
import sys

from oslo.config import cfg
import inspect
import logging
from logging.handlers import RotatingFileHandler
import logging.handlers

CONF = cfg.CONF

CONF.register_cli_opts([
    cfg.IntOpt('default-log-level', default=None, help='default log level'),
    cfg.BoolOpt('verbose', default=False, help='show debug output'),
    cfg.BoolOpt('use-stderr', default=True, help='log to standard error'),
    cfg.BoolOpt('use-syslog', default=False, help='output to syslog'),
    cfg.StrOpt('log-dir', default='/tmp', help='log file directory'),
    cfg.StrOpt('log-file', default=None, help='log file name'),
    cfg.StrOpt('log-file-mode', default='0644',
               help='default log file permission')
])


_EARLY_LOG_HANDLER = None


def early_init_log(level=None):
    global _EARLY_LOG_HANDLER
    _EARLY_LOG_HANDLER = logging.StreamHandler(sys.stderr)

    log = logging.getLogger()
    log.addHandler(_EARLY_LOG_HANDLER)
    if level is not None:
        log.setLevel(level)


def _get_log_file():
    if CONF.log_file:
        return CONF.log_file
    if CONF.log_dir:
        return os.path.join(CONF.log_dir,
                            os.path.basename(inspect.stack()[-1][1])) + '.log'
    return None

def init_log():
    global _EARLY_LOG_HANDLER

    log = logging.getLogger()
    if CONF.use_stderr:
        log.addHandler(logging.StreamHandler(sys.stderr))
    if _EARLY_LOG_HANDLER is not None:
        log.removeHandler(_EARLY_LOG_HANDLER)
        _EARLY_LOG_HANDLER = None

    if CONF.use_syslog:
        syslog = logging.handlers.SysLogHandler(address='/dev/log')
        log.addHandler(syslog)

    log_file = _get_log_file()
    if log_file is not None:
        handler = logging.handlers.WatchedFileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s [-] %(message)s from (pid=%(process)d) %(funcName)s %(pathname)s:%(lineno)d')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        mode = int(CONF.log_file_mode, 8)
        os.chmod(log_file, mode)

    if CONF.default_log_level is not None:
        log.setLevel(CONF.default_log_level)
    elif CONF.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

class Logger(object):
    def __init__(self, logName, logDir, logFile):
        logFile = '%s/%s' % (logDir.rstrip('/'), logFile)
        self._logger = logging.getLogger(logName)
        handler = logging.FileHandler(logFile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s [-] %(message)s from (pid=%(process)d) %(funcName)s %(pathname)s:%(lineno)d')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def info(self, msg):
        self._logger.info(msg)
    
    def error(self, msg):
        self._logger.error(msg)

    def debug(self, msg):
        self._logger.debug(msg)

    def warn(self, msg):
        self._logger.warn(msg)
        
    def exception(self, msg):
        self._logger.exception(msg)
        
    def critical(self, msg):
        self._logger.critical(msg)


log_map = {}
def setup_logging(logger, logfile, logdir=CONF.log_dir, scrnlog=True, txtlog=True, loglevel=logging.DEBUG):
    if log_map.get(logger, ''):
        return
    else:
        log_map[logger] = logger
    
    logdir = os.path.abspath(logdir)

    if not os.path.exists(logdir):
        os.mkdir(logdir)

    log = logging.getLogger(logger)
    log.setLevel(loglevel)

    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s [-] %(message)s from (pid=%(process)d) %(funcName)s %(pathname)s:%(lineno)d')

    if txtlog:
        txt_handler = RotatingFileHandler(os.path.join(logdir, logfile), backupCount=5)
        txt_handler.setFormatter(log_formatter)
        log.addHandler(txt_handler)
        log.info("Logger initialised.")

if __name__ == "__main__":
    pass

