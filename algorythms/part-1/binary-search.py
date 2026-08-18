# Нужна гарантия на монотонный предикант 
# Мы ищем границы а не результат поэтому просто == не получится
def bs(lo, hi, ok):
  while (lo < hi): 
    mid = lo + ((hi - lo) // 2)
    if ok(mid):
      return mid
    else:
      lo = mid - 1
    hi = mid
    print(lo, hi, mid)
  return mid
  

a = [1, 3, 3, 5, 7]

assert bs(0, len(a), lambda i: a[i] >= 3) == 1 # index 1 becuase 3 at index 1 is >= 3
assert bs(0, len(a), lambda i: a[i] > 9) == 5 # 5 is out of index so it is pass, since not found
assert bs(0, len(a), lambda i: a[i] >= 5) == 3 # index of 5 is 3
print("ok")