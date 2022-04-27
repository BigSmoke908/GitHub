def f(n):
    if n >= 0:
        if n > 0:
            return n * f(n - 1)
        return 1
    return 0


print(f(997))
