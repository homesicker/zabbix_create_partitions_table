import time
import datetime
import calendar
import numpy as np

calendar.setfirstweekday(0)

start = datetime.datetime.strptime("01-01-2020 00:00:00", "%d-%m-%Y %H:%M:%S")

forward_year = 16

table = 'history_uint'

def get_mw(year, month, day):
    x = np.array(calendar.monthcalendar(year, month))
    mw = np.where(x==day)[0][0] + 1
    return mw

def gen_sqlq(ufdt, uldt, fdt):
    w =  get_mw(year=fdt.year, month=fdt.month, day=fdt.day)
    q = "CREATE TABLE %s_%s_%s_%sw PARTITION OF %s FOR VALUES FROM (%s) TO (%s);\n" % (table, fdt.year, fdt.month, w, table, ufdt, uldt)
    f = open("./sqlq.txt", "a")
    f.write(q)
    f.close()


def get_dt(cm, year, month):
    if len(cm) == 1:
        fdt = datetime.datetime(day=cm[0], month=month, year=year, hour=0, minute=0, second=0)
        ldt = datetime.datetime(day=cm[0], month=month, year=year, hour=0, minute=0, second=0) + datetime.timedelta(days=1)
        ufdt = int(time.mktime(fdt.timetuple()))
        uldt = int(time.mktime(ldt.timetuple()))
        gen_sqlq(ufdt=ufdt, uldt=uldt, fdt=fdt)
    if len(cm) >= 2:
        fdt = datetime.datetime(day=cm[0], month=month, year=year, hour=0, minute=0, second=0)
        ldt = datetime.datetime(day=cm[-1], month=month, year=year, hour=0, minute=0, second=0) + datetime.timedelta(days=1)
        ufdt = int(time.mktime(fdt.timetuple()))
        uldt = int(time.mktime(ldt.timetuple()))
        gen_sqlq(ufdt=ufdt, uldt=uldt, fdt=fdt)

def add_month(dt, months):
    m = dt.month - 1 + months
    y = dt.year + months // 12
    m = m % 12 +1
    d = min(dt.day, calendar.monthrange(year=y, month=m)[1])
    return datetime.date(year=y, month=m, day=d)

def gen_cm(dt):
    cr = calendar.monthcalendar(dt.year, dt.month)
    for i in range(0, len(cr)):
        m = calendar.monthcalendar(dt.year, dt.month)[i]
        cm = [x for x in m if x != 0]
        get_dt(cm, dt.year, dt.month)

for i in range(0, forward_year):
    for i in range(0, 12):
        gen_cm(start)
        start = add_month(start, 1)
    start = datetime.date(year=start.year + 1, month=start.month, day=start.day)
