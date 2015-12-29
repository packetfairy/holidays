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

dayofweek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
             'saturday', 'sunday']
currentyear = date.today().year


def checkweek(week, dow, month):
    '''take given 'week' of a month of datetime.date() objects as gathered by:
         calendar.Calendar.monthdatescalendar(year, month)[N]
       and 'day of week' as requested, evaluate whether or not the given day of
       the day falls within a week within the given month, and return True or
       False based on that evaluation.'''
    check = week[dayofweek.index(dow.lower())].month
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
    if day:
        monthcal = cal.monthdatescalendar(year, month)
        (which, dow) = day.split()
        which = which.lower()
        first_dow_is_in_this_month = checkweek(monthcal[0], dow, month)
        if which == 'first':
            if first_dow_is_in_this_month:
                week = monthcal[0]
            else:
                week = monthcal[1]
        elif which == 'second':
            if first_dow_is_in_this_month:
                week = monthcal[1]
            else:
                week = monthcal[2]
        elif which == 'third':
            if first_dow_is_in_this_month:
                week = monthcal[2]
            else:
                week = monthcal[3]
        elif which == 'fourth':
            if first_dow_is_in_this_month:
                week = monthcal[3]
            else:
                week = monthcal[4]
        elif which == 'last':
            if checkweek(monthcal[-1], dow, month):
                week = monthcal[-1]
            else:
                week = monthcal[-2]
        theday = week[dayofweek.index(dow.lower())]
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
                theday = date(year, month, dom - 1)
            elif beforeorafter == 'after':
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
    parser.add_argument('--month', type=int, default=False,
                        help='specify integer month (eg: April = 4)')
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
