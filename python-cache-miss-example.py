# Bytes  type        empty + scaling notes
# 24     int         NA
# 28     long        NA
# 37     str         + 1 byte per additional character
# 52     unicode     + 4 bytes per additional character
# 56     tuple       + 8 bytes per additional item
# 72     list        + 32 for first, 8 for each additional
# 232    set         sixth item increases to 744; 22nd, 2280; 86th, 8424
# 280    dict        sixth item increases to 1048; 22nd, 3352; 86th, 12568 *
# 120    func def    does not include default args and other attrs
# 64     class inst  has a __dict__ attr, same scaling as dict above
# 16     __slots__   class with slots has no dict, seems to store in 
#                     mutable tuple-like structure.
# 904    class def   has a proxy __dict__ structure for class attrs
# 104    old class   makes sense, less stuff, has real dict though.

# BlockSize  CacheSpeed  CacheType  DeviceID        InstalledSize  Level  MaxCacheSize  NumberOfBlocks  Status  
# 1024       1           5          Cache Memory 0  1024           3      1024          1024            OK
# 1024       1           5          Cache Memory 1  8192           4      8192          8192            OK
# 65536      1           5          Cache Memory 2  65536          5      65536         1024            OK

import sys
import tracemalloc
import timeit
import random
import matplotlib.pyplot as plt
from collections import deque

class Value:
    num = 1

object = Value()
object_memory_estimate = sys.getsizeof(object) + sys.getsizeof(object.num)

print(sys.getsizeof(object), sys.getsizeof(object.num))

memory_wanted = 200 * 1024 * 1024
object_count = memory_wanted // sys.getsizeof(object_memory_estimate)

tracemalloc.start()

# Allocate
memory = [Value() for _ in range(object_count)]

print("Allocated Memory", tracemalloc.get_traced_memory())
tracemalloc.stop()

N = 100000

# Pick N consecutive objects
array = [memory[i] for i in range(N)]
llist = deque(array)

# Pick N random objects
rand_array = [memory[random.randint(0, len(memory))] for _ in range(N)]
rand_llist = deque(rand_array)

def read_array():
    x = 0
    for v in array:
        x = v.num

def read_llist():
    x = 0
    for v in llist:
        x = v.num

def read_rand_array():
    x = 0
    for v in rand_array:
        x = v.num

def read_rand_llist():
    x = 0
    for v in rand_llist:
        x = v.num

repetitions = 1000
print(timeit.timeit(read_array, number=repetitions), "Consecutive array")
print(timeit.timeit(read_llist, number=repetitions), "Consecutive list")
print(timeit.timeit(read_rand_array, number=repetitions), "Rand array")
print(timeit.timeit(read_rand_llist, number=repetitions), "Rand list")


N = 10000

fig, (ax1, ax2) = plt.subplots(2, sharex=True)

ax1.scatter(list(range(N)), [id(array[i]) for i in range(N)], label='array', s=10)
ax1.scatter(list(range(N)), [id(llist[i]) for i in range(N)], label='list', s=10)
ax1.legend()

ax2.scatter(list(range(N)), [id(rand_array[i]) for i in range(N)], label='rand_array', s=10)
ax2.scatter(list(range(N)), [id(rand_llist[i]) for i in range(N)], label='rand_list', s=10)
ax2.legend()

plt.show()