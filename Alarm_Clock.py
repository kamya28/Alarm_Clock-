import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, time as dt_time
import threading
import time


class AlarmClock:
    def __init__(self, master):
        self.master = master
        self.master.title("Alarm Clock")
        self.master.geometry("400x200")

        self.label = ttk.Label(master, text="Set Alarm:")
        self.label.pack(pady=10)

        self.time_var = tk.StringVar()
        self.time_entry = ttk.Entry(
            master, textvariable=self.time_var, font=("Helvetica", 14)
        )
        self.time_entry.pack(pady=10)

        self.set_button = ttk.Button(master, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=10)

        self.stop_button = ttk.Button(
            master, text="Stop Alarm", state=tk.DISABLED, command=self.stop_alarm
        )
        self.stop_button.pack(pady=10)

        self.alarm_thread = None

    def set_alarm(self):
        alarm_time_str = self.time_var.get()
        try:
            alarm_time = datetime.strptime(alarm_time_str, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM")
            return

        current_time = datetime.now().time()

        if alarm_time <= current_time:
            messagebox.showerror("Error", "Invalid time. Please choose a future time.")
            return

        messagebox.showinfo(
            "Alarm Set", f"Alarm set for {alarm_time.strftime('%H:%M')}"
        )

        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread.join()

        self.alarm_thread = threading.Thread(
            target=self.wait_and_ring, args=(alarm_time,)
        )
        self.alarm_thread.start()

    def ring_alarm(self):
        messagebox.showinfo("Alarm", "Time's up! Wake up!")
        self.set_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def stop_alarm(self):
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread.join()
            messagebox.showinfo("Alarm Stopped", "Alarm stopped successfully.")
            self.set_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def wait_and_ring(self, alarm_time):
        self.set_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        while datetime.now().time() < alarm_time:
            time.sleep(1)

        self.ring_alarm()


if __name__ == "__main__":
    root = tk.Tk()
    clock = AlarmClock(root)
    root.mainloop()
