import os
from datetime import datetime

from minihelper_backend import settings
import logging

from utils.mailutil import send_mail

logger = logging.getLogger('django')

def statistics():
    # 读取统计的Tog内容
    data_file = os.path.join(settings.BASE_DIR, 'log', 'stat.log')
    if not os.path.exists(data_file):
        logger.warning("File not exists. file=[%s]" % data_file)
        return

    result = {}
    with open(data_file, 'r') as data_file:
        for line in data_file:
            line = line.strip()
            content = line.split(' ')[2]
            content_list = content.split(settings.STATISTICS_SPLIT_FLAG)
            log_time = int(content_list[0].split('=')[1][1:-1])
            path = content_list[1].split('=')[1][1:-1]
            full_path = content_list[2].split('=')[1][1:-1]
            cost = float(content_list[3].split('=')[1][1:-1])

            if path not in result.keys():
                result[path] = []
            result[path].append(cost)

    # report max, min, mean
    report_content = []
    for k, v_list in result.items():
        # 请求次数
        count = len(v_list)
        # 最大值
        v_max = max(v_list)
        # 最小值
        v_min = min(v_list)
        # 平均值
        v_avg = sum(v_list) * 1.00 / count
        content = ('%-40s COUNT: %d MAX_TIME: %.4f(s) MIN_TIME: %.4f(s) AVG_TIME: %.4f(s)'
                   % (k, count, v_max, v_min, v_avg))
        report_content.append(content)

    return report_content


def report_by_mail():
    logger.info('Begin statistics data.')
    content = statistics()
    content = '\r\n'.join(content)
    logger.info('End statistics data.')
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    subject = '[Minihelper Backend Django Service Performance Monitor]---' + date_time_str
    send_mail(content, subject)