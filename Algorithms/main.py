def candidata(m):
    j = m
    c = A[m]
    count = 1
    while j < n-1 and count > 0:
        j = j + 1
        if c == A[j]:
            count += 1
        else:
            count -= 1
    if j == n-1 :
        return c
    else:
        return candidata(j+1)

if __name__ == '__main__':
    number = input("请输入列表中的每个元素：")
    A = [int(n) for n in number.split()]
    n = len(A)
    print('A[%d] ='%n,A)
    c = candidata(0)
    count = 0
    for j in range(n):
        if A[j] == c:
            count += 1
    if count > int(n/2):
        print('列表中的多数元素是：%d' %c)
    else:
        print('该列表不存在多数元素')
