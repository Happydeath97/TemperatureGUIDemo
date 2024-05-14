import tkinter as tk
import csv


def add_data_to_csv(file_path, data):
    """
    Add data to a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        data (list): List of data to be added to the CSV file.
                     Each item in the list represents a row of data.
    """
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


class TemperatureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Temperature App")
        self.geometry("300x150")

        self.temperature_label = tk.Label(self, text="Temperature: 0°C")
        self.temperature_label.pack(pady=10)

        # Create a canvas widget
        self.canvas = tk.Canvas(self, width=200, height=10)
        self.canvas.pack()

        # Create the colored portion of the slider background
        self.canvas.create_rectangle(0, 0, 120, 10, fill="green")  # Light blue background
        self.canvas.create_rectangle(120, 0, 170, 10, fill="orange")
        self.canvas.create_rectangle(170, 0, 200, 10, fill="red")

        self.temperature_slider = tk.Scale(self, from_=0, to=100, orient="horizontal", length=200,
                                           showvalue=0, command=self.update_temperature)
        self.temp_data = [0 for _ in range(20)]
        self.temperature_slider.pack()
        self.update_temperature()
        self.after(50, self.read_temperature)

    def update_temperature(self, event=None):
        temperature = self.temperature_slider.get()
        self.temperature_label.config(text=f"Temperature: {temperature}°C")

    def read_temperature(self):
        temperature = self.temperature_slider.get()
        self.temp_data.insert(0, temperature)
        self.temp_data.pop()
        add_data_to_csv("data.csv", self.temp_data + [self.temperature_evaluation()])
        self.after(50, self.read_temperature)

    def temperature_evaluation(self):
        temp = self.temp_data
        if any(temp) >= 90:
            return 1
        count = 0
        for t in temp:
            if t >= 60:
                count += 1
        if count >= 3:
            return 1
        return 0


if __name__ == "__main__":
    app = TemperatureApp()
    app.mainloop()
