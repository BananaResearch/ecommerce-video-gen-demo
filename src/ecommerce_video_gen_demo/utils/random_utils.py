import random

def gen_sd_seed():
    # 生成一个介于0和2^32 - 1之间的随机整数作为种子值
    random_seed = random.randint(0, 2**32 - 1)

    return random_seed