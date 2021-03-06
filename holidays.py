# make sure we have the right python version
import sys
python_required = (2,7)
python_inuse = sys.version_info
class VersionError(Exception):
    pass
if python_inuse < python_required:
    raise VersionError, 'holidays module requires python 2.7 or higher'

# carry on
import calendar
from datetime import date

currentyear = date.today().year


def firstcap(s):
    return s[0].upper() + s[1:].lower()


def checkweek(week, dow, month):
    '''take given 'week' of datetime.date() objects as gathered by:
         calendar.Calendar.monthdatescalendar(year, month)[N]
       and 'day of week' as requested, evaluate whether or not the given day of
       the week falls within the given month (ie: neither in the previous nor
       in the next month), and return True or False based on that
       evaluation.'''
    check = week[list(calendar.day_name).index(firstcap(dow))].month
    if check == month:
        return True
    else:
        return False


def holidayis(month, dom=False, day=False, year=currentyear,
              beforeorafter='default'):
    '''validate a given date, and return the appropriate work day to reflect
       the holiday, provided the parameters.

       arguments:
         month: typical integer value for month beginning with January = 1
         year:  defaults to current year, if unspecified

         optional, but at least one is required:
           dom:  integer value for day of month (eg: the fourth = 4)
           day:  description of a day in a month (eg: "last Monday" or "fourth
                 Thursday"). possible values for day:
                   - first
                   - second
                   - third
                   - fourth
                   - last

         possible values for beforeorafter, and their behavior:
          - default: picks the Friday before if it falls on a Saturday, and the
                     Monday after if it falls on a Sunday
          - before:  forces to the Friday before
          - after:   forces to the Monday after
    '''
    cal = calendar.Calendar(0)
    try:
        month = int(month)
    except:
        month = list(calendar.month_abbr).index(firstcap(month))
    if day:
        monthcal = cal.monthdatescalendar(year, month)
        (which, dow) = day.split()
        which = which.lower()
        map_if = {'first': 0,
                  'second': 1,
                  'third': 2,
                  'fourth': 3,
                  'last': -1}
        map_if_not = {'first': 1,
                      'second': 2,
                      'third': 3,
                      'fourth': 4,
                      'last': -2}
        dow_is_in_this_month = checkweek(monthcal[map_if[which]], dow, month)
        if dow_is_in_this_month:
            week = monthcal[map_if[which]]
        else:
            week = monthcal[map_if_not[which]]
        theday = week[list(calendar.day_name).index(firstcap(dow))]
    elif dom:
        dow = calendar.weekday(year, month, dom)
        if dow > 4:
            if beforeorafter == 'default':
                if dow == 5:
                    theday = date(year, month, dom - 1)
                elif dow == 6:
                    theday = date(year, month, dom + 1)
                else:
                    return 'wrongdayofweekfound'
            elif beforeorafter == 'before':
                if dow == 5:
                    theday = date(year, month, dom - 1)
                elif dow == 6:
                    theday = date(year, month, dom - 2)
            elif beforeorafter == 'after':
                if dow == 5:
                    theday = date(year, month, dom + 2)
                elif dow == 6:
                    theday = date(year, month, dom + 1)
        else:
            theday = date(year, month, dom)
    else:
        return 'nodayordomgiven'
    return '%s-%02d-%02d' % (theday.year, theday.month, theday.day)


def all_holiday_list(y=currentyear):
    NewYearsDay = holidayis(month=1, dom=1, year=y, beforeorafter='after')
    ChristmasEve = holidayis(month=12, dom=24, year=y, beforeorafter='before')
    ChristmasDay = holidayis(month=12, dom=25, year=y, beforeorafter='after')
    NewYearsEve = holidayis(month=12, dom=31, year=y, beforeorafter='before')
    return NewYearsDay, ChristmasEve, ChristmasDay, NewYearsEve


def us_holiday_list(y=currentyear):
    MLKDay = holidayis(month=1, day='third Monday', year=y)
    PresidentsDay = holidayis(month=2, day='third Monday', year=y)
    MemorialDay = holidayis(month=5, day='last Monday', year=y)
    IndependenceDay = holidayis(month=7, dom=4, year=y)
    LaborDay = holidayis(month=9, day='first Monday', year=y)
    ThanksgivingDay = holidayis(month=11, day='fourth Thursday', year=y)
    DayAfterThanksgiving = holidayis(month=11, day='fourth Friday', year=y)

    dates = all_holiday_list(y=y)
    dates += (MLKDay, PresidentsDay, MemorialDay, IndependenceDay, LaborDay,
              ThanksgivingDay, DayAfterThanksgiving)
    return list(dates)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, default=date.today().year,
                        help='specify year')
    parser.add_argument('--month', default=False,
                        help='specify month (eg: April or 4)')
    parser.add_argument('--dom', type=int, default=False,
                        help='specify integer day of month (eg: 4)')
    parser.add_argument('--day', type=str, default=False,
                        help='describe day (eg: first Monday)')
    parser.add_argument('--boa', type=str, default='default',
                        help='before or after behavior')
    args = parser.parse_args()
    if not (args.dom or args.day):
        print 'Observed US Holidays:'
        for x in sorted(us_holiday_list(y=args.year)):
            print '  %s' % x
        print
    else:
        print holidayis(month=args.month, dom=args.dom, day=args.day,
                        year=args.year, beforeorafter=args.boa)
