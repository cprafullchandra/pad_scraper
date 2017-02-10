def ErrorHandler(function):
    """ Decorator that wraps function in a try/catch and prints error """
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print(sys.exc_info())
            print(e)
    return wrapper
