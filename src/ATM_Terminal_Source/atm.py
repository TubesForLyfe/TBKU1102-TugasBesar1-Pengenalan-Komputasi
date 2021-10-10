from art import *
import os

def horizontal_break():
    print("="*100)

def format_num(x):
    return format(x,',d').replace(",",".")

def inisialisasi():
    if not os.path.exists('./data_atm.txt'):
        with open('data_atm.txt', 'w') as fobj:
            fobj.write('1231231231-Tuan Mor-123456-200000\n1231231232-Pak Dengklek-654321-200000\n')
    temp = []
    with open('data_atm.txt', 'r') as fobj:
        temp = fobj.readlines()
    users = []
    for x in temp:
        users.append(x.rstrip().split('-'))
    logged_in = False
    return logged_in, users

def pilih_bahasa():
    horizontal_break()
    bahasa = ''
    while bahasa == '':  # Belum menemukan pilihan bahasa
        temp = input("Masukkan bahasa yang diinginkan/Choose the language you want to use (Indonesia/Inggris): ")
        # Cek inputnya, ganti bahasa sesuai yang diinginkan
        if temp.lower() == 'indonesia':
            bahasa = 'Indonesia'
        elif temp.lower() == 'inggris':
            bahasa = 'Inggris'
        else:
            print("Input Anda tidak dimengerti ATM.")
    return bahasa

def minta_kartu():
    horizontal_break()
    tprint('ATM')
    global users
    global bahasa
    flag = True
    no_rekening = ''
    nama_user = ''
    pin_user = ''
    saldo = 0
    while flag:
        rekening = input('Masukkan kartu Anda (input nomor rekening 10 digit): ' if bahasa=='Indonesia' else 'Enter your card (10 digits of your account): ')
        for user in users:
            if rekening in user:
                no_rekening = user[0]
                nama_user = user[1]
                pin_user = user[2]
                saldo = int(user[3])
                flag = False
                print('Anda akan diminta untuk memasukkan pin.' if bahasa=='Indonesia' else 'You will be asked input your pin.')
        if flag:
            print('Input yang Anda masukkan tidak dikenal dalam database.' if bahasa=='Indonesia' else 'Your input is not recognized in our database.')
    return no_rekening, nama_user, pin_user, saldo

def autentikasi():
    horizontal_break()
    tprint('ATM')
    global pin_user
    global bahasa
    global logged_in
    while not logged_in:
        pin = input("Masukkan pin Anda: " if bahasa == 'Indonesia' else 'Enter your pin: ')
        if pin == pin_user:
            logged_in = True
            print('Anda berhasil masuk ke dalam sistem.' if bahasa == 'Indonesia' else 'You have been logged in to the system.')
        else:
            print("Pin Anda salah." if bahasa == 'Indonesia' else 'You entered the wrong pin.')

def minta_transaksi():
    horizontal_break()
    tprint('Menu')
    global bahasa
    global nama_user
    valid = False
    if bahasa == 'Indonesia':
        print(f'Halo, {nama_user}!')
        print('Pilih jenis transaksi yang Anda ingin lakukan: ')
        print('\t1. Simpan tunai')
        print('\t2. Ambil tunai')
        print('\t3. Transfer')
        print('\t4. Cek saldo')
        print('\t5. Akhiri transaksi')
        print('Masukkan input berupa nomor saja (contoh: 1).')
    else:
        print(f'Hello, {nama_user}!')
        print('Choose your transaction method: ')
        print('\t1. Deposit cash')
        print('\t2. Withdraw cash')
        print('\t3. Transfer')
        print('\t4. Check balance')
        print('\t5. End the transaction')
        print('Your input should be just the number (example: 1).')
    while not valid:
        prompt = ''
        if bahasa == 'Indonesia':
            prompt = 'Masukkan jenis transaksi yang ingin Anda lakukan: '
        else:
            prompt = 'Enter which transaction method you want to do: '
        choice = input(prompt)
        if choice == '1':
            simpan_tunai()
            valid = True
        elif choice == '2':
            ambil_tunai()
            valid = True
        elif choice == '3':
            transfer_tunai()
            valid = True
        elif choice == '4':
            cek_saldo()
            valid = True
        elif choice == '5':
            keluar()
            valid = True
        else:
            if bahasa == 'Indonesia':
                print('Input yang Anda masukkan tidak dimengerti oleh sistem.')
            else:
                print('Your input cannot be recognized by the system.')

def transaksi_lain():
    horizontal_break()
    global bahasa
    prompt = ''
    if bahasa == 'Indonesia':
        prompt = 'Apakah Anda ingin melaksanakan transaksi lain? (y/n): '
    else:
        prompt = 'Do you want to do another transaction? (y/n): '
    flag = True
    while flag:
        choice = input(prompt)
        if choice.lower() == 'y':
            minta_transaksi()
            flag = False
        elif choice.lower() == 'n':
            keluar()
            flag = False
        else:
            if bahasa == 'Indonesia':
                print('Input yang Anda masukkan tidak dimengerti oleh sistem.')
            else:
                print('Your input cannot be recognized by the system.')

def keluar():
    horizontal_break()
    global saldo
    global bahasa
    global no_rekening
    tprint('Terima  Kasih!' if bahasa=='Indonesia' else 'Thank  You!')
    print('Anda telah mengakhiri transaksi Anda.' if bahasa=='Indonesia' else 'You have finished your transaction.')
    print(f'Saldo Anda tersisa Rp{format_num(saldo)}.' if bahasa=='Indonesia' else f'You have Rp{format_num(saldo)} left in your balance.')

def simpan_tunai():
    horizontal_break()
    global bahasa
    global saldo
    global no_rekening
    tprint('Simpan  Tunai' if bahasa == 'Indonesia' else 'Deposit  Cash')
    prompt_simpan_tunai = ''
    if bahasa == 'Inggris':
        prompt_simpan_tunai = 'Please insert your cash: '
    else:
        prompt_simpan_tunai = 'Masukkan lembaran uang Anda: '

    error_simpan_tunai = ''
    if bahasa == 'Inggris':
        error_simpan_tunai = 'Your cash must be a multiplier of 50.000.'
    else:
        error_simpan_tunai = 'Uang yang Anda masukkan harus merupakan kelipatan dari 50.000.'

    flag_simpan_tunai = False
    nominal_simpan_tunai = 0
    while not flag_simpan_tunai:
        nominal_simpan_tunai = int(input(prompt_simpan_tunai))
        if nominal_simpan_tunai > 0:
            if nominal_simpan_tunai % 50000 == 0:
                flag_simpan_tunai = True
            else:
                print(error_simpan_tunai)
        else:
            if bahasa == 'Inggris':
                print("Your input must be positive.")
            else:
                print("Input Anda harus positif.")

    saldo += nominal_simpan_tunai
    update_saldo(no_rekening, saldo)
    horizontal_break()
    tprint('Berhasil!' if bahasa == 'Indonesia' else 'Success!')
    if bahasa == 'Inggris':
        print(f'You have deposited an amount of Rp{format_num(nominal_simpan_tunai)}.')
        print(f'Your current balance is now Rp{format_num(saldo)}.')
    else:
        print(f'Anda telah memasukkan uang sebesar Rp{format_num(nominal_simpan_tunai)}.')
        print(f'Saldo Anda sekarang sebesar Rp{format_num(saldo)}.')
    transaksi_lain()

def ambil_tunai():
    horizontal_break()
    global bahasa
    global saldo
    global no_rekening
    tprint('Ambil  Tunai' if bahasa == 'Indonesia' else 'Withdraw  Cash')
    prompt_ambil_tunai = ''
    if bahasa == 'Inggris':
        prompt_ambil_tunai = 'Please insert the amount of cash you need: '
    else:
        prompt_ambil_tunai = 'Masukkan nominal yang Anda inginkan: '

    error_ambil_tunai = ''
    if bahasa == 'Inggris':
        error_ambil_tunai = 'Your cash must be a multiplier of 50.000.'
    else:
        error_ambil_tunai = 'Uang yang Anda masukkan harus merupakan kelipatan dari 50.000.'

    flag_ambil_tunai = False
    nominal_ambil_tunai = 0
    while not flag_ambil_tunai:
        nominal_ambil_tunai = int(input(prompt_ambil_tunai))
        if nominal_ambil_tunai > 0:
            if saldo >= nominal_ambil_tunai:
                if nominal_ambil_tunai % 50000 == 0:
                    flag_ambil_tunai = True
                else:
                    print(error_ambil_tunai)
            else:
                if bahasa == 'Inggris':
                    print("Your input exceeds your current deposit.")
                else:
                    print("Input yang Anda masukkan melebihi saldo Anda.")
        else:
            if bahasa == 'Inggris':
                print("Your input must be positive.")
            else:
                print("Input yang Anda masukkan harus positif.")

    # Menambahkan saldo
    saldo -= nominal_ambil_tunai
    update_saldo(no_rekening, saldo)
    horizontal_break()
    tprint('Berhasil!' if bahasa == 'Indonesia' else 'Success!')
    if bahasa == 'Inggris':
        print(f'You have withdrawn an amount of Rp{format_num(nominal_ambil_tunai)}.')
        print(f'Your current balance is now Rp{format_num(saldo)}.')
    else:
        print(f'Anda telah menarik uang sebesar Rp{format_num(nominal_ambil_tunai)}.')
        print(f'Saldo Anda sekarang sebesar Rp{format_num(saldo)}.')
    transaksi_lain()

def transfer_tunai():
    horizontal_break()
    global bahasa
    global saldo
    global no_rekening
    global users
    tprint('Transfer')
    transfer_prompt = ''
    if bahasa == 'Inggris':
        transfer_prompt = 'Please input your destination account: '
    else:
        transfer_prompt = 'Masukkan rekening tujuan Anda: '

    rekening_orang = input(transfer_prompt)
    saldo_orang = -1
    nama_orang = ''
    flag = True
    while flag:
        if rekening_orang == no_rekening:
            print('Anda tidak bisa mentransfer ke akun sendiri.' if bahasa=='Indonesia' else 'You cannot transfer to your own account.')
            rekening_orang = input(transfer_prompt)
        else:
            for user in users:
                if rekening_orang == user[0] and rekening_orang != no_rekening:
                    saldo_orang = int(user[3])
                    nama_orang = user[1]
                    flag = False
            if flag:
                if bahasa == 'Inggris':
                    print("Invalid destination account.")
                    rekening_orang = input(transfer_prompt)
                else:
                    print("Rekening yang Anda masukkan tidak dikenali.")
                    rekening_orang = input(transfer_prompt)

    if bahasa == 'Inggris':
        print(f'You will be transferring to {nama_orang}\'s account.')
    else:
        print(f'Anda akan melakukan transfer ke rekening {nama_orang}.')

    if bahasa == 'Inggris':
        transfer_prompt = 'Please input your desired transfer value: '
    else:
        transfer_prompt = 'Masukkan nominal yang Anda ingin transfer: '

    # Mengirim uang
    error_transfer_tunai = ''
    if bahasa == 'Inggris':
        error_transfer_tunai = 'Your cash must be a multiplier of 50.000.'
    else:
        error_transfer_tunai = 'Uang yang Anda masukkan harus merupakan kelipatan dari 50.000'

    flag_transfer_tunai = False
    nominal_transfer_tunai = 0
    while not flag_transfer_tunai:
        nominal_transfer_tunai = int(input(transfer_prompt))
        if nominal_transfer_tunai > 0:
            if saldo >= nominal_transfer_tunai:
                if nominal_transfer_tunai % 50000 == 0:
                    flag_transfer_tunai = True
                else:
                    print(error_transfer_tunai)
            else:
                if bahasa == 'Inggris':
                    print("Your input exceeds your current deposit.")
                else:
                    print("Input yang Anda masukkan melebihi saldo Anda.")
        else:
            if bahasa == 'Inggris':
                print("Your input must be positive.")
            else:
                print("Input yang Anda masukkan harus positif.")

    # Menambahkan saldo
    saldo -= nominal_transfer_tunai
    saldo_orang += nominal_transfer_tunai
    update_saldo(no_rekening, saldo)
    update_saldo(rekening_orang, saldo_orang)
    horizontal_break()
    tprint('Berhasil!' if bahasa == 'Indonesia' else 'Success!')
    if bahasa == 'Inggris':
        print(f'You have transferred an amount of Rp{format_num(nominal_transfer_tunai)} to {nama_orang}\'s account.')
        print(f'Your current balance is now Rp{format_num(saldo)}.')
    else:
        print(f'Anda telah mentransfer uang sebesar Rp{format_num(nominal_transfer_tunai)} ke rekening {nama_orang}.')
        print(f'Saldo Anda sekarang sebesar Rp{format_num(saldo)}.')
    transaksi_lain()

def cek_saldo():
    global bahasa
    global no_rekening
    global nama_user
    global saldo
    horizontal_break()
    tprint('Cek  Saldo' if bahasa=='Indonesia' else 'Check   Balance')
    print(f'\tNama pengguna: {nama_user}' if bahasa=='Indonesia' else f'\tUser\'s name: {nama_user}')
    print(f'\tNomor rekening: {no_rekening}' if bahasa=='Indonesia' else f'\tAccount number: {no_rekening}')
    print(f'\tSaldo: Rp{format_num(saldo)}' if bahasa=='Indonesia' else f'\tBalance: Rp{format_num(saldo)}')
    transaksi_lain()

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

# === PROGRAM ===
logged_in, users = inisialisasi()
bahasa = pilih_bahasa()
no_rekening, nama_user, pin_user, saldo = minta_kartu()
autentikasi()
minta_transaksi()
