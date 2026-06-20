import os
import time

while True:
    os.system("git add .")
    os.system('git commit -m "Auto Update"')
    os.system("git push")
    time.sleep(60)