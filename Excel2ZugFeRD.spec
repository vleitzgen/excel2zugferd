# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

datas = [
    ('_internal/Fonts', 'Fonts'),
    ('_internal/version.json', '.'),
    ('_internal/sRGB2014.icc', '.'),
] + collect_data_files('drafthorse', includes=['schema/**/*'])

a = Analysis(
    ['excel2zugferd.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['_pytest', 'mccabe', 'pycodestyle', 'pytest', 'radon'],
    noarchive=False,
    # NumPy 1.26 reads docstrings at import time, so level 2 is not safe.
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='excel2zugferd',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='excel2zugferd',
)
