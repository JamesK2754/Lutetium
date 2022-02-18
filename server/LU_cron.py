#!/usr/local/bin/python3.10

import mysql.connector
import datetime
import time
from os import system
from LU_mail import sendmail

mydb = mysql.connector.connect(
    host="",
    user='',
    passwd="",
    database="Lutetium"
)
logfile = open("/home/pi/Lutetium/LUcron.log", "w")
logfile.write("")
logfile.close()
logfile = open("/home/pi/Lutetium/LUcron.log", "a")
curs = mydb.cursor()
curs.execute("SELECT * FROM `files`")
res = curs.fetchall()

if res != None:
    dlCount = 0
    failCount = 0
    for job in res:
        if job[4] != 0:
            logfile.write(f"[{datetime.datetime.now()}] Job '{job[1]}' in DB but status suggests already downloaded.\n")
            continue
        dlCount+=1
        success = True
        start_time = time.time()
        if job[3] == 1:
            try:
                system(f"youtube-dl -o '/home/pi/Lutetium/media/%(title)s-%(id)s.%(ext)s' {job[2]}")
                curs.execute(f"UPDATE files SET Status = 1 WHERE dlID = {job[0]}")
            except Exception as e:
                success = False
                failCount+=1
                logfile.write(f"[{datetime.datetime.now()}] ERROR: youtube-dl failed when trying to download {job[2]} [{e}]\n")
                curs.execute(f"UPDATE files SET Status = 2 WHERE dlID = {job[0]}")
        else:
            try:
                system(f"wget {job[2]} -P /home/pi/Lutetium/media/")
                curs.execute(f"UPDATE files SET Status = 1 WHERE dlID = {job[0]}")
            except Exception as e:
                success = False
                failCount += 1
                logfile.write(f"[{datetime.datetime.now()}] ERROR: wget failed when trying to download {job[2]} [{e}]\n")
                curs.execute(f"UPDATE files SET Status = 1 WHERE dlID = {job[0]}")
        mydb.commit()
        end_time = time.time()
        time_taken = end_time - start_time
    logfile.write(f"[{datetime.datetime.now()}] LUCron ran, {dlCount} downloads attempted, {failCount} failed.\n")
    logfile.close()
    if dlCount > 0:
        sendmail(f"Morning James,\nLutetium was ran tonight, attempting {dlCount} downloads and failing {failCount}. "
                f"These downloads are available for you now on the Lutetium server and/or flash drive."
                f"\nThank you for using Lutetium. \n", True, "Your post-run report")
else:
    print("No records")
    logfile.write(f"[{datetime.datetime.now()}] LUCron ran but no downloads were found.\n")
logfile.close()
print("all done")
