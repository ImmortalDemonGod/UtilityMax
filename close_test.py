def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


lst = [2.4, 3.2, 6.9, 5.0, 5.2, 7.2, 9.8]

K = 5.1
print(closest(lst, K))

