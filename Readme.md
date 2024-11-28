# Training Journal Application<br>
The Training Journal Application is a desktop application that helps users log, manage, and analyze their training sessions. Built using Tkinter, it provides an intuitive graphical interface for managing workout records, exporting and importing data, and visualizing progress through graphs.<br>

# Features<br>
**1. Add Training Records:**
* Record details like date, exercise name, weight (kg), and repetitions.<br>
* Validates inputs for correct format and completeness.<br>

**2. View Training Records:**
* Display all records in an interactive table.
* Sort records by date for better organization.

**3. Filter and Search:**
* Filter records by date range.
* Search for specific exercises using keywords.

**4. Edit and Delete:**
* Modify existing records directly in the table.
* Delete unwanted records with a simple confirmation dialog.
* 
**5. Save and Load Records:**
* Save records to a JSON file for persistent storage.
* Load records from an existing JSON file.

**6. Import and Export CSV:**
* Import records from a CSV file with matching headers.
* Export current data to a CSV file for external use.

**7. Visualize Progress:**
* Generate a line graph of weight progress for each exercise.

# Installation
```bash
pip install -r requirements.txt
```
**Usage**<br>
1.
```bash
python main.py
```

**2. Add Records:**<br>
* Fill in the date, exercise name, weight, and repetitions.
* Click the "Add" button to save the record.

**3. View Records:**<br>
* Click the "View All" button to see your training records.
* Use the filter and search tools to narrow down your data.

**4. Import/Export Data:**<br>
* Import a CSV file with matching headers to add records.
* Export your current data to a CSV file for external analysis.

**5. Visualize Progress:**<br>
* Generate a line graph to monitor your progress over time.

**6. Edit/Delete Records:**<br>
* Right-click on a row in the table to edit or delete the record.

# Screenshots
**Add Records**

![Alt text](https://raw.githubusercontent.com/asstrix/files/main/TrainingJournal/add.png) 

**View Records**

![Alt text](https://github.com/asstrix/files/blob/dc0c1922bcb7fdc423fe63fa8d76eae1858babc5/TrainingJournal/veiw_records.png) 

**Visualize Progress**

![Alt text](https://raw.githubusercontent.com/asstrix/files/main/TrainingJournal/chart.png) 
