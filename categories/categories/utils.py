import traceback


def safe_func(func):

    def wrapped_func(*arg, **kwargs):
        try:
            return func(*arg, **kwargs)
        except Exception as e:
            print('- ' * 50)
            print('- ' * 50)
            print('- ' * 50)
            traceback.print_exc()
            print('- ' * 50)
            print('- ' * 50)
            print('- ' * 50)

    return wrapped_func
