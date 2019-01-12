from celery.decorators import task 
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from searchgoods.crawler1 import *

logger = get_task_logger(__name__)  


@periodic_task(  
    run_every=(crontab(minute='*/10')),
    name="momo_task",  
    ignore_result=True  
)
def momo_task():
    
    momocrawler()
    logger.info("crawled_momo")

@periodic_task(  
    run_every=(crontab(minute='*/600')),
    name="pchome_task",  
    ignore_result=True  
)  
def pchome_task():
    
    pchomecrawler()  
    logger.info("crawled_pchome")
