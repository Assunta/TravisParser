import logging.handlers

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from Flask_App.utilityClasses.ContextProvider import ContextualFilter
from utility.dbUtility import readDbLogin


def getLogger():
    # logging
    LOG_FILENAME = "log.log"
    # Set up a specific logger with our desired output level
    log = logging.getLogger('MainLogger')
    log.setLevel(logging.DEBUG)
    context_provider = ContextualFilter()
    log.addFilter(context_provider)
    # Add the log message handler to the logger
    h = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", interval=1)
    h.suffix = "%Y%m%d"
    fmt = logging.Formatter('''
        Time: %(asctime)s
        Level: %(levelname)s
        Method: %(method)s
        Path: %(url)s
        IP: %(ip)s
        User ID: %(user_id)s
        Message: %(message)s
        ---------------------''')

    h.setFormatter(fmt)
    hConsole = logging.StreamHandler()
    hConsole.setFormatter(fmt)
    log.addHandler(h)
    log.addHandler(hConsole)
    return log

def configureScheduler():
    dbCredentials = readDbLogin()
    uri = "mysql+mysqlconnector://" + dbCredentials[1] + ":" + dbCredentials[2] + "@" + dbCredentials[0] + "/travisdb"
    jobstores = {
        'default': SQLAlchemyJobStore(url=uri)
    }
    scheduler = BackgroundScheduler(jobstores=jobstores)
    return scheduler

def getLoggerScheduler():
    LOG_FILENAME="logScheduler.log"
    logAps = logging.getLogger('apscheduler.executors.default')
    logAps.setLevel(logging.INFO)
    hAps = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", interval=1)
    hAps.suffix = "%Y%m%d"
    fmt = logging.Formatter('%(asctime)s-%(levelname)s-%(name)s-%(message)s')
    hAps.setFormatter(fmt)
    logAps.addHandler(hAps)
    return logAps