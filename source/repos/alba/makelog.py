from datetime import datetime
import os

def writelog(contents , finish  = False):
    global f
    directory = "./log"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = directory+"/"+ datetime.today().strftime('%Y-%m-%d') + "_log.txt"
    time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S') 
    if os.path.isfile(file_name):
        try:
            f.write(time+contents+"\n")
            f.flush()
        except Exception as e:
            f = open(file_name, "a")
            f.write(time+contents+"\n")
            f.flush()

    else:
        f = open(file_name ,"w")
        f.write(time+contents+"\n")
        f.flush()
    if finish:  
        f.close()

