import random

verify_code_salt = 810894

# 验证码机制
def generate_raw():
    global verify_code_salt
    num = random.randint(1, verify_code_salt)
    print('raw: ' + str(num))
    return num
def en_vcode(num):
    global verify_code_salt
    num = num * 2 +  verify_code_salt
    print('en: ' + str(num))
    return num
def de_vcode(num):
    global verify_code_salt
    num = (num - verify_code_salt) // 2
    print('de: ' + str(num))
    return num