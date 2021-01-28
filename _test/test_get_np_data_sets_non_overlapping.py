
import datetime

from keras_coach.data_handling import get_np_data_sets, get_data_set_spec_for_spy_and_efs


def main():
    date_end = datetime.date(2020, 12, 22)
    time_range = datetime.timedelta(days=200)
    data_set_spec = get_data_set_spec_for_spy_and_efs()
    xx = get_np_data_sets(data_set_spec, date_end=date_end, time_range=time_range)


main()
