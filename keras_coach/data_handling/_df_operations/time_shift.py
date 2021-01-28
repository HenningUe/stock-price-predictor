
import datetime as dt
from ._helper import time_add, time_minus


def shift_symbols_data_time_to_make_days_congruent(symbols_data):
    for symb in symbols_data:
        rtn_dict = _shift_symbols_data_time_for_single_symbol(symb['spec'], symb['df'],
                                                              algebraic_sign_direction=1)
        symb['spec'] = rtn_dict['spec']
        symb['df'] = rtn_dict['df']
    return symbols_data


def shift_back_symbol_df_batches_time_to_its_original(symbol_data, df_batches):
    for i, df_batch in enumerate(df_batches):
        df = df_batch['df']
        rtn_dict = _shift_symbols_data_time_for_single_symbol(symbol_data['spec'], df,
                                                              algebraic_sign_direction=-1)
        symbol_data['spec'] = rtn_dict['spec']
        df_batches[i]['df'] = rtn_dict['df']
    symbol_data['spec'].pop('day_start_time_original')
    symbol_data['spec'].pop('day_end_time_original')
    return df_batches


def _shift_symbols_data_time_for_single_symbol(symbol_spec, df, algebraic_sign_direction=1):
    assert(algebraic_sign_direction in [1, -1])
    day_start_time = symbol_spec['day_start_time']
    day_end_time = symbol_spec['day_end_time']
    if algebraic_sign_direction == 1:
        symbol_spec['day_start_time_original'] = day_start_time
        symbol_spec['day_end_time_original'] = day_end_time
    day_start_time_orig = symbol_spec['day_start_time_original']
    day_end_time_orig = symbol_spec['day_end_time_original']

    if day_end_time_orig > day_start_time_orig:
        return dict(spec=symbol_spec, df=df)
    else:
        assert('timeshift_adapt_direction' in symbol_spec)
        assert(symbol_spec['timeshift_adapt_direction'] in ['+', '-'])
    if symbol_spec['timeshift_adapt_direction'] == '+':
        day_start_time_for_calc = time_add(day_start_time_orig, -dt.timedelta(minutes=1))
        delta = time_minus(dt.time(23, 59), day_start_time_for_calc)
    else:
        delta = time_minus(dt.time(0, 0), day_end_time_orig)
    delta = delta * algebraic_sign_direction
    df_ = df
    df.index = df_.index + delta
    symbol_spec['day_start_time'] = time_add(day_start_time, delta)
    symbol_spec['day_end_time'] = time_add(day_end_time, delta)
    if algebraic_sign_direction == 1:
        assert(symbol_spec['day_end_time'] > symbol_spec['day_start_time'])
    return dict(spec=symbol_spec, df=df)
