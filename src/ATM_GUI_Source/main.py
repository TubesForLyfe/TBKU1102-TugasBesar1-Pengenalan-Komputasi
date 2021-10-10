import eel
import os

# >> FUNGSI
# def create_file():
#     with open('data_atm.txt', 'w') as fobj:
#         fobj.write('Tuan Mor\n123456\n200\n')
#
# def read_file():
#     user = ''
#     correct_pin = ''
#     saldo = 0
#     lines = []
#     with open('data_atm.txt', 'r') as fobj:
#         lines = fobj.readlines()
#     user = lines[0].rstrip()
#     correct_pin = lines[1].rstrip()
#     saldo = int(lines[2].rstrip())
#     return user, correct_pin, saldo
#
# def update_file():
#     with open('data_atm.txt', 'w') as fobj:
#         fobj.write(f'{user}\n{correct_pin}\n{saldo}')

def inisialisasi():
    if not os.path.exists('./data_atm.txt'):
        with open('data_atm.txt', 'w') as fobj:
            fobj.write('1231231231-Tuan Mor-123456-200\n1231231232-Pak Dengklek-654321-200\n')
    temp = []
    with open('data_atm.txt', 'r') as fobj:
        temp = fobj.readlines()
    users = []
    for x in temp:
        users.append(x.rstrip().split('-'))
    return users

def update_saldo(rekening, saldo):
    global users
    user_index = -1
    for i in range(len(users)):
        if users[i][0] == rekening:
            user_index = i
            break
    users[user_index][3] = saldo
    string_to_write = ''
    for x in range(len(users)):
        temp_string = f'{users[x][0]}-{users[x][1]}-{users[x][2]}-{users[x][3]}\n'
        string_to_write += temp_string
    with open('./data_atm.txt', 'w') as fobj:
        fobj.write(string_to_write)

# >> MAIN PROGRAM
users = inisialisasi()

# user, correct_pin, saldo = read_file()
rekening = ''
user = ''
correct_pin = ''
saldo = 0

penarikan = 0
deposit = 0
pin_list = []
nominal_list = ['$']
rekening_list = []
akun_list = []
transfer_list = ['$']

rekening_tujuan = ''
user_tujuan = ''
saldo_tujuan = 0

rekening_valid = '1231231231'

# Halaman minta rekening
@eel.expose
def add_akun(num):
    global akun_list
    if len(akun_list) < 10:
        akun_list.append(str(num))
        x = ''.join(akun_list)
        eel.update_akun(x)

@eel.expose
def erase_akun():
    global akun_list
    if len(akun_list) > 0:
        akun_list.pop()
        x = ''.join(akun_list)
        eel.update_akun(x)

@eel.expose
def ke_pin():
    global akun_list
    global users
    global rekening
    global user
    global correct_pin
    global saldo
    if len(akun_list) == 10:
        akun = ''.join(akun_list)
        for x in users:
            if akun in x:
                rekening = x[0]
                user = x[1]
                correct_pin = x[2]
                saldo = int(x[3])
                akun_list = []
                eel.masuk()
        if user == '':
            eel.update_akun('Tidak ditemukan')
            eel.sleep(1)
            eel.update_akun('')
            akun_list = []

# Halaman autentikasi
@eel.expose
def add_click(num, current_str):
    global pin_list
    if len(pin_list) < 6:
        pin_list.append(str(num))
        temp = list(current_str)
        temp.append('x')
        ret_val = ''.join(temp)
        eel.update_text(ret_val)

@eel.expose
def validate(pin):
    global pin_list
    if len(pin_list) == 6:
        current_pin = ''.join(pin_list)
        if current_pin == correct_pin:
            eel.enter_cp()
            pin_list = []
        else:
            eel.update_text("Silakan coba lagi.")
            eel.sleep(1)
            eel.update_text("")
            pin_list = []

@eel.expose
def erase_pin(current_str):
    global pin_list
    if len(pin_list) > 0:
        pin_list.pop()
        temp = list(current_str)
        temp.pop()
        ret_val = ''.join(temp)
        eel.update_text(ret_val)

# Halaman CP
@eel.expose
def get_info():
    global user
    global saldo
    saldo_str = f'${saldo}'
    eel.update_info(user, saldo_str)

# Halaman tarik tunai
@eel.expose
def tarik_tunai(amount):
    global saldo
    global rekening
    if amount <= saldo:
        global penarikan
        penarikan = amount
        saldo -= amount
        update_saldo(rekening, saldo)
        eel.go_transaksi()
    else:
        eel.go_gagal()

# Halaman transaksi
@eel.expose
def get_info_transaksi():
    global saldo
    global penarikan
    besar_tunai = f'${penarikan}'
    besar_saldo = f'${saldo}'
    eel.update_transaksi(besar_tunai, besar_saldo)

# Halaman tarik tunai dengan nominal custom
@eel.expose
def erase_nominal():
    global nominal_list
    if len(nominal_list) > 1:
        nominal_list.pop()
        update = ''.join(nominal_list)
        eel.update_nominal(update)

@eel.expose
def add_nominal(num, current):
    global nominal_list
    if len(nominal_list) < 4:
        nominal_list.append(str(num))
        update = ''.join(nominal_list)
        eel.update_nominal(update)

@eel.expose
def tarik():
    global nominal_list
    new_list = nominal_list[:]
    new_list.remove('$')
    check = ''.join(new_list)
    if int(check) % 5 == 0 and int(check) <= 200:
        tarik_tunai(int(check))

@eel.expose
def reset_nominal_data():
    global nominal_list
    nominal_list = ['$']

# Halaman deposit
@eel.expose
def deposit(amount):
    global saldo
    global deposit
    global rekening
    deposit = amount
    saldo += amount
    update_saldo(rekening, saldo)

# Halaman transaksi deposit
@eel.expose
def get_info_deposit():
    global saldo
    global deposit
    ret_saldo = f'${saldo}'
    ret_deposit = f'${deposit}'
    eel.update_deposit(ret_deposit, ret_saldo)

# Halaman transfer-1
@eel.expose
def reset_rekening_data():
    global rekening_list
    rekening_list = []

@eel.expose
def add_rekening(num):
    global rekening_list
    if len(rekening_list) < 10:
        rekening_list.append(str(num))
        rekening_string = ''.join(rekening_list)
        eel.update_rekening(rekening_string)

@eel.expose
def erase_rekening():
    global rekening_list
    if len(rekening_list) > 0:
        rekening_list.pop()
        rekening_string = ''.join(rekening_list)
        eel.update_rekening(rekening_string)

@eel.expose
def ke_transfer():
    global rekening_list
    global rekening
    global rekening_tujuan
    global user_tujuan
    global saldo_tujuan
    global users
    if len(rekening_list) == 10:
        check = ''.join(rekening_list)
        if check == rekening:
            eel.update_rekening('Tidak diterima')
            eel.sleep(1)
            eel.update_rekening('')
            rekening_list = []
        else:
            found = False
            for x in users:
                if check == x[0]:
                    rekening_tujuan = check
                    user_tujuan = x[1]
                    saldo_tujuan = int(x[3])
                    found = True
            if not found:
                eel.update_rekening('Tidak ditemukan')
                eel.sleep(1)
                eel.update_rekening('')
                rekening_list = []
            else:
                eel.go_transfer()

# Halaman transfer-2
@eel.expose
def reset_transfer_data():
    global transfer_list
    transfer_list = ['$']

@eel.expose
def set_text_1():
    global user_tujuan
    eel.setText1(f'Anda akan mentransfer uang ke rekening {user_tujuan}.')

@eel.expose
def erase_transfer():
    global transfer_list
    if len(transfer_list) > 1:
        transfer_list.pop()
        eel.update_transfer(''.join(transfer_list))

@eel.expose
def add_transfer(num):
    global transfer_list
    if len(transfer_list) < 4:
        transfer_list.append(str(num))
        eel.update_transfer(''.join(transfer_list))

@eel.expose
def ke_transaksi():
    global transfer_list
    global saldo
    global saldo_tujuan
    global rekening
    global rekening_tujuaan
    if len(transfer_list) > 1:
        x = transfer_list[:]
        x.remove('$')
        angka = int(''.join(x))
        if angka > 200:
            eel.update_transfer('Tidak bisa')
            eel.sleep(1)
            eel.update_transfer('$')
            transfer_list = ['$']
        else:
            if angka > saldo:
                eel.update_transfer('Tidak cukup')
                eel.sleep(1)
                eel.update_transfer('$')
                transfer_list = ['$']
            else:
                saldo -= angka
                saldo_tujuan += angka
                update_saldo(rekening, saldo)
                update_saldo(rekening_tujuan, saldo_tujuan)
                eel.go_transaksi()

@eel.expose
def get_info_transaksi2():
    global saldo
    global user_tujuan
    global transfer_list
    eel.update_transaksi2(f'Transfer ke rekening {user_tujuan}', ''.join(transfer_list), f'${saldo}')

eel.init("static")
eel.start("minta_kartu.html", size=(500, 500))
