from icalendar import Calendar
import datetime
import requests

CODE = 'FMAF05'
URL = 'http://www.maths.lth.se/media11/exams/sot/exam_%s-%s-%s.pdf'
URLSOL = 'http://www.maths.lth.se/media11/exams/sot/solution_%s-%s-%s.pdf'

with open('schema.ics', 'r') as ics:
    for comp in Calendar.from_ical(ics.read()).walk('VEVENT'):
        if CODE in comp.get('summary'):
            dt = comp.get('dtstart').dt
            year = str(dt.year)
            month = str(dt.month)
            month = month if len(month) > 1 else '0'+month
            day = str(dt.day)
            day = day if len(day) > 1 else '0'+day
            with open('tentor/%s_%s_%s_%s.pdf' % (CODE, year, month, day), 'wb') as f:
                f.write(requests.get(URL % (year, month, day), stream=True).content)
            with open('tentor/%s_%s_%s_%sSOL.pdf' % (CODE, year, month, day), 'wb') as f:
                f.write(requests.get(URLSOL % (year, month, day), stream=True).content)
