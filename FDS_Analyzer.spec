# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

# Збираємо ВСІ модулі для проблемних бібліотек
pandas_imports = collect_submodules('pandas')
numpy_imports = collect_submodules('numpy')
openpyxl_imports = collect_submodules('openpyxl')

datas_pandas = []
binaries_pandas = []
hiddenimports_pandas = []
tmp_ret = collect_all('pandas')
datas_pandas += tmp_ret[0]
binaries_pandas += tmp_ret[1]
hiddenimports_pandas += tmp_ret[2]

a = Analysis(
    ['app_gui.py'],
    pathex=[],
    binaries=binaries_pandas,
    datas=datas_pandas,
    hiddenimports=[
        'tkinter',
        'matplotlib.backends.backend_tkagg',
        'docx',
        'lxml',
        'lxml.etree',
        'PIL._tkinter_finder'
    ] + pandas_imports + numpy_imports + openpyxl_imports + hiddenimports_pandas,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['IPython', 'jupyter', 'notebook', 'pytest', 'sphinx', 'setuptools.tests'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FDS_Analyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Вимкнути консоль для GUI додатку
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Можна додати іконку якщо є
)
