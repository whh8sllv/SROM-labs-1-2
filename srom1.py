import random
import secrets
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
    res[len(num1)] = carry
    while res and res[-1] == 0:
        res.pop()
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
    while res and res[-1] == 0:
        res.pop()
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
        temp2 = [0] * i + temp
        res, temp2 = make_eq(res, temp2)
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
    while num2 and num2[-1] == 0:
        num2.pop()
    if num2 == []:
        return 'Error', 'Error'
    k = bitLength(num2)
    R = num1
    Q = [0] * len(num1)
    p = bitLength(R)
    counter = 0
    while longCmp(R, num2) >= 0:
        while R and R[-1] == 0:
            R.pop()
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

def gcd_stein(num1, num2):
    a = num1
    b = num2
    d = [1]
    while (a[0] % 2 == 0 and b[0] % 2 == 0):
        a = divide_by_2_32(a)
        b = divide_by_2_32(b)
        d = longMul(d, [2])
    while a[0] % 2 == 0:
        a = divide_by_2_32(a)    
    while longCmp(b, [0]) != 0:
        while b[0] % 2 == 0:
            b = divide_by_2_32(b)
        if longCmp(a, b) > 0:
            a, b = b, a
        b = longSub(b, a)   
    d = longMul(d, a)
    return d
        
def divide_by_2_32(num):
    res = []
    carry = 0 
    for i in reversed(num):
        new_block = (i >> 1) | (carry << 31)
        carry = i & 1
        res.append(new_block)
    res.reverse()
    while len(res) > 1 and res[0] == 0:
        res.pop(0)
    return res

def lcm(num1, num2):
    gcd = gcd_stein(num1, num2)
    mult = longMul(num1, num2)
    gcd, mult = make_eq(gcd, mult)
    return longDivMod(mult, gcd)[0]

def find_mu(mod):
    k = len(mod)
    beta_2k = [0] * 2*k
    beta_2k.append(1)
    beta_2k, mod = make_eq(beta_2k, mod)
    mu = longDivMod(beta_2k, mod)[0]
    while mu[-1]==0:
        mu.pop()
    return mu

def killLastDigits(num, counter):
    k = len(num)
    if k < counter:
        return [0]
    return num[counter:]

def BarretReduction(num, mod, mu):
    while num and num[-1] == 0:
        num.pop()
    while mod and mod[-1] == 0:
        mod.pop()
    k = len(mod)
    q = killLastDigits(num, k - 1)    
    q = longMul(q, mu)
    while q and q[-1] == 0:
        q.pop()
    q = killLastDigits(q, k + 1)
    sup_product = longMul(q, mod)
    num, sup_product = make_eq(num, sup_product)
    r = longSub(num, sup_product)
    while r and r[-1] == 0:
        r.pop()
    while longCmp(r, mod) >= 0:
        r, mod = make_eq(r, mod)
        r = longSub(r, mod)
        while r and r[-1] == 0:
            r.pop()
    return r

def BarretAdd(num1, num2, mod, mu):
    num1, num2 = make_eq(num1, num2)
    sum = longAdd(num1, num2)
    while sum and sum[-1] == 0:
        sum.pop()
    res = BarretReduction(sum, mod, mu)
    while res and res[-1] == 0:
        res.pop()
    return res

def BarretSub(num1, num2, mod, mu):
    num1, num2 = make_eq(num1, num2)
    if longCmp(num1, num2) >= 0:
        return BarretReduction(longSub(num1, num2), mod, mu)
    else:
        num1, num2 = num2, num1
        sub = longSub(num1, num2)
        a = BarretReduction(sub, mod, mu)
        mod, a = make_eq(mod, a)
        return longSub(mod, a)
    
def BarretProduct(num1, num2, mod, mu):
    num1, num2 = make_eq(num1, num2)
    mul = longMul(num1, num2)
    while mul and mul[-1] == 0:
        mul.pop()
    res = BarretReduction(mul, mod, mu)
    while res and res[-1] == 0:
        res.pop()
    return res

def BarretPower(num1, num2, mod, mu):
    c = [1]
    counter = 0
    if longCmp(num1, mod) > 0:
        num1 = BarretReduction(num1, mod, mu)
    for i in num2:
        if i == 1:
            c = BarretProduct(c, num1, mod, mu)
        num1 = BarretProduct(num1, num1, mod, mu)
        counter += 1
        print(counter)
    return c

def converter16(res):
    base = 2**32
    final = 0
    for i in range(len(res)):
        final += res[i] * (base)**i
    return hex(final)


a = 0xf72f0997fd3fd17931e014ad1d5d4db96a02588d15aaee9cb769e0dcdfdb69bf77e6a98eeab67c11838bea11a81ab45d02b54db21b96a0b0af9c2fd09a9ff4ef3a86bb7d6a17d12af09afc551aa644ba1fa32ea91673aba7d7cdc10a5e8c3c48a77ff30ae93c81ed12b5561cc70715a4639f87bc0725ab487a029b3daef12244f423613cb43806ddfe7c0cc1c6d51d161fb5472a434a3adb633af5816c3c0c241459df8a4656e420f8e23188fe7fc38a82a3928e90699114d62a635957de794a85df4d2a41933f7e01a422a5cce917e50cb35456db7f334e2998287cae20731406dbc33a6d51c5e22d466cbe2b769af76797548b1702556df52a68097e50c42b
b = 0x2522d4428d027178b75b4b1f17f7a2dfb8bd6cae86e9d81b04a9defaa7eecd7809ec882fbe880ceb0cd53866cc1d5424e3a83a828f80d350b13c5a132fb9f4e46bc0087150be3f1aa5d4b3a899fffda944f0f5553ebb7418222b0ca2a6aefdc58cb6d16d04b6deafae0d6e7eaa2bc757667b923ce6f642fa33158391f0d0cd2f473b9dd266e91539b77dd42ffb25a86b9335071b3a4a7adce833a0b7acdcd01b8e58646af45ee8e28dbeb9414b1fd4cfac0819282f13d6a7508f4fc6540a68b2af828143e0856dfc2ab93a0254b4beb5cffc291ca4b540a3cf47dfb6e1830fb1d1529520bafcdfa9a46233187b1c47e765df4a26c69af717e75044b038c537cf
n = 0x7d33390b4beb86348eef5d995506d03aa10718105e142814492ec01eff9facdd197ac451b624a5b7e35712d0caf3567b15944ed95099d3bc1c6b2e0da7c426250b7524cb1c96706250fc39d4a41664bea073695fb89e37d30c42c73e7ade345538c3e7279d33750f9fb1f94e6d53aafa0afa0c4d9c2e21a97e456ea82cc6a83fe6ffa5a5c99156990b9c1d605c105847b0c33d603f6fd8cc2a0deed7ca5eab92e838c10c930d4c2c04f7c8fab88d52c77391ddfdf25b8ac5a3f692331cc47d329b4e0100bf8b3f486f65c03b16af17efcbe53ab6b1eae18eaa185bcfb8f3e91321de981baa83efeaf753bbbc1865eb9dfbd4b67bf30af9c4e024f870e2523ca4


base = 2**32
a1 = converter32(a, base)
b1 = converter32(b, base)
n1 = converter32(n, base)

mu = find_mu(n1)

print()
barPower = BarretPower(a1, converter32(b, 2), n1, mu)
print(f'Module Power = {converter16(barPower)[2:]}')

print()
barAdd = BarretAdd(a1, b1, n1, mu)
print(f'Module Add = {converter16(barAdd)[2:]}')

print()
barSub = BarretSub(a1, b1, n1, mu)
print(f'Module Sub = {converter16(barSub)[2:]}')

print()
barProdcut = BarretProduct(a1, b1, n1, mu)
print(f'Module Product = {converter16(barProdcut)[2:]}')

print()
barSquare = BarretProduct(a1, a1, n1, mu)
print(f'Module Square = {converter16(barSquare)[2:]}')

print()
gcd = gcd_stein(a1, b1)
print(f'gcd(a, b) = {converter16(gcd)[2:]}')

print()
lc = lcm(a1, b1)
print(f'lcm(a, b) = {converter16(lc)[2:]}')



'''TESTING'''
'''def test_control1(a, b, c, n):
    mu = find_mu(n)
    a, b = make_eq(a, b)
    sum1 = longAdd(a, b)
    sum1, c = make_eq(sum1, c)
    product1 = longMul(sum1, c)
    product2 = longMul(c, sum1)
    sup_product1 = longMul(a, c)
    sup_product2 = longMul(b, c)
    sup_product1, sup_product2 = make_eq(sup_product1, sup_product2)
    sum3 = longAdd(sup_product1, sup_product2)
    product1 = BarretReduction(product1, n, mu)
    product2 = BarretReduction(product2, n, mu)
    sum3 = BarretReduction(sum3, n, mu)
    while product1 and product1[-1] == 0:
        product1.pop()
    while product2 and product2[-1] == 0:
        product2.pop()
    while sum3 and sum3[-1] == 0:
        sum3.pop()
    if product1 == product2 and product1 == sum3:
        return '(a + b) * c = c * (a + b) = a * c + b * c (mod n)'
    
a_test1 = 0xe5886ac912eebddce5a6a3da6e26ffddbdecbad9dd4085106e5a9fedf36eb418e3c092c2bfaa539b0f498014d1e0eb914b4d2f35b84b1de70d7e9f2757470c8d40e3a4d5ebad43120fdb2321d7bea7c7c565a444cda06873323294a9779910f17f875ea38d4e72ca254d05200fead870b5c5edbe2dedca6ef6e1c39a1eebfca4a7f9bf4b1652a24a42ddd1f7f7daa7025076f7a1c9dd28b4f5b240b41864e62bbb1813375f581a3cb68c4b28b7300345a62fbeebd3bf81cf6f4ac7950f53ff48957602d464aaa1478ff5cfb651e25b2ee002e9f4d2946245ac84ddf365f1a5fd24d1d44a0be661ce4161659e539e726107bac322ea68ceb1b96fe78d0cc4909a
b_test1 = 0x283dc4dccc9c4438248e125dba49244eaa4d236f2e8d2e7c7f128ec6cbca917b6ffef616f7303474abf745e48821826d268e036eac4ed9cdc58b4a4bec9929711155fa4c6b3cc843c82eb228f2d7c8d34331efafce9e4adf17df0010201625495acde92403dfad466bf5175206db7b04a4c82da678e9d8ad983e5b6a02f02d74f28ab56c7af549a87217a86ccc0a14af141a0ca9ff194a0591739a348c9ea90a2ecda5054b6872d4569e7e167f791f41dd6344246eb6ea327bbaf2ac7bb1f7f5694f3f56fa63b982b1334887a4f4b318af545f982aad919e0057eaa387b22921eaffca4a0dcb1eaab2dbdef21c76508f74b34efaf51069372c9b50dd870c7400
c_test1 = 0xc32085f9f32d60426ad79a6826f1644469ee1e71df338b2c33d24d8e2e197738fde69223838eedac74ba18fe9d21eaef49a020ff21eddcdf1ba1b151e1f6c156e6dd3cbca7b5b78e1900dc1a2e42bf4583562e8eb38552d093fb7e7288fead898cd1789464f248d08bdfb792d49ad1211a3bf71996ceb43dfc19b117115f03f43a4e639b9dee55d676d5f5cc185e9a6e12a4084774987148b7d84ee9d206d8464c44b643be80d6cfefbf4293c99a8960c1c9cdcc463eddbfd3a11b852d97bf0cb2333839ce529872ad3a026dabdc769a22679d015dd9222814fbda64bda127a5fdcee785519b656258290dd3dc61dd76d156260ff579c7ea35bd51758bd9ad48
n_test1 = 0xdc31d364f964bd002ea71e0f1b240d812909369d6b3a4ad743a588d081784af618e2a800f15b2fb461c45b0e718bc9c1d4f4ef3235ee729f2cb79f6bd75f8c834b1f713dcbc2ad28e53b20d2c4b2d74e4942899c0ff8f7518daf2f03d0d5aab91d01b6b7c22fc1dbb0d2bb72f88d83211377e07deaa77b79263f887ec7a46bfdd1c5ac733b84debc4d73c0aaffe9557347f6d17ef837c71bca0773e8e9fef39d70ec9ee82ef6eda3f10fbf0f13b0a7775310df538cf7e619d91e1c02120ea7220ebbc9d603cd011d6dd522a652261cfadec46708ffaa8f6bd82678e52347a0553a709d5ce7af97a25c7e3b3ae8213ebed72ba2d95b0da91a5ad1485fdbe54910

a_t = converter32(a_test1, 2**32)
b_t = converter32(b_test1, 2**32)
c_t = converter32(c_test1, 2**32)
n_t = converter32(n_test1, 2**32)

print()
print('Quality Test')
print()
print(test_control1(a_t, b_t, c_t, n_t))


def test_control2(num1, mod):
    num1 = converter32(num1, 2**32)
    mod = converter32(mod, 2**32)
    mu = find_mu(mod)
    const = converter32(0x64, 2**32)
    res1 = longMul(num1, const)
    res1_mod = BarretReduction(res1, mod, mu)
    res = longAdd(num1, num1)
    for i in range(98):
        num1, res = make_eq(num1, res)
        res = longAdd(num1, res)
    res = BarretReduction(res, mod, mu)
    if converter16(res1_mod) == converter16(res):
        return 'n * a = a + a + ... + a (mod m)  (n=100)'

test1_num1 = 0x9f9287f22b20eec5b35b35cadcca1575ae9b847d691edb18c20c413e8a4573b2c4bdcc5b07404d278b908e0e42b94fe5db97591bcc92048cda32cd443aaddfae792eac319e8327ee956174c02234c8b82418bf2a8934d16665b3c99a4b2ace4fd64a12eb35410f1054ba2a29d53eb3a5d5ab43a4954256c5c5337ec7dd96b6be8547f58ad77931d4a6f42df8f9547d0a77d73f734b7351715fe398a9a5b86df97b85068036d6e68a4e05b2d1babb8c6bda83c7a21f1a8e01c468540c703e2977d03d0cad5f121f83918353d13b4e7fcee9b729e1ad76f5b5b16384621388bb147d6b66c8d2d35e90797ac3198ef99f42f85caddeb845ad1c4cd05be000d592e5
test1_mod = 0x923cdcc1c7a64b2a35059003cb51901b5824b9116208de51aa5adef834253cd2543fb138643905cf76de0e0ed2dd4769812a22d163670a0fa3bb2699bc87f60c7848329b1c420c32de339d8f1efc4d094f68c96159a3d1a2cf33abafeb7dedbef01528da7e8ecba15401fd5c342a97f3182391ca27f4956f4eb13e65a73692186e0125d1c762813692a6badc6eff14356dbe0683c16db1fc3cacc81665709fbda93fec40549dbba26e7c1ff26d5fe79e000d76f1a10f71268443807441d93dfc075f971a3858f8163aae4e8f4115204a346c0315dc39b2921fed927aa39601cb5ed622214479fc039b96d02fd5d45f6ef690003b4f885000cd1a0f644c379586
print(test_control2(test1_num1, test1_mod))

print()'''



'''TIME TESTING'''
'''print('Time Test')
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
        mod = converter32(int((secrets.randbits(2048))), 2**32)
        mu = find_mu(mod)
        a2, b2 = make_eq(a1, b1)
        if operation == 'longAddMod':
            start = time.time()    
            res = BarretAdd(a2, b2, mod, mu)
            end = time.time()
            final_time = end - start
            average_time.append(final_time)
        elif operation == 'longSubMod':
            start = time.time()
            res = BarretSub(a2, b2, mod, mu)
            end = time.time()
            final_time = end - start
            average_time.append(final_time)
        elif operation == 'longMulMod':
            start = time.time()
            res = BarretProduct(a2, b2, mod, mu)
            end = time.time()
            final_time = end - start
            average_time.append(final_time)
        elif operation == 'gcd':
            start = time.time()
            res = gcd_stein(a2, b2)
            end = time.time()
            final_time = end - start
            average_time.append(final_time)
        elif operation == 'lcm':
            start = time.time()
            res = lcm(a2, b2)
            end = time.time()
            final_time = end - start
            average_time.append(final_time)
        return (sum(average_time))/len(average_time)
    
    

#print('LongAddMod')
longAddTime100 = AverageTimeLongTest(100, 'longAddMod')
#print(f'Середній час виконання операції багаторозрядного додавання за модулем(100 ітерацій) = {f"{longAddTime100:.20f}"} секунд')
longAddTime1000 = AverageTimeLongTest(1000, 'longAddMod')
#print(f'Середній час виконання операції багаторозрядного додавання за модулем (1000 ітерацій) = {f"{longAddTime1000:.20f}"} секунд')
longAddTime10000 = AverageTimeLongTest(10000, 'longAddMod')
#print(f'Середній час виконання операції багаторозрядного додавання за модулем (10000 ітерацій) = {f"{longAddTime10000:.20f}"} секунд')

print()
#print('longSubMod')
longSubTime100 = AverageTimeLongTest(100, 'longSubMod')
#print(f'Середній час виконання операції багаторозрядного віднімання за модулем (100 ітерацій) = {f"{longSubTime100:.20f}"} секунд')
longSubTime1000 = AverageTimeLongTest(1000, 'longSubMod')
#print(f'Середній час виконання операції багаторозрядного віднімання за модулем (1000 ітерацій) = {f"{longSubTime1000:.20f}"} секунд')
longSubTime10000 = AverageTimeLongTest(10000, 'longSubMod')    
#print(f'Середній час виконання операції багаторозрядного віднімання за модулем (10000 ітерацій) = {f"{longSubTime10000:.20f}"} секунд')

print()
#print('longMulMod')
longMulTime100 = AverageTimeLongTest(100, 'longMulMod')
#print(f'Середній час виконання операції багаторозрядного множення за модулем (100 ітерацій) = {f"{longMulTime100:.20f}"} секунд')
longMulTime1000 = AverageTimeLongTest(1000, 'longMulMod')
#print(f'Середній час виконання операції багаторозрядного множення за модулем (1000 ітерацій) = {f"{longMulTime1000:.20f}"} секунд')
longMulTime10000 = AverageTimeLongTest(10000, 'longMulMod')
#print(f'Середній час виконання операції багаторозрядного множення за модулем (10000 ітерацій) = {f"{longMulTime10000:.20f}"} секунд')

gcdTime100 = AverageTimeLongTest(100, 'gcd')
gcdTime1000 = AverageTimeLongTest(1000, 'gcd')
gcdTime10000 = AverageTimeLongTest(10000, 'gcd')

lcmTime100 = AverageTimeLongTest(100, 'lcm')
lcmTime1000 = AverageTimeLongTest(1000, 'lcm')
lcmTime10000 = AverageTimeLongTest(10000, 'lcm')

def module(a, b, mod):
    while mod <= a or mod <= b:
        mod = int(hex(secrets.randbits(2048)), 16)
    return mod


def timeTestPower(n):
    avg = []
    for i in range(n):
        hex_number1 = int(hex(secrets.randbits(2048)), 16)
        hex_number2 = int(hex(secrets.randbits(2048)), 16)
        mod = int(hex(secrets.randbits(2048)), 16)
        a1 = converter32(hex_number1, 2**32)
        b1 = converter32(hex_number2, 2)
        mod = converter32(mod, 2**32)
        mu = find_mu(mod)
        start = time.time()
        barPow = BarretPower(a1, b1, mod, mu)
        end = time.time()
        dif = end - start
        avg.append(dif)
    return (sum(avg))/len(avg)



t = timeTestPower(1)
tt = timeTestPower(5)
ttt = timeTestPower(10)




timeResultsPower = {'1 ітерація': [f"{t:.20f}"],
                  '5 ітерацій': [f"{tt:.20f}"],
                  '10 ітерацій': [f"{ttt:.20f}"]}

df2 = pd.DataFrame(timeResultsPower, index=['longPower'])
print(df2)


print()

timeResultsAll = {'100 ітерацій': [f"{longAddTime100:.20f}", f"{longSubTime100:.20f}", f"{longMulTime100:.20f}", f'{gcdTime100:.20f}', f'{lcmTime100:.20f}'],
                  '1000 ітерацій': [f"{longAddTime1000:.20f}", f"{longSubTime1000:.20f}", f"{longMulTime1000:.20f}", f'{gcdTime1000:.20f}', f'{lcmTime1000:.20f}'],
                  '10000 ітерацій' : [f"{longAddTime10000:.20f}", f"{longSubTime10000:.20f}", f"{longMulTime10000:.20f}", f'{gcdTime10000:.20f}', f'{lcmTime10000:.20f}']}

df = pd.DataFrame(timeResultsAll, index=["longAddMod", "longSubMod", "longMulMod", "gcd", "lcm"])

print(df)'''