from icalendar import Calendar
import datetime
import requests

CODE = 'FMAF05'
URL = 'http://www.maths.lth.se/media11/exams/sot/exam_%s-%s-%s.pdf'
URLSOL = 'http://www.maths.lth.se/media11/exams/sot/solution_%s-%s-%s.pdf'

with open('schema_ny.ics', 'r') as ics:
    for comp in Calendar.from_ical(ics.read()).walk('VEVENT'):
        if CODE in comp.get('summary'):
            dt = comp.get('dtstart').dt
            year = str(dt.year)
            month = str(dt.month)
            month = month if len(month) > 1 else '0'+ month
            day = str(dt.day)
            day = day if len(day) > 1 else '0'+ day
            
            response = requests.get(URL % (year, month, day), stream=True)
            if not response.ok:
                for i in range(1, 32):
                    response = requests.get(URL % (year, month, i), stream=True)
                    if response.ok:
                        break
            if response.ok:
                with open('tentor/%s_%s_%s_%s.pdf' % (CODE, year, month, day), 'wb') as f:
                    f.write(response.content)
            else:
                print(URL % (year, month, day))
            
            response_sol = requests.get(URLSOL % (year, month, day), stream=True)
            if not response_sol.ok:
                for i in range(1, 32):
                    response_sol = requests.get(URLSOL % (year, month, i), stream=True)
                    if response_sol.ok:
                        break
            if response_sol.ok:
                with open('tentor/%s_%s_%s_%sSOL.pdf' % (CODE, year, month, day), 'wb') as f:
                    f.write(requests.get(URLSOL % (year, month, day), stream=True).content)
            else:
                print(URLSOL % (year, month, day))
