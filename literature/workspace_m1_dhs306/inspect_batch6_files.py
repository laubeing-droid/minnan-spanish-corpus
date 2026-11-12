import zipfile
import glob

pkg = glob.glob("literature/assets/dhs306/*0865_0869*")[0]
print("Found package:", pkg)
with zipfile.ZipFile(pkg, 'r') as zf:
    for n in zf.namelist():
        print(" ", n)
