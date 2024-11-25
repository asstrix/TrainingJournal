import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime

# Файл для сохранения данных
data_file = 'training_log.json'


def load_data():
	"""Загрузка данных о тренировках из файла."""
	try:
		with open(data_file, 'r') as file:
			return json.load(file)
	except (FileNotFoundError, json.JSONDecodeError):
		return []


def save_data(data):
	"""Сохранение данных о тренировках в файл."""
	with open(data_file, 'w') as file:
		json.dump(data, file, indent=4)


class TrainingLogApp:
	def __init__(self, root):
		self.root = root
		root.title("Training Journal")
		self.date_entry_label = ttk.Label(self.root, text="Date:")
		self.date_entry = DateEntry(self.root, width=12, background="darkblue", foreground="white", borderwidth=2)
		self.exercise_label = ttk.Label(self.root, text="Exercise:")
		self.exercise_entry = ttk.Entry(self.root)
		self.weight_label = ttk.Label(self.root, text="Weight (kg):")
		self.weight_entry = ttk.Entry(self.root)
		self.repetitions_label = ttk.Label(self.root, text="Repetitions:")
		self.repetitions_entry = ttk.Entry(self.root)
		self.add_button = ttk.Button(self.root, text="Add", command=self.add_entry)
		self.view_button = ttk.Button(self.root, text="View all", command=self.view_records)
		self.create_widgets()

	def create_widgets(self):
		# Виджеты для ввода данных
		self.date_entry_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
		self.date_entry.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
		self.exercise_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
		self.exercise_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)
		self.weight_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
		self.weight_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)
		self.repetitions_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
		self.repetitions_entry.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)
		self.add_button.grid(column=0, row=4, columnspan=2, pady=10)
		self.view_button.grid(column=0, row=5, columnspan=2, pady=10)

	def add_entry(self):
		date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		exercise = self.exercise_entry.get()
		weight = self.weight_entry.get()
		repetitions = self.repetitions_entry.get()

		if not (exercise and weight and repetitions):
			messagebox.showerror("Error", "All fields must be filled!")
			return

		entry = {
			'date': date,
			'exercise': exercise,
			'weight': weight,
			'repetitions': repetitions
		}

		data = load_data()
		data.append(entry)
		save_data(data)

		# Очистка полей ввода после добавления
		self.exercise_entry.delete(0, tk.END)
		self.weight_entry.delete(0, tk.END)
		self.repetitions_entry.delete(0, tk.END)
		messagebox.showinfo("Success", "Exercise has been added!")

	def view_records(self):
		data = load_data()
		records_window = Toplevel(self.root)
		records_window.title("Records")

		tool_box = tk.Frame(records_window)
		tool_box.pack(side=tk.TOP, fill=tk.X, pady=2)

		csv_icon = tk.PhotoImage(file="images/save.png")
		csv_button = tk.Button(tool_box, image=csv_icon)
		csv_button.image = csv_icon
		csv_button.pack(side=tk.LEFT, padx=2)
		self.add_tooltip(csv_button, "Save to csv")

		upload_icon = tk.PhotoImage(file="images/open.png")
		upload_button = tk.Button(tool_box, image=upload_icon)
		upload_button.image = upload_icon
		upload_button.pack(side=tk.LEFT, padx=2)
		self.add_tooltip(upload_button, "Load from csv")

		headings = ["Date", "Exercise", "Weight", "Repetitions"]
		tree = ttk.Treeview(records_window, columns=headings, show="headings")
		for i, j in enumerate(headings):
			tree.heading(j, text=j)
			if i != 0:
				tree.column(j, anchor="center")

		def display_data(filtered_data):
			tree.delete(*tree.get_children())  # Очищаем существующие записи
			for entry in filtered_data:
				tree.insert('', tk.END,
							values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
		display_data(data)

		tree.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=0, padx=2)

		# Создаем фрейм для поисковой строки и фильтров
		filter_frame = tk.Frame(records_window)
		filter_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=0)

		filter_frame.columnconfigure(0, weight=7)
		filter_frame.columnconfigure(1, weight=1)

		search_entry = tk.Entry(filter_frame)
		search_entry.grid(row=0, column=0, sticky="ew", padx=2)

		start_date_entry = DateEntry(filter_frame, width=12, background="darkblue", foreground="white", borderwidth=2)
		start_date_entry.grid(row=0, column=1, sticky="ew", padx=2)

		end_date_entry = DateEntry(filter_frame, width=12, background="darkblue", foreground="white", borderwidth=2)
		end_date_entry.grid(row=0, column=2, sticky="ew", padx=2)

		# Кнопка для применения фильтра
		apply_button = tk.Button(filter_frame, text="Request", command=lambda: apply_filter())
		apply_button.grid(row=0, column=3, sticky="ew", padx=2)

		def apply_filter():
			search_filter = search_entry.get().strip().lower()
			start_date = start_date_entry.get_date()
			end_date = end_date_entry.get_date()

			# Фильтруем данные по упражнению и диапазону дат
			filtered_data = [
				entry for entry in data
				if (not search_filter or search_filter in entry['exercise'].lower())
				   and (start_date <= datetime.strptime(entry['date'], "%Y-%m-%d").date() <= end_date)
			]
			display_data(filtered_data)

	@staticmethod
	def add_tooltip(widget, text):
		"""
			This method creates a `Toplevel` window that appears near the widget when
			the mouse cursor enters the widget's area, displaying the specified tooltip text.
			The tooltip window closes automatically when the mouse cursor leaves the widget area.

			Args:
				widget (tk.Widget): The widget to which the tooltip will be attached.
				text (str): The text to display within the tooltip window.

			Inside the method:
				- `show_tooltip(event)`: A function to create and display the tooltip near the widget.
				- `hide_tooltip(event)`: A function to destroy the tooltip when the mouse leaves the widget area.
		"""
		tooltip = None

		def show_tooltip(event):
			nonlocal tooltip
			if tooltip is not None:
				return
			x = widget.winfo_rootx() + 20
			y = widget.winfo_rooty() + widget.winfo_height() + 5
			tooltip = tk.Toplevel(widget)
			tooltip.wm_overrideredirect(True)
			tooltip.wm_geometry(f"+{x}+{y}")
			label = tk.Label(tooltip, text=text, background='white', relief='solid', borderwidth=1, padx=5, pady=3)
			label.pack()

		def hide_tooltip(event):
			nonlocal tooltip
			if isinstance(tooltip, tk.Toplevel):
				tooltip.destroy()
				tooltip = None

		widget.bind('<Enter>', show_tooltip)
		widget.bind('<Leave>', hide_tooltip)


def main():
	root = tk.Tk()
	app = TrainingLogApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()