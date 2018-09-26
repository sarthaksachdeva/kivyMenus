from kivyDemos.kivyHomeMenuGit.kivyMenus.firstMenu import DemoApp
from kivyDemos.kivyHomeMenuGit.DataBaseUtility.MongoDbUtility import MongoDbHelper
from kivyDemos.kivyHomeMenuGit.Threads.PrinterThread import PrinterThread

import queue
from threading import Event

if __name__ == '__main__':
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
