def signature(*args, **kwargs):
    def decorator(fn):
        def wrapped(*fn_args, **fn_kwargs):
            new_args = [t(raw) for t, raw in zip(args, fn_args)]
            new_kwargs = dict([(k, kwargs[k](v)) for k, v in fn_kwargs.items()])

            fn(*new_args, **new_kwargs)

        return wrapped

    return decorator