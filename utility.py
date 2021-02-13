from functools import reduce
from collections import OrderedDict
from pytz import timezone
import datetime
import jpholiday


class TimeTable:
    def __init__(self, _distination, _diagram):
        self.distination = _distination
        self.diagram = _diagram
        self.feture_schedule = self.calc_feture_schedule()

    def calc_feture_schedule(self) -> tuple:
        times = [time for time in self.diagram.keys()]
        dict_key = self.make_dict_key()
        idx = reduce(lambda a, x: a+1 if x < dict_key else a, times, 0)
        ret = [self.diagram[k] for k in times[idx:idx+3]]
        while len(ret) < 3:
            ret.append("運行終了")
        return tuple(ret)

    def make_dict_key() -> str:
        jst_now = datetime.datetime.now(timezone('Asia/Tokyo'))
        return jst_now.hour * 60 + jst_now.minute


class TimeTableUtility:
    @classmethod
    def selectTimeTable(cls, mode: str) -> TimeTable:
        if mode == "TakatsukiToKansai":
            from timetable import TAKATSUKI_TO_KANSAI as diagram
            distination = "JR高槻駅 -> 関西大学"
        elif mode == "TondaToKansai":
            from timetable import TONDA_TO_KANSAI as diagram
            distination = "JR富田駅 -> 関西大学"
        elif mode == "KansaiToTakatsuki":
            from timetable import KANSAI_TO_TAKATSUKI as diagram
            distination = "関西大学 -> JR高槻駅"
        elif mode == "KansaiToTonda":
            from timetable import KANSAI_TO_TONDA as diagram
            distination = "関西大学 -> JR富田駅"
        else:
            pass

        jst_now = datetime.datetime.now(timezone('Asia/Tokyo'))
        is_holiday = jpholiday.is_holiday(jst_now)
        if is_holiday or jst_now.weekday() == 6:
            return TimeTable(distination, diagram.sunday)
        elif jst_now.weekday() < 5:
            return TimeTable(distination, diagram.weekday)
        elif jst_now.weekday() == 5:
            return TimeTable(distination, diagram.saturday)
        else:
            pass

    @classmethod
    def make_response_text(cls, mode: str) -> str:
        return cls.make_text(cls.selectTimeTable(mode))

    @classmethod
    def make_text(cls, timeTable: TimeTable) -> str:
        text = "次のバスの時刻は\n" \
            + "[1]:" + timeTable.feture_schedule[0] + "\n" \
            + "[2]:" + timeTable.feture_schedule[1] + "\n" \
            + "[3]:" + timeTable.feture_schedule[2] + "\n"
        return text
