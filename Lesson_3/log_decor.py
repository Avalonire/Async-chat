class Log:
    def __init__(self) -> None:
        pass

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f'Вызов {func.__name__} {args} {kwargs}')
            r = func(*args, **kwargs)
            print(f'{func.__name__} вернула {r}')
            return r

        return wrapper
    