# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
a = Analysis(['../app.py'], pathex=['../launcher'], binaries=[], datas=[('../assets', 'launcher/assets'), ('../../site', 'site')], hiddenimports=[], hookspath=[], runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='DgmCraft', debug=False, console=False, icon='../assets/brand/DgmCraft-app-icon.ico')
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, name='DgmCraft')
