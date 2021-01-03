#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import subprocess
import math

staticimei = 0
quickstart = True

def bruteforce(increment):
    algoOEMcode     = 1000000000000000  # base
    autoreboot      = True              # phone has auto-reboot?
    autorebootcount = 4                 # number of attempts before reboot minus one (5 attempts - 1 = 4)
    savecount       = 200               # save progress every 200 attempts
    unknownfail     = False             # fail if unknown output

    failmsg = "check password failed"

    unlock = False
    n=0

    while (unlock == False):
        print("[+] В настоящее время тестируемый код "+str(algoOEMcode).zfill(16))
        output = subprocess.run("fastboot oem unlock "+str(algoOEMcode).zfill(16), shell=True, stderr=subprocess.PIPE).stderr.decode('utf-8')
        output = output.lower()
        n+=1

        if 'success' in output:
            bak = open("unlock_code.txt", "w")
            bak.write("Код загрузчика: "+str(algoOEMcode))
            bak.close()
        if 'reboot' in output:
            print("[!] Устройство имеет защиту от брутфорса! Установка защиты от перезагрузки и продолжение ...")
            os.system("adb wait-for-device")
            os.system("adb reboot bootloader")
            autoreboot=True
        if failmsg in output:
            pass
        if 'success' not in output and 'reboot' not in output and failmsg not in output and unknownfail:
            # fail
            print("[-] Не удалось проанализировать вывод")
            exit()
        if (n%savecount==0):
            bak = open("saves.txt", "w")
            bak.write("SAVE "+str(algoOEMcode))
            bak.close()
            print("[*] Прогресс сохранен")

        algoOEMcode += increment

        if (algoOEMcode > 10000000000000000):
            print("[!] OEM код не найден")
            os.system("fastboot reboot")
            exit()

def luhn_checksum(imei):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(imei)
    oddDigits = digits[-1::-2]
    evenDigits = digits[-2::-2]
    checksum = 0
    checksum += sum(oddDigits)
    for i in evenDigits:
        checksum += sum(digits_of(i*2))
    return checksum % 10

# setup
print(' ______     ______     ______     ______   ______     ______     _____     ______        ______     ______     __  __     ______   ______    ')
print('/\  == \   /\  __ \   /\  __ \   /\__  _\ /\  ___\   /\  __ \   /\  __-.  /\  ___\      /\  == \   /\  == \   /\ \/\ \   /\__  _\ /\  ___\   ')
print('\ \  __<   \ \ \/\ \  \ \ \/\ \  \/_/\ \/ \ \ \____  \ \ \/\ \  \ \ \/\ \ \ \  __\      \ \  __<   \ \  __<   \ \ \_\ \  \/_/\ \/ \ \  __\   ')
print(' \ \_____\  \ \_____\  \ \_____\    \ \_\  \ \_____\  \ \_____\  \ \____-  \ \_____\     \ \_____\  \ \_\ \_\  \ \_____\    \ \_\  \ \_____\ ')
print('  \/_____/   \/_____/   \/_____/     \/_/   \/_____/   \/_____/   \/____/   \/_____/      \/_____/   \/_/ /_/   \/_____/     \/_/   \/_____/ ')
print('                                                                                                    Bootloader Code Bruteforcer by @capice_0 ')

os.system('adb devices')

print("[!] Пожалуйста, выберите \"Разрешить с этого компьютера\" в диалоговом окне adb")

checksum = 1
while (checksum != 0):
    if staticimei == 0:
        imei = int(input('[*] Напишите IMEI: '))
    if staticimei > 0:
        imei = staticimei
    checksum = luhn_checksum(imei)
    if (checksum != 0):
        print('IMEI неверный!')
        if(staticimei > 0):
            exit()
increment = int(math.sqrt(imei)*1024)
if quickstart==False:
    input('[*] Нажмите ENTER, чтобы перезагрузить устройство...\n')
os.system('adb reboot bootloader')

codeOEM = bruteforce(increment)

os.system('fastboot getvar unlocked')

print('\n\n[!] УСТРОЙСТВО РАЗБЛОКИРОВАНО! OEM КОД: '+codeOEM+'\n')
exit()

