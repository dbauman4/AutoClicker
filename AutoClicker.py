import tkinter as tk
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Listener as KeyboardListener, KeyCode
import threading
import time

class AutoClickerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Auto Clicker")
        self.click_speed = 25  # Default click speed (clicks per second)
        self.clicking = False
        self.keybind_toggle = str(Key.insert)
        self.keybind_increase = str(Key.up)
        self.keybind_decrease = str(Key.down)
        self.record_button_active = False
        self.record_button_target = None

        self.create_widgets()
        self.setup_listeners()

    def create_widgets(self):
        # Click speed entry
        self.click_speed_label = tk.Label(self.master, text="Click Speed (CPS):")
        self.click_speed_label.grid(row=0, column=0, sticky="w")
        self.click_speed_entry = tk.Entry(self.master, state='normal')
        self.click_speed_entry.insert(0, str(self.click_speed))
        self.click_speed_entry.config(state='readonly')
        self.click_speed_entry.grid(row=0, column=1)

        # Toggle keybind entry
        self.toggle_keybind_label = tk.Label(self.master, text="Toggle Keybind:")
        self.toggle_keybind_label.grid(row=1, column=0, sticky="w")
        self.toggle_keybind_entry = tk.Entry(self.master, state='normal')
        self.toggle_keybind_entry.insert(0, str(self.keybind_toggle))
        self.toggle_keybind_entry.config(state='readonly')
        self.toggle_keybind_entry.grid(row=1, column=1)
        self.toggle_record_button = tk.Button(self.master, text="Record", command=lambda: self.toggle_record("toggle"))
        self.toggle_record_button.grid(row=1, column=2)

        # Increase keybind entry
        self.increase_keybind_label = tk.Label(self.master, text="Increase Speed Keybind:")
        self.increase_keybind_label.grid(row=2, column=0, sticky="w")
        self.increase_keybind_entry = tk.Entry(self.master, state='normal')
        self.increase_keybind_entry.insert(0, str(self.keybind_increase))
        self.increase_keybind_entry.config(state='readonly')
        self.increase_keybind_entry.grid(row=2, column=1)
        self.increase_record_button = tk.Button(self.master, text="Record", command=lambda: self.toggle_record("increase"))
        self.increase_record_button.grid(row=2, column=2)

        # Decrease keybind entry
        self.decrease_keybind_label = tk.Label(self.master, text="Decrease Speed Keybind:")
        self.decrease_keybind_label.grid(row=3, column=0, sticky="w")
        self.decrease_keybind_entry = tk.Entry(self.master, state='normal')
        self.decrease_keybind_entry.insert(0, str(self.keybind_decrease))
        self.decrease_keybind_entry.config(state='readonly')
        self.decrease_keybind_entry.grid(row=3, column=1)
        self.decrease_record_button = tk.Button(self.master, text="Record", command=lambda: self.toggle_record("decrease"))
        self.decrease_record_button.grid(row=3, column=2)

        # Start/Stop clicking button
        self.toggle_button = tk.Button(self.master, text="Start Clicking", command=self.toggle_clicking)
        self.toggle_button.grid(row=4, columnspan=3, pady=10)

    def setup_listeners(self):
        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.keyboard_listener.start()

    def toggle_clicking(self):
        self.clicking = not self.clicking
        if self.clicking:
            self.toggle_button.config(text="Stop Clicking")
            self.start_clicking()
        else:
            self.toggle_button.config(text="Start Clicking")

    def start_clicking(self):
        threading.Thread(target=self.auto_click).start()

    def auto_click(self):
        mouse = MouseController()
        print("Auto Clicker On!")
        while self.clicking:
            #print("CLICKING!")
            mouse.click(Button.left)
            time.sleep(1 / self.click_speed)
        print("Auto Clicker Off!")

    def on_key_press(self, key):
        #print("Keypressed: "+ str(key))
        if self.record_button_active:
            self.set_recorded_keybind(str(key))
            self.toggle_record(self.record_button_target)
        elif self.keybind_toggle is not None and str(key) == self.keybind_toggle:
            self.toggle_clicking()
        elif self.keybind_increase is not None and str(key) == self.keybind_increase:
            self.increase_speed()
        elif self.keybind_decrease is not None and str(key) == self.keybind_decrease:
            self.decrease_speed()
        

    def on_key_release(self, key):
        pass

    def increase_speed(self):
        self.click_speed += 1
        self.click_speed_entry.config(state='normal')
        self.click_speed_entry.delete(0, tk.END)
        self.click_speed_entry.insert(0, str(self.click_speed))
        self.click_speed_entry.config(state='readonly')

    def decrease_speed(self):
        if self.click_speed > 1:
            self.click_speed -= 1
            self.click_speed_entry.config(state='normal')
            self.click_speed_entry.delete(0, tk.END)
            self.click_speed_entry.insert(0, str(self.click_speed))
            self.click_speed_entry.config(state='readonly')

    def toggle_record(self, target):
        self.record_button_active = not self.record_button_active
        self.record_button_target = target

    def set_recorded_keybind(self, key):
        if self.record_button_target == "toggle":
            self.keybind_toggle = key
            self.toggle_keybind_entry.config(state='normal')
            self.toggle_keybind_entry.delete(0, tk.END)
            self.toggle_keybind_entry.insert(0, self.format_key(key))
            self.toggle_keybind_entry.config(state='readonly')
        elif self.record_button_target == "increase":
            self.keybind_increase = key
            self.increase_keybind_entry.config(state='normal')
            self.increase_keybind_entry.delete(0, tk.END)
            self.increase_keybind_entry.insert(0, self.format_key(key))
            self.increase_keybind_entry.config(state='readonly')
        elif self.record_button_target == "decrease":
            self.keybind_decrease = key
            self.decrease_keybind_entry.config(state='normal')
            self.decrease_keybind_entry.delete(0, tk.END)
            self.decrease_keybind_entry.insert(0, self.format_key(key))
            self.decrease_keybind_entry.config(state='readonly')

    def format_key(self, key):
        if isinstance(key, KeyCode):
            return key.char
        elif hasattr(key, 'name'):
            return key.name
        else:
            return str(key)


def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
