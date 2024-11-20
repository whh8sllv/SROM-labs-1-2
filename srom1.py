import random
import time
import pandas as pd


def converter32(num, b):
    res = []
    while num >= 0:
        r = num % b
        num //= b
        res.append(r)
        if num == 0:
            break
    return res

def make_eq(num1, num2):
    if len(num1) == len(num2):
        return num1, num2
    elif len(num2) > len(num1):
        dif = len(num2) - len(num1)
        for i in range(dif):
            num1.append(0)
    else:
        dif = len(num1) - len(num2)
        for i in range(dif):
            num2.append(0)
    return num1, num2

def longCmp(num1, num2):
    num1, num2 = make_eq(num1, num2)
    i = len(num1) - 1
    while num1[i] == num2[i]:
        i -= 1
        if i == -1:
            break
    if i == -1:
        return 0
    else:
        if num1[i] > num2[i]:
            return 1
        else:
            return -1

def longAdd(num1, num2):
    carry = 0
    res = [0] * (len(num1) + 1)
    for i in range(len(num1)):
        temp = num1[i] + num2[i] + carry
        res[i] = temp & (2**32 - 1)
        carry = temp >> 32
    return res

def longSub(num1, num2):
    borrow = 0
    res = [0] * len(num1)
    for i in range(len(num1)):
        temp = num1[i] - num2[i] - borrow
        if temp >= 0:
            res[i] = temp
            borrow = 0
        else:
            res[i] = 2**32 + temp
            borrow = 1
    return res

def longMuolOneDigit(num1, const):
    carry = 0
    res = [0] * (len(num1) + 1)
    for i in range(len(num1)):
        temp = num1[i] * const + carry
        res[i] = temp & (2**32 - 1)
        carry = temp >> 32
    res[len(num1)] = carry
    return res

def longShiftDigitsToHigh(num, shift):
    num = num[::-1]
    for j in range(shift):
        num.append(0)
    return num[::-1]

def longMul(num1, num2):
    cmp = longCmp(num1, num2)
    if cmp == -1:
        num1, num2 = num2, num1
    res = []
    for i in range(len(num1)):
        temp = longMuolOneDigit(num1, num2[i])
        temp2 = longShiftDigitsToHigh(temp, i)
        res, temp = make_eq(res, temp2)
        res = longAdd(res, temp2)
    return res

def bitLength(num):
    lastBits = num[-1].bit_length()
    return (len(num)-1) * 32 + lastBits

def longShiftBitsToHigh(num, shift):
    if num == [] or shift < 0:
        return [0]
    bits = 32
    limit = 2**32 - 1
    numShift = shift // bits
    bitShift = shift % bits
    if bitShift > 0:
        new_length = len(num) + numShift + 1
    else:
        new_length = len(num) + numShift
    res = [0] * new_length

    if bitShift > 0:
        carry = 0
        for i in range(len(num)):
            a = num[i]
            aShifted = ((a << bitShift) | carry) & limit
            carry = (a << bitShift) >> bits
            res[i+numShift] = aShifted
        if carry > 0:
            res[len(num)+numShift] = carry
    else:
        for i in range(len(num)):
            res[i+numShift] = num[i]
    
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res

def longDivMod(num1, num2):
    num2 = [int(i) for i in num2 if i != 0]
    if num2 == []:
        return 'Error', 'Error'
    k = bitLength(num2)
    R = num1
    Q = [0] * len(num1)
    p = bitLength(R)
    counter = 0
    while longCmp(R, num2) >= 0:
        R = [int(i) for i in R if i > 0]
        t = bitLength(R)
        afterShift = longShiftBitsToHigh(num2, t-k)
        if longCmp(R, afterShift) == -1:
            t -= 1
            afterShift = longShiftBitsToHigh(num2, t-k)
        R, afterShift = make_eq(R, afterShift)
        R = longSub(R, afterShift)
        sup = [2**(t-k)]
        Q, sup = make_eq(Q, sup)
        Q = longAdd(Q, sup)
    return Q, R

def longPowerWindow(num1, num2):
    t = 4
    res = [1]
    count = 2**t -1
    D = []
    for i in range(count+1):
        D.append([])
    D[0] = [1]
    sec = [i for i in num1 if i != 0]
    D[1] = sec
    for i in range(2, 2**t):
        sup = D[i-1]
        supR, num1R = make_eq(sup, num1)
        fin = longMul(supR, num1R)
        while fin[-1] == 0 and len(fin) != 1:
            fin.pop()
        D[i] = fin

    for i in range(len(num2)-1, -1, -1):
        var = D[num2[i]]
        res, var = make_eq(res, var)
        res = longMul(res, var)
        if i != 0:
            for j in range(1, t+1):
                res = longMul(res, res)
    return res

def converter16(res):
    base = 2**32
    final = 0
    for i in range(len(res)):
        final += res[i] * (base)**i
    return hex(final)

print()
print('*************************************** Main ***************************************')
print()


a1 = 0x8a6e3f27c0b38751c37770f0cda92acd43297af9dddd3647cc436d5c6b2ca06e6184965c46cb771cc0d41f71ad234396d716f3412f7d3ec8e04b5408517af5961c03b02568d63e5a68fc1c0293aee23a22f60639d0c594f2b1dfeba6d461fd81c9857ccf0ef9f6c2425c4f9294955ee26d1f8a5a415e3f68e00d05199fee30c01b9ef52bc295d88021ec04e3eb39fa3ee446a3214b52e1f97a2b63098b56e9c5dd13c76878567142fc40c8f69829813483b754b4b7c88ad697e5752d2f179b3b60
b1 = 0x1708e3e3b1bbbea6a1252c905144a13d5159c6f5c78e2e7472c750588d1cc14fbb79b08d3b187c9cfec6cd9853e4283ed48784e8f0595818f193ffd31aa35616869e2dd92ed8672b30af58986a870d41644c8d952332c22ac8a8fb7b23579a53b8e199d5116e4663fae8950da5b4afdd9fbcb959891b46d3336e280ff914b7196fc8b9f7ed3364a88c085944e05f61f86f996cb5b12c6d3e22d0a12791d8ac30a24729b92f9190a0b7b11ce4c1a555bdbfb86ccd16a5f47f7c5170

base = 2**32

a2 = converter32(a1, base)
b2 = converter32(b1, base)


a3, b3 = make_eq(a2, b2)


print(f'A = {hex(a1)[2:]}')
print(f'B = {hex(b1)[2:]}')
print()

resAdd = longAdd(a3, b3)
print(f'A + B = {str(converter16(resAdd))[2:]}')

print()

cmp = longCmp(a3, b3)
if cmp == -1:
    resSub = longSub(b3, a3)
    print(f'A - b  = -{(converter16(resSub))[2:]}')
else:
    resSub = longSub(a3, b3)
    print(f'A - B  = {(converter16(resSub))[2:]}')

print()

resMul = longMul(a3, b3)
print(f'A * B = {converter16(resMul)[2:]}')

print()

resSquare = longMul(a2, a2)
print(f'A ^ 2 = {converter16(resSquare)[2:]}')


print()
resQ, resR = longDivMod(a2, b2)
if resQ == 'Error' and resR == 'Error':
    print('Error, ZeroDivision!')
else:
    print(f'A / B = {converter16(resQ)[2:]}')
    print()
    print(f'A mod B = {converter16(resR)[2:]}')
print()

#b2 = converter32(b1, 2**4)
#resPower = longPowerWindow(a2, b2)
#print(f'A ^ B = {converter16(resPower)[2:]}')

print()


print('*************************************** Testing ***************************************')
print()

print('test1: (a+b)*c = c*(a+b) = a*c + b*c')
def test1(a, b, c):
    base = 2**32
    a1 = converter32(a, base)
    b1 = converter32(b, base)
    c1 = converter32(c, base)
    a1, b1 = make_eq(a1, b1)
    resAdd = longAdd(a1, b1)
    resAdd, c1 = make_eq(resAdd, c1)
    resMul1 = converter16(longMul(resAdd, c1))[2:]
    resMul2 = converter16(longMul(c1, resAdd))[2:]
    a2, c2 = make_eq(a1, c1)
    resMulfirst = longMul(a2, c2)
    b2, c3 = make_eq(b1, c1)
    resMulSecond = longMul(b2, c3)
    resMulfirst, resMulSecond = make_eq(resMulfirst, resMulSecond)
    resAdd3 = converter16(longAdd(resMulfirst, resMulSecond))[2:]
    if resMul1 == resMul2 and resMul1 == resAdd3:
        print('(a+b)*c = c*(a+b) = a*c + b*c - True')

aTest1 = 0x20d4b9704135d0
bTest1 = 0xa577b7292
cTest1 = 0x0
test1(aTest1, bTest1, cTest1)


print()
print('test2: n*a = a + a + a + ... + a (n >= 100)')
def test2(n, a):
    base = 2**32
    n1 = converter32(n, base)
    a1 = converter32(a, base)
    n1, a1 = make_eq(n1, a1)
    resMul = converter16(longMul(n1, a1))[2:]
    res = longAdd(a1, a1)
    for i in range(n-0x2):
        a1, res = make_eq(a1, res)
        res = longAdd(a1, res)
    res = converter16(res)[2:]
    if resMul == res:
        print('n * a == a + a + ... + a (n >= 100) - True')

nTest2 = 0x381
aTest2 = 0x80f2267304d
test2(nTest2, aTest2)


print()
print('test3: 0 in operations LongAdd, LongSub, LongMul, LongDivMod, LongPowerWindow')
def test3(const, a):
    a1 = converter32(a, 2**32)
    const1 = converter32(const, 2**4)
    const = converter32(const, 2**32)
    a1, const = make_eq(a1, const)
    resAddZero = longAdd(a1, const)
    resSubZero = longSub(a1, const)
    resMulZero = longMul(a1, const)
    resQZero, resRZero = longDivMod(a1, const)
    resPowerZero = longPowerWindow(a1, const1)
    if converter16(resAddZero) == hex(a):
        print('ZeroAdd - True')
    if converter16(resSubZero) == hex(a):
        print('ZeroSub - True')
    if converter16(resMulZero) == hex(0):
        print('ZeroMul - True')
    if resQZero == 'Error' and resRZero == 'Error':
        print('ZeroDivMod - True')
    if converter16(resPowerZero) == hex(1):
        print('ZeroPower - True')

constTest3 = 0x0
aTest3 = 0x80f2267304d
test3(constTest3, aTest3)


print()
print('test4: 1 in operations LongMul, LongDivMod, LongPowerWindow')
def test4(const, a):
    a1 = converter32(a, 2**32)
    const1 = converter32(const, 2**4)
    const = converter32(const, 2**32)
    a1, const = make_eq(a1, const)
    resMulOne = longMul(a1, const)
    resQOne, resROne = longDivMod(a1, const)
    resPowerOne = longPowerWindow(a1, const1)
    if converter16(resMulOne) == hex(a):
        print('OneMul - True')
    if converter16(resQOne) == hex(a) and converter16(resROne) == hex(0):
        print('OneDiv - True')
    if converter16(resPowerOne) == hex(a):
        print('OnePower - True')

constTest4 = 0x1
aTest4 = 0x80f2267304d
test4(constTest4, aTest4)

print()

print('test5: commutativity of LongAdd and LongMul')
def test5(a, b):
    a1 = converter32(a, 2**32)
    b1 = converter32(b, 2**32)
    a1, b1 = make_eq(a1, b1)
    resAdd1 = longAdd(a1, b1)
    resAdd2 = longAdd(b1, a1)
    if converter16(resAdd1) == converter16(resAdd2):
        print('a + b = b + a - True')
    resMul1 = longMul(a1, b1)
    resMul2 = longMul(b1, a1)
    if converter16(resMul1) == converter16(resMul2):
        print('a * b = b * a - True')

aTest5 = 0x381
bTest5 = 0x80f2267304d
test5(aTest5, bTest5)

print()

print('test6: a^n = a * a * ... * a (n >= 100)')
def test6(n, a):
    base = 2**32
    a1 = converter32(a, base)
    n1 = converter32(n, 2**4)
    resPower = longPowerWindow(a1, n1)
    resMul1 = longMul(a1, a1)
    for i in range(n-0x2):
        a1, resMul1 = make_eq(a1, resMul1)
        resMul1 = longMul(a1, resMul1)
        while resMul1 and resMul1[-1] == 0:
            resMul1.pop()
    if converter16(resPower) == converter16(resMul1):
        print('a^n = a * a * ... * a (n >= 100) - True')

nTest6 = 0x64
aTest6 = 0x4c8
test6(nTest6, aTest6)

print()
print('*************************************** Time Testing ***************************************')
print()

def AverageTimeLongTest(n, operation):
    average_time = []
    max_len = 309
    for _ in range(n):
        a = ''
        b = ''
        len_a = random.randint(1, max_len+1)
        for i in range(len_a):
            a += str(random.randint(0, 10))
    
        len_b = random.randint(1, max_len+1)
        for j in range(len_b):
            b += str(random.randint(0, 10))
    
        a1 = converter32(int(a), 2**32)
        b1 = converter32(int(b), 2**32)
        a2, b2 = make_eq(a1, b1)
        if operation == 'longAdd':
            start = time.time()    
            res = longAdd(a2, b2)
            end = time.time()
            final_time = end - start
            average_time.append(final_time)
        elif operation == 'longSub':
            start = time.time()
            res = longSub(a2, b2)
            end = time.time()
            final_time = end - start
            average_time.append(final_time)
        elif operation == 'longMul':
            start = time.time()
            res = longMul(a2, b2)
            end = time.time()
            final_time = end - start
            average_time.append(final_time)
        elif operation == 'longDivMod':
            start = time.time()    
            res = longDivMod(a1, b1)
            end = time.time()
            final_time = end - start
            average_time.append(final_time)
    return (sum(average_time))/len(average_time)

print('LongAdd')
longAddTime100 = AverageTimeLongTest(100, 'longAdd')
print(f'Середній час виконання операції багаторозрядного додавання (100 ітерацій) = {f"{longAddTime100:.20f}"} секунд')
longAddTime1000 = AverageTimeLongTest(1000, 'longAdd')
print(f'Середній час виконання операції багаторозрядного додавання (1000 ітерацій) = {f"{longAddTime1000:.20f}"} секунд')
longAddTime10000 = AverageTimeLongTest(10000, 'longAdd')
print(f'Середній час виконання операції багаторозрядного додавання (10000 ітерацій) = {f"{longAddTime10000:.20f}"} секунд')

print()
print('LongSub')
longSubTime100 = AverageTimeLongTest(100, 'longSub')
print(f'Середній час виконання операції багаторозрядного віднімання (100 ітерацій) = {f"{longSubTime100:.20f}"} секунд')
longSubTime1000 = AverageTimeLongTest(1000, 'longSub')
print(f'Середній час виконання операції багаторозрядного віднімання (1000 ітерацій) = {f"{longSubTime1000:.20f}"} секунд')
longSubTime10000 = AverageTimeLongTest(10000, 'longSub')    
print(f'Середній час виконання операції багаторозрядного віднімання (10000 ітерацій) = {f"{longSubTime10000:.20f}"} секунд')

print()
print('LongMul')
longMulTime100 = AverageTimeLongTest(100, 'longMul')
print(f'Середній час виконання операції багаторозрядного множення (100 ітерацій) = {f"{longMulTime100:.20f}"} секунд')
longMulTime1000 = AverageTimeLongTest(1000, 'longMul')
print(f'Середній час виконання операції багаторозрядного множення (1000 ітерацій) = {f"{longMulTime1000:.20f}"} секунд')
longMulTime10000 = AverageTimeLongTest(10000, 'longMul')    
print(f'Середній час виконання операції багаторозрядного множення (10000 ітерацій) = {f"{longMulTime10000:.20f}"} секунд')

print()
print('LongDivMod')
longDivModTime100 = AverageTimeLongTest(100, 'longDivMod')
print(f'Середній час виконання операції багаторозрядного ділення та знаходження остачі від ділення (100 ітерацій) = {f"{longDivModTime100:.20f}"} секунд')
longDivModTime1000 = AverageTimeLongTest(1000, 'longDivMod')
print(f'Середній час виконання операції багаторозрядного ділення та знаходження остачі від ділення (1000 ітерацій) = {f"{longDivModTime1000:.20f}"} секунд')
longDivModTime10000 = AverageTimeLongTest(10000, 'longDivMod')    
print(f'Середній час виконання операції багаторозрядного ділення та знаходження остачі від ділення (10000 ітерацій) = {f"{longDivModTime10000:.20f}"} секунд')

print()
print('Усереднені часові заміри операцій над багаторозрядними випадковими числами до 1024 біт (у секундах)')
print()

timeResultsAll = {'100 ітерацій': [f"{longAddTime100:.20f}", f"{longSubTime100:.20f}", f"{longMulTime100:.20f}", f"{longDivModTime100:.20f}"],
                  '1000 ітерацій': [f"{longAddTime1000:.20f}", f"{longSubTime1000:.20f}", f"{longMulTime1000:.20f}", f"{longDivModTime1000:.20f}"],
                  '10000 ітерацій' : [f"{longAddTime10000:.20f}", f"{longSubTime10000:.20f}", f"{longMulTime10000:.20f}", f"{longDivModTime10000:.20f}"]}

df = pd.DataFrame(timeResultsAll, index=["longAdd", "longSub", "longMul", "longDivMod"])

print(df)