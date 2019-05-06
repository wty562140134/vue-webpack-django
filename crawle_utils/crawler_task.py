import schedule
import threading


class Task:

    def __init__(self):
        self._job = None
        self._threads = []
        self._tasks = []

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Task, "_instance"):
            Task._instance = Task(*args, **kwargs)
        return Task._instance

    def set_task(self, task):
        self._tasks.append(task)

    def thread_job(self, job):
        t = threading.Thread(target=job)
        t.setDaemon(True)
        self._threads.append(t)
        t.start()

    def run(self):
        while True:
            schedule.run_pending()
            for t in self._threads:
                t.join()


def set_task(job, every=None, when_time=None, at_day_start_time='', to=None):
    """
    使用示例:
    schedule.every(10).minutes 每隔十分钟执行一次任务
    schedule.every().hour 每隔一小时执行一次任务
    schedule.every().day.at("10:30") 每天的10:30执行一次任务
    schedule.every(5).to(10).days 每隔5到10天执行一次任务
    schedule.every().monday 每周一的这个时候执行一次任务
    schedule.every().wednesday.at("13:15") 每周三13:15执行一次任务

    :param job: 需要运行的任务函数,是一个函数对象
    :type object
    :param every: schedule.every()中的传参
    :type int
    :param when_time: 是schedule中的second,minute,hours，day等
    :type str
    :param at_day_start_time:当schedule使用day时，例如schedule.every().day.at() at()中的传参
    :type str
    :param to: 当schedule需要在某一时间段或每过几天之内执行,例如schedule.every(5).to(10).days
    :type int
    """
    task = Task.instance()
    if when_time == 'day':
        if every is not None:
            sch = schedule.every().day.at(at_day_start_time).do(task.thread_job, job)
        else:
            if to is not None:
                sch = schedule.every(every).to(to).day.do(task.thread_job, job)
            else:
                sch = schedule.every().day.at(at_day_start_time).do(task.thread_job, job)
    else:
        sch = eval('schedule.every({}).{}.do(task.thread_job, job)'.format(every, when_time))
    task.set_task(sch)


def run_task():
    Task.instance().run()
