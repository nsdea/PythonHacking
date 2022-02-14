from colorama import Fore, Style, init
from threading import Thread 
from queue import Queue 
import zipfile
import time
import sys 
import os 
# init colorama
init()

# found
found = [None, None]
    
# function to crack zip()
def crackzip(password: Queue, tid: int) -> None:
    # counter
    count = 0
    # info print
    print("{}[info]{} New Thread {} started...".format(Fore.LIGHTYELLOW_EX, 
                                                       Style.RESET_ALL ,tid))
    # start cracking
    while not password.empty():
        # if another thread found password
        if count % 5 == 0:
            if found[0]:
                break 
        # get password from queue
        passwd = password.get()
        # try to extract the file
        try:
            with zipfile.ZipFile("main.zip", "r") as zfile:
                # try to extract
                zfile.extractall(pwd=passwd.encode())
                # found password if sucess
                found.insert(0, True), found.insert(1, passwd)
                exit()
        except Exception as error:
            pass 
        
# load wordlist   
def loadwordlist(filepath: str) -> Queue:
    loadedlist = Queue()
    if os.path.exists(filepath):
        with open(filepath, "r") as wordlist:
            for word in wordlist:
                loadedlist.put(word.rstrip("\n").strip()) 
    return loadedlist            

# argument
def argumentparse():      
    if len(sys.argv) < 4:
        print("{}[i] Usage: {} <zipfile> <passwordlist> <threads>{}".format(
            Fore.LIGHTRED_EX, sys.argv[0], Style.RESET_ALL))
        exit(1)            
    return sys.argv[1], sys.argv[2], int(sys.argv[3])        
                
# run script
def run():
    # some userinput
    filepath, wordlist, threads = argumentparse()
    # load wordlist
    qwordlist = loadwordlist(wordlist)
    # list of running threads
    workers = []
    # start threads
    for t in range(threads):
        t = Thread(target=crackzip, args=(qwordlist, t), daemon=True)
        t.start()
        workers.append(t)
        # sleep a short moment
        time.sleep(0.1)
    # sleep a moment
    time.sleep(0.1)
    # print info on the screen
    print("{}[info]{} Cracking Password ...".format(Fore.LIGHTRED_EX, Style.RESET_ALL))
    # join threads
    for t in workers:
        t.join()
    # print password
    if found[0]:
        print("{}[info]{} Password found: -> {} !!!".format(Fore.LIGHTRED_EX,
                                                            Style.RESET_ALL, found[1]))
        exit()
    # password not found :cry:
    print("[i]Password not found")
    

if __name__=="__main__":
    run()