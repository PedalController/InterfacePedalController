class integer(object):
    """
    Convert the informed args to integer
    """
    def __init__(self, *args):
        self.args = args

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            for arg in self.args:
                kwargs[arg] = int(kwargs[arg])
            f(*args, **kwargs)

        return wrapped
