from functools import reduce
from pytz import timezone
import datetime
import jpholiday


def make_response_text(mode):
    timeTable = selectTimeTable(mode)
    dict_key = make_dict_key()
    return calc_feture_bus_times(timeTable, dict_key)


def calc_feture_bus_times(timetable: dict, now: int) -> tuple:
    times = [time for time in timetable.keys()]
    idx = reduce(lambda a, x: a+1 if x < now else a, times, 0)
    ret = [timetable[k] for k in times[idx:idx+3]]
    while len(ret) < 3:
        ret.append("運行終了")
    return tuple(ret)


def selectTimeTable(mode):
    if mode == "TakatsukiToKansai":
        from .timetable import TAKATSUKI_TO_KANSAI as diagram
    elif mode == "TondaToKansai":
        from .timetable import TONDA_TO_KANSAI as diagram
    elif mode == "KansaiToTakatsuki":
        from .timetable import KANSAI_TO_TAKATSUKI as diagram
    elif mode == "KansaiToTonda":
        from .timetable import KANSAI_TO_TONDA as diagram
    else:
        pass

    jst_now = datetime.datetime.now(timezone('Asia/Tokyo'))
    is_holiday = jpholiday.is_holiday(jst_now)
    if is_holiday:
        return diagram.sunday
    elif jst_now.weekday() < 5:
        return diagram.weekday
    elif jst_now.weekday() == 5:
        return diagram.saturday
    elif jst_now.weekday() == 6:
        return diagram.sunday
    else:
        pass


def make_dict_key():
    jst_now = datetime.datetime.now(timezone('Asia/Tokyo'))
    return jst_now.hour * 60 + jst_now.minute


if __name__ == '__main__':
    make_response_text("TakatsukiToKansai")
    # print(calc_feture_bus_times.fill_gte_3.map(lambda x: x.toDisp())