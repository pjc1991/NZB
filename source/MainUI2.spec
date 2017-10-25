# -*- mode: python -*-

block_cipher = None

added_files = [
                ('phantomJS.exe', '.')
                ('NZB.ui', '.')
                ('Init.ui', '.')

a = Analysis(['MainUI2.py'],
             pathex=['C:\\Users\\whdek\\PycharmProjects\\NZB2'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MainUI2',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
