import sys


import queue
from threading import Event

if __name__ == '__main__':
    
    sys.path.append('/home/pi/python_p/kivyAppPrinterAndDb/KivyDbAndThreads/DataBaseUtility')
    sys.path.append('/home/pi/python_p/kivyAppPrinterAndDb/KivyDbAndThreads/Threads')

    print(sys.path)
    from firstMenu import DemoApp
    from MongoDbUtility import MongoDbHelper
    from PrinterThread import PrinterThread
    # create global object for using mongo db.
    globalMongoDbHelper = MongoDbHelper()

    q = queue.Queue()
    event = Event()
    printerT = PrinterThread(q, event, globalMongoDbHelper)
    printerT.start()
    DemoApp(eventGroup=event, queue=q, dbHelper=globalMongoDbHelper).run()
    q.put("done")
    q.put("done")
    event.set()
    printerT.join()
