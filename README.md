## Requirements
python3

## How to
Run ui.py. You should see the interface below:
![UI image](images/UI.PNG)

1. Click <kbd>choose zip</kbd> to use the default OS file chooser, or enter the path to your zip directly
2. Paste the names of the students you need to correct into the **list of names** field  
 **(If no names are included, all files in the zip will be extracted)**
3. Choose your preferences
4. Click <kbd>start</kbd>

## Preferences
1. **remove zips** removes zip files submitted by students will be deleted once all files within them have been extracted. The main zip (chosen using the <kbd>choose zip</kbd> button) will never be removed.
2. **compile files** uses gcc to compile files and give them the same name as their source file. This feature only works with C files currently.
3. **safe mode** creates a new folder called safe and copies the main zip to it before running anything.
 
