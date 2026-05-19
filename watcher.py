import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
print("Watcher started..")
class Watch(FileSystemEventHandler):
    def on_modified(self,event):
        print("Detected:",event.src_path)
        if event.src_path.endswith("input.txt"):
                print("Running script...")
                result=subprocess.run([r"C:\Users\Dell\AppData\Local\Programs\Python\Python312\Python.exe",
                                       r"F:\Sneha Backup\Career\BA\Portfolio\Sneha-Prabhakar-Portfolio\doc_quality_analyzer.py"],
                                       capture_output=True,
                                       text=True)
                print("Output:",result.stdout)
                print("Error:",result.stderr)
event_handler=Watch()
observer=Observer()
observer.schedule(event_handler,path=r"F:\Sneha Backup\Career\BA\Portfolio\Sneha-Prabhakar-Portfolio\input",recursive=False)
observer.start()
try:
    while True:
         time.sleep(1)
except KeyboardInterrupt:
     observer.stop()
observer.join()