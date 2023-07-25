import chime
#chime.info(sync=True)
chime.success(sync=True)
import threading
class Notifier:
    def __init__(self, *notif_func):
        self.func_list = notif_func
    def notify(self):
        for i in self.func_list:
            i()
    def __call__(self):
        thread = threading.Thread(target=self.notify())
        thread.start()

n = Notifier()
n()