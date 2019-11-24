from pynput.keyboard import Key, Listener
import threading
from pynput.keyboard import KeyCode
class KeyListener(threading.Thread):
    def __init__(self):
        super(KeyListener, self).__init__()
        self.keys_pressed = set()
        self.listener = Listener()
        self.pause_listener = None
        self.quit_listener = None

    def register_pause(self, pause_func):
        self.pause_listener = pause_func
    def register_quit(self, quit_func):
        self.quit_listener = quit_func
    def is_pressed(self, key):
        if self.keys_pressed:
            if key in self.keys_pressed:
                return True
                
        return False
    def on_press(self, key):
        #print('{0} pressed'.format(
        #    key))
        self.keys_pressed.add("{}".format(key).strip('\''))
        if "{}".format(key).strip('\'') == 'p':
            #print("KEYS PRESSED {}".format(self.keys_pressed))
            if(self.pause_listener):
                self.pause_listener()

        if "{}".format(key).strip('\'') == 'q':
            #print("KEYS PRESSED {}".format(self.keys_pressed))
            if(self.quit_listener):
                self.quit_listener()
        

    def on_release(self, key):
        #print('{0} release'.format(
        #    key))
        #print("KEY REMOVE {}".format(self.keys_pressed))
        try:
            self.keys_pressed.remove("{}".format(key).strip('\''))
        except:
            None
        if key == Key.esc:
            # Stop listener
            return False
    def run(self):
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as self.listener:
            self.listener.join()
    def __del__(self):
        self.listener.stop()
    def exit(self):
        self.listener.stop()
if __name__ == "__main__":
    kl = KeyListener()
    kl.start()
    print("AFTER START")