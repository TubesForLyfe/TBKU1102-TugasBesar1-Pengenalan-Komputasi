# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Rangga Garmastewira\\PycharmProjects\\atmTest'],
             binaries=[],
             datas=[('C:\\Users\\Rangga Garmastewira\\AppData\\Local\\Programs\\Python\\Python38-32\\lib\\site-packages\\eel\\eel.js', 'eel'), ('static', 'static')],
             hiddenimports=['bottle_websocket'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
