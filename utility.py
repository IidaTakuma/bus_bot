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

    def make_dict_key(self) -> str:
        jst_now = datetime.datetime.now(timezone('Asia/Tokyo'))
        return jst_now.hour * 60 + jst_now.minute


class TimeTableUtility:

    def __init__(self, _mode: str):
        self.mode = _mode
        self.timeTable = self.set_timeTable()

    def set_timeTable(self) -> TimeTable:
        if self.mode == "TakatsukiToKansai":
            from timetable import TAKATSUKI_TO_KANSAI as diagram
            distination = "JR高槻駅->関西大学"
        elif self.mode == "TondaToKansai":
            from timetable import TONDA_TO_KANSAI as diagram
            distination = "JR富田駅->関西大学"
        elif self.mode == "KansaiToTakatsuki":
            from timetable import KANSAI_TO_TAKATSUKI as diagram
            distination = "関西大学->JR高槻駅"
        elif self.mode == "KansaiToTonda":
            from timetable import KANSAI_TO_TONDA as diagram
            distination = "関西大学->JR富田駅"
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

    def make_response_text(self) -> str:
        return self.make_text()

    def make_text(self) -> str:
        text = self.timeTable.distination + "\n" \
            + "現在時刻から次に来るバス\n" \
            + "先発　：" + self.timeTable.feture_schedule[0] + "\n" \
            + "次発　：" + self.timeTable.feture_schedule[1] + "\n" \
            + "次次発：" + self.timeTable.feture_schedule[2] + "\n"
        return text

    def make_all_timeTable_text(self) -> str:
        timeTable_dict = {}
        for key, value in self.timeTable.diagram.items():
            hour_str = value[0:2]
            minute_str = value[3:5]
            timeTable_dict.setdefault(hour_str, []).append(minute_str)

        header = "本日の時刻表\n" + self.timeTable.distination + "\n"
        header += "ーーーーーーーーーーーーーー\n"
        timeTable_text = ""
        for key, value in timeTable_dict.items():
            timeTable_text += key + "｜"
            for i, minute in enumerate(value):
                timeTable_text += minute
                if i + 1 == len(value):
                    timeTable_text += "\n"
                else:
                    timeTable_text += ", "

        footer = "ーーーーーーーーーーーーーー\n"

        return header + timeTable_text + footer


def test():
    timeTable_utility = TimeTableUtility("KansaiToTonda")
    print(timeTable_utility.make_all_timeTable_text())
    return


if __name__ == "__main__":
    test()
