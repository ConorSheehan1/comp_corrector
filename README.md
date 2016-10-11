# CompCorrector
#### Usage:
1. Choose the download all option for a practical on moodle (returns single zip)
2. Copy the path to the zip or use the open button to select the zipfile
3. Copy names you are assigned from google sheets file
4. Hit start


##
* Input: A path to a zip file and a list of string seperated by "\n" 
* Output: 
    * All folders in zip starting with names specified are extracted
	* Files in the resulting folders are renamed with the prefix of the name of the folder.
 		* For example: Path = **C:/test**, Subdir = **C:/test/name**
 		* Files in **C:/test/name** will change to **C:/test_name**
 		* e.g **C:/test/name/p1p1.py** will change **to C:/test/name_p1p1.py**
 	* Option to remove empty folders after move
 	* The main zip will not be removed, in case you want to check all relevant files have been extracted
 	
#### To run either:
* Run ui.py
* Run src/main.py and edit (not recommended)
