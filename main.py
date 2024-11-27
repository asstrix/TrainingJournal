import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, filedialog
from tkcalendar import DateEntry
import json, csv, os
from datetime import datetime


class TrainingLogApp:
	def __init__(self, root):
		self.root = root
		root.title("Training Journal")
		root.geometry(f"{300}x{200}+{(root.winfo_screenwidth() - 300) // 4}+{(root.winfo_screenheight() - 200) // 3}")

		self.data_file = None
		self.data = []
		self.date_entry_label = ttk.Label(self.root, text="Date:")
		self.date_entry = DateEntry(
			self.root, width=12, borderwidth=2, date_pattern="dd.mm.yyyy",
			background="darkgrey",
			foreground="black",
			headersbackground="grey",
			headersforeground="black",
			selectbackground="green",
			selectforeground="white"
		)
		self.exercise_label = ttk.Label(self.root, text="Exercise:")
		self.exercise_entry = ttk.Entry(self.root)
		self.weight_label = ttk.Label(self.root, text="Weight (kg):")
		self.weight_entry = ttk.Entry(self.root)
		self.repetitions_label = ttk.Label(self.root, text="Repetitions:")
		self.repetitions_entry = ttk.Entry(self.root)
		self.tool_box = tk.Frame(self.root)
		self.view_button = ttk.Button(self.tool_box, command=self.view_records)
		self.create_widgets()

	def create_widgets(self):
		self.root.grid_columnconfigure(1, weight=1)
		self.tool_box.grid(column=0, row=0, sticky='ew', padx=5, pady=1)
		self.date_entry_label.grid(column=0, row=1, sticky='ew', padx=5, pady=1)
		self.date_entry.grid(column=1, row=1, sticky='ew', padx=5, pady=1)
		self.exercise_label.grid(column=0, row=2, sticky='ew', padx=5, pady=1)
		self.exercise_entry.grid(column=1, row=2, sticky='ew', padx=5, pady=1)
		self.weight_label.grid(column=0, row=3, sticky='ew', padx=5, pady=1)
		self.weight_entry.grid(column=1, row=3, sticky='ew', padx=5, pady=1)
		self.repetitions_label.grid(column=0, row=4, sticky='ew', padx=5, pady=1)
		self.repetitions_entry.grid(column=1, row=4, sticky='ew', padx=5, pady=1)

		add_button = ttk.Button(self.root, text="Add", width=5, command=self.add_entry)
		add_button.grid(column=1, row=5, pady=1)

		view_button_icon = tk.PhotoImage(file="images/view.png")
		self.view_button.config(image=view_button_icon, state='disabled')
		self.view_button.image = view_button_icon
		self.view_button.pack(side=tk.LEFT)
		self.add_tooltip(self.view_button, 'View all')

		open_button_icon = tk.PhotoImage(file="images/open.png")
		open_button = ttk.Button(self.tool_box, image=open_button_icon, command=self.open_file)
		open_button.image = open_button_icon
		self.add_tooltip(open_button, "Open JSON")
		self.view_button.pack(side=tk.LEFT)
		open_button.pack(side=tk.LEFT)

	def add_entry(self):
		date = self.date_entry.get()
		exercise = self.exercise_entry.get()
		weight = self.weight_entry.get()
		repetitions = self.repetitions_entry.get()
		if not (exercise and weight and repetitions):
			messagebox.showerror("Error", "All fields must be filled!")
			return
		try:
			weight, repetitions = map(int, (weight, repetitions))
		except ValueError:
			messagebox.showerror("Error", "Weight and Repetitions fields must be integers!")
			return

		entry = {
			'date': date,
			'exercise': exercise,
			'weight': weight,
			'repetitions': repetitions
		}
		if self.data_file:
			self.data = self.load_data()
		self.data.append(entry)
		self.save_data()

		# Очистка полей ввода после добавления
		self.exercise_entry.delete(0, tk.END)
		self.weight_entry.delete(0, tk.END)
		self.repetitions_entry.delete(0, tk.END)
		messagebox.showinfo("Success", "Exercise has been added!")

	def open_file(self):
		file_path = filedialog.askopenfilename(
			title="Select a JSON file",
			filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
		)
		self.data_file = file_path
		self.view_records()
		self.view_button.config(state='enabled')

	def load_data(self):
		with open(self.data_file, 'r') as file:
			return json.load(file)

	def save_data(self):
		if not self.data_file:
			self.data_file = 'training_journal.json'
		with open(self.data_file, 'w') as file:
			json.dump(self.data, file, indent=4)

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

	def view_records(self):
		def display_data(data_):
			table.delete(*table.get_children())
			for entry in data_:
				table.insert(
					'', tk.END,
					values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions'])
				)

		def apply_filter():
			search = search_entry.get().strip().lower()
			start_date = start_date_entry.get_date()
			end_date = end_date_entry.get_date()
			filtered_data = [entry for entry in self.data
							 if ('*' in search or not search or search in entry['exercise'].lower())
							 and (start_date <= datetime.strptime(entry['date'], "%d.%m.%Y").date() <= end_date)
							 ]
			display_data(filtered_data)
			search_entry.delete(0, tk.END)

		def import_from_csv():
			try:
				file_path = filedialog.askopenfilename(
					title="Select a CSV file",
					filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
				)
				if not file_path:
					return
				with open(file_path, mode="r", encoding="utf-8") as file:
					reader = csv.reader(file)
					headers = next(reader, None)  # Первая строка - заголовки
					tree_headers = [table.heading(col)["text"] for col in table["columns"]]
					if headers != tree_headers:
						messagebox.showerror("Error", "CSV headers do not match Treeview headers.")
						return
					for row in reader:
						table.insert("", "end", values=row)
				messagebox.showinfo("Success", f"Data successfully loaded from {file_path}!")
			except Exception as e:
				messagebox.showerror("Error", f"An error occurred: {e}")

		def export_to_csv(training_list):
			try:
				file_path = filedialog.asksaveasfilename(
					title="Save as",
					defaultextension=".csv",
					filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
				)
				if not file_path:
					return
				data_ = []
				for row_id in training_list.get_children():
					row = training_list.item(row_id)['values']
					data_.append(row)
				if not data_:
					messagebox.showinfo("Info", "No data to export.")
					return
				headers = [training_list.heading(col)["text"] for col in training_list["columns"]]
				with open(file_path, mode="w", newline="", encoding="utf-8") as file:
					writer = csv.writer(file)
					writer.writerow(headers)
					writer.writerows(data_)
			except Exception as e:
				messagebox.showerror("Error", f"An error occurred: {e}")

		def create_context_menu(tree):
			menu = tk.Menu(tree, tearoff=0)
			edit_image = tk.PhotoImage(file="images/edit.png")
			delete_image = tk.PhotoImage(file="images/delete.png")

			edit_label = None
			delete_label = None

			def edit_row(row_id=None):
				"""Редактирует выбранную строку."""
				selected_row = row_id if row_id else tree.selection()
				if not selected_row:
					messagebox.showwarning("No selection", "Please select a row to edit.")
					return

				current_values = tree.item(selected_row, "values")
				column_names = tree["columns"]

				edit_window = tk.Toplevel()
				edit_window.title("Edit exercise")
				edit_window.geometry(f"{400}x{200}+{(edit_window.winfo_screenwidth() - 400) // 2}+{(edit_window.winfo_screenheight() - 200) // 2}")

				entry_widgets = []
				for idx, value in enumerate(current_values):
					tk.Label(edit_window, text=f"{column_names[idx]}:").grid(row=idx, column=0, padx=10, pady=5,
																			 sticky="w")
					entry = tk.Entry(edit_window, width=30)
					entry.insert(0, value)
					entry.grid(row=idx, column=1, padx=10, pady=5)
					entry_widgets.append(entry)

				def save_changes():
					new_values = [k.get() for k in entry_widgets]
					tree.item(selected_row, values=new_values)
					ind_row = tree.index(selected_row)
					self.data[ind_row] = {
						"date": new_values[0],
						"exercise": new_values[1],
						"weight": new_values[2],
						"repetitions": new_values[3],
					}
					self.save_data()
					edit_window.destroy()

				ttk.Button(edit_window, text="Save", command=save_changes).grid(
					row=len(current_values), column=0, columnspan=2, pady=10
				)

			def delete_row(row_id=None):
				selected_item = row_id if row_id else tree.selection()
				if not selected_item:
					messagebox.showwarning("No selection", "Please select a row to delete.")
					return

				confirm = messagebox.askyesno("Delete Row", "Are you sure you want to delete the selected row?")
				if confirm:
					row_index = tree.index(selected_item)
					tree.delete(selected_item)
					del self.data[row_index]
					self.save_data()

			def show_hover_icons(event):
				nonlocal edit_label, delete_label

				row_id = tree.identify_row(event.y)
				col_id = tree.identify_column(event.x)

				if row_id and col_id == f"#{len(tree['columns'])}":
					bbox = tree.bbox(row_id, col_id)
					if bbox:
						x, y, width, height = bbox
						destroy_hover_icons()

						edit_label = tk.Label(tree, image=edit_image, cursor="hand2")
						edit_label.place(x=x + width - 50, y=y, width=20, height=20)
						edit_label.bind("<Button-1>", lambda e: edit_row(row_id))

						delete_label = tk.Label(tree, image=delete_image, cursor="hand2")
						delete_label.place(x=x + width - 25, y=y, width=20, height=20)
						delete_label.bind("<Button-1>", lambda e: delete_row(row_id))
				else:
					destroy_hover_icons()

			def destroy_hover_icons():
				nonlocal edit_label, delete_label
				if isinstance(edit_label, tk.Label):
					edit_label.destroy()
					edit_label = None
				if isinstance(delete_label, tk.Label):
					delete_label.destroy()
					delete_label = None

			def context_menu(event):
				row = tree.identify_row(event.y)
				if row:
					tree.selection_set(row)
					menu.post(event.x_root, event.y_root)

			def on_double_click(event):
				row_id = tree.identify_row(event.y)
				if row_id:
					tree.selection_set(row_id)
					edit_row(row_id)

			def on_delete_key(event):
				selected_row = tree.selection()
				if selected_row:
					delete_row(selected_row)

			menu.add_command(label="Edit", command=lambda: edit_row())
			menu.add_command(label="Delete", command=lambda: delete_row())

			tree.bind("<Button-3>", context_menu)
			tree.bind("<Motion>", show_hover_icons)
			tree.bind("<Double-1>", on_double_click)
			tree.bind("<Delete>", on_delete_key)
			tree.bind("<Leave>", lambda e: destroy_hover_icons())

		self.data = self.load_data()
		records_window = Toplevel(self.root)
		records_window.title("Records")
		records_window.geometry(f"{800}x{300}+{(records_window.winfo_screenwidth() - 800) // 2}+{(records_window.winfo_screenheight() - 300) // 2}")

		records_window.grid_columnconfigure(0, weight=1)
		records_window.grid_rowconfigure(1, weight=1)
		records_window.grid_rowconfigure(2, weight=0)

		tool_box = tk.Frame(records_window)
		tool_box.grid(row=0, column=0, sticky="ew", padx=1, pady=(0, 5))

		import_icon = tk.PhotoImage(file="images/import.png")
		import_button = tk.Button(tool_box, image=import_icon, command=lambda: import_from_csv())
		import_button.image = import_icon
		import_button.pack(side=tk.LEFT, padx=2)
		self.add_tooltip(import_button, "Import from csv")

		export_icon = tk.PhotoImage(file="images/export.png")
		export_button = tk.Button(tool_box, image=export_icon, command=lambda: export_to_csv(table))
		export_button.image = export_icon
		export_button.pack(side=tk.LEFT, padx=2)
		self.add_tooltip(export_button, "Export to csv")

		file_name_label = tk.Label(tool_box, text="File name:", font=("Arial", 10, "bold"))
		file_name_value = tk.Label(tool_box, text=os.path.basename(self.data_file))
		rows_label = tk.Label(tool_box, text=f"Rows:", font=("Arial", 10, "bold"))
		rows_value = tk.Label(tool_box, text=len(self.load_data()))
		rows_value.pack(side=tk.RIGHT)
		rows_label.pack(side=tk.RIGHT)
		file_name_value.pack(side=tk.RIGHT)
		file_name_label.pack(side=tk.RIGHT)

		headings = ["Date", "Exercise", "Weight", "Repetitions"]
		table = ttk.Treeview(records_window, columns=headings, show="headings")
		for i, j in enumerate(headings):
			table.heading(j, text=j)
			if i != 0:
				table.column(j, anchor="center")

		display_data(self.data)
		table.grid(row=1, column=0, sticky="nsew", padx=1, pady=(2, 0))
		create_context_menu(table)

		filter_frame = tk.Frame(records_window)
		filter_frame.grid(row=2, column=0, sticky="ew", padx=1, pady=(0, 2))
		filter_frame.columnconfigure(0, weight=7)
		filter_frame.columnconfigure(1, weight=1)
		search_entry = tk.Entry(filter_frame)
		search_entry.grid(row=2, column=0, sticky="ew", padx=1, pady=(0, 2))
		start_date_entry = DateEntry(
			filter_frame,
			width=12, borderwidth=2, date_pattern="dd.mm.yyyy",
			background="darkgrey",
			foreground="black",
			headersbackground="grey",
			headersforeground="black",
			selectbackground="green",
			selectforeground="white"
		)
		start_date_entry.grid(row=2, column=1, sticky="ew", padx=0, pady=(0, 2))
		end_date_entry = DateEntry(
			filter_frame,
			width=12, borderwidth=2, date_pattern="dd.mm.yyyy",
			background="darkgrey",
			foreground="black",
			headersbackground="grey",
			headersforeground="black",
			selectbackground="green",
			selectforeground="white"
		)
		end_date_entry.grid(row=2, column=2, sticky="ew", padx=0, pady=(0, 2))
		apply_button = tk.Button(filter_frame, text="Request", command=lambda: apply_filter())
		apply_button.grid(row=2, column=3, sticky="ew", padx=2, pady=(2, 2))


def main():
	root = tk.Tk()
	app = TrainingLogApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()
