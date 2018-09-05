def print_or_save(value, data_out=None):
    if data_out is None:
        print(value)
    else:
        data_out.write(value + '\n')