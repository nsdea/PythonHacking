from colorama import Fore, Style, init 
from threading import Thread 
from queue import Queue 
import socket 
import time 
import sys
import os
# clear command
cmd = "cls"

# init colorama
init()
# port "db" :rofl:  
portdb = {
    21 : "ftp",
    22 : "ssh",
    25 : "some tcp service",
    80 : "http",
    443: "http",
    445: "smtp"
}


# formated print 
def formatted_print(host: str, ports: Queue) -> None:
    # clear terminal
    os.system(cmd)
    # info
    print("Result ({}): \n {}".format(host, "-" * 50))
    # print ports formated
    while not ports.empty():
        # get port from queue
        port = ports.get()
        # print formated
        print("{}[info]{} Port: {}{} - {}{} is open !!!".format(
            Fore.LIGHTRED_EX, Style.RESET_ALL,
            Fore.LIGHTGREEN_EX, port, portdb[port], Style.RESET_ALL,
        ))
        
# scanner function
def scanport(host: str, ports: Queue, result: Queue, timeout: float, tid: int):
    # short info print
    print("{}[i]{} Thread {} started!!! ".format(Fore.LIGHTRED_EX, Style.RESET_ALL, tid))
    # loop while queue is not empty
    while not ports.empty():
        # read port from queue
        port = ports.get()
        # create socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # set timeout
            sock.settimeout(timeout)
            # check if port % 250 == 0
            if port % 250 == 0:
                print("{}[i]{} Reached Port {}!!!".format(Fore.LIGHTRED_EX,
                                                          port, Style.RESET_ALL))
            # check if port is open => returs 0 if success
            if sock.connect_ex((host, port)) == 0:
                result.put(port)
                
# argumet parser
def parsearguments():
    if len(sys.argv) < 5:
        print("Usage: {} <host> <port> <threads> <timeout>".format(sys.argv[0]))
        exit(1)
    host, port =  sys.argv[1], int(sys.argv[2])
    runs, timeout = int(sys.argv[3]), float(sys.argv[4]) 
    return host, port, runs, timeout


# run portscanner
def run():
    # values to run 
    host, port, runs, timeout = parsearguments()
    # result ports to scan queue
    result = Queue()
    ports = Queue()
    # initialize the queue 
    for p in range(1, port + 1):
        ports.put(p)
    # workers - list of running threads
    workers = []
    # start threads
    for i in range(runs):
        t = Thread(target=scanport, args=(host, ports, result, timeout, i))
        t.start()
        workers.append(t)
        time.sleep(0.1)
    # info
    print("{}[info]{} Please wait a moment !!!".format(Fore.LIGHTRED_EX, Style.RESET_ALL))
    # wait until threads are returned
    for t in workers:
        t.join()
    # info  
    print("{}[info]{} Threads are returned !!!".format(Fore.LIGHTRED_EX, Style.RESET_ALL))
    # sleep a moment
    time.sleep(0.3)
    # formated print
    formated_print(host, result)
    

if __name__=="__main__":
    run()
