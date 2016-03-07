import os
import subprocess
QRImagePath = os.path.join(os.getcwd(), 'baby.jpg')
print(QRImagePath)
subprocess.call(['open', QRImagePath])
