'''

Created on 14 Feb 2020
@author: nga

'''
# This only work with Ubuntu and MacOS
#from watchdog.observers import Observer
# This work with Windows also!
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

import os, sys
import time
import subprocess
import shutil
import logging

observed_path   = "/workspace/input"
sys_script_path = "/workspace/scripts/sclite_stm_scoring.py"

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
Logger = logging.getLogger('inputObserver')


class MediaFileHandler(FileSystemEventHandler):

    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        Logger.info("Got event for file %s" % event.src_path)
        Logger.info("Transcribe this file: "  + sys_script_path)
        args = ['python3', sys_script_path, event.src_path]
        if not event.src_path.endswith('.TextGrid'):
            return
        # check file size
        historicalSize = -1
        time_in_seconds = float(os.getenv('CHECKING_FILESZ_TIME', 2))
        
        file_path = event.src_path
        while (historicalSize != os.path.getsize(file_path)):
            historicalSize = os.path.getsize(file_path)
            time.sleep(time_in_seconds)

        subprocess.call(args)

if __name__ == '__main__':
    cwd = os.getcwd()
    os.environ["PYTHONPATH"] = cwd

    observed_path = os.path.abspath(sys.argv[1])
    if (not os.path.exists(observed_path)):
        print ("ERROR: The input path you provided does not exist.")
        exit(0)

    #observer = Observer()
    # This work with Windows also!
    observer = PollingObserver() 
    event_handler = MediaFileHandler() # create event handler

    # set observer to use created handler in directory
    observer.schedule(event_handler, path=observed_path)
    observer.start()

    # sleep until keyboard interrupt, then stop + rejoin the observer
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
