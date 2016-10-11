# CompCorrector
#### Usage:
Choose download all option for practical on moodle
Copy names you are assigned from google sheets file

* Input: A path to a zip file 
* Output: 
    * All folders in zip starting with names specified are extracted
	* Files in the resulting folders are renamed with the prefix of the name of the folder.
 		* For example: Path = **C:/test**, Subdir = **C:/test/name**
 		* Files in **C:/test/name** will change to **C:/test_name**
 		* e.g **C:/test/name/p1p1.py** will change **to C:/test/name_p1p1.py**
 	* Option to remove empty folders after move
 	
#### To run either:
* Run ui.py
* Run src/main.py to bypass ui
