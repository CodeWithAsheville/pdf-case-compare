# About pdf-case-compare
The pdf-case-compare project originated as a request to Code for Asheville, to help a non-profit legal aid organization, which was helping people get their records expunged per North Carolina law.

The resulting Python program compares two PDF report files, one generated through the LexisNexis Public Records database, and the other through the North Carolina Criminal and Infraction Public Records Search (CIPRS) database.

The program identifies court cases that are found in the LexisNexis PDF file, but which do not seem to appear in the CIPRS PDF file.

The output report is shown on the screen, as well as sent to a text file. 

The Python program, with a Windows 10 GUI (via PyQt5), is delivered as a stand-alone desktop EXE app using pyinstaller.

## Setup Notes:
1. Python code was tested using Python 3.9 under Ubuntu 20.04
2. Libraries installed:
 - PyQt5: Windows 10 GUI library  
`$pip3 install PyQt5`
 - PyMuPDF: PDF extraction program (aka fitz)  
`$pip3 install fitz`
 - pyinstaller: Windows 10 packaging-to-exe program  
`$pip3 install pyinstaller`
3. You must run pyinstaller on the platform you are delivering to. So, in this case, since the client needed the EXE file to run under Windows 10, I had to run pyinstaller from Windows 10. Note: the PisgahPDFComp.spec was created by pyinstaller, not me, so is not necessary to creating the EXE. The only options I used were given in the command line:  
`$pyinstaller --name PisgahPDFComp --onefile --noconsole  main.py`

For a good introduction to using PyQt5 and pyinstaller, read:
<https://medium.com/analytics-vidhya/how-to-build-your-first-desktop-application-in-python-7568c7d74311>

Some peculiarities you need to know:

- pisgah_pdf.py is the testing version for the non-GUI part of the code. The program assumes that the files to be compared, "Lexis.pdf" and "CIPRS.pdf", are already in the same subdirectory as pisgah_pdf.py. pisgay_pdf.py lets me unit test the file_comparison code, which will be later imported into the pisgah_gui.py program (under main.py). In this way, we could work on the GUI independently of the file_comparison portions of the code.

- main.py is the program that I ran under Linux Python3 via Visual Studio Code. This code, by default, puts the "comparison.txt" file in the same subdirectory as the EXE file, which is what we want for the final delivered product. However, this means that when testing the program, I got an error message that I didn't have write access to "/bin" (or in Windows 10, the output was sent to an obscure Python subdirectory). So for testing, I would need to specify the entire path for the comparison.txt output file in the field shown on the screen. The field needed the full path name, without quotes (even if there are spaces), and without the ".txt" extension (which is added later).

- after unit testing file_comparison via pisgah_pdf.py, the GUI was tested using main.py.

- After testing the interface, I left Linux and switched to Windows 10 to run pyinstaller. I need to be running Python in the operating system of the desired delivery platform, in this case, Windows 10.
 
- WARNING: I did try running pyinstaller with an icon file (ico) I created, so the app would have its own icon, but I got too many virus warnings, so I took out the icon and used the default Python icon.
 
- I used the site https://www.virustotal.com/ to make sure there weren't any known viruses in the app's EXE file.

- WARNING: The EXE file is large (approx. 40MB), which means I couldn't email it. Also, Google Drive balked at letting me share an EXE file. So I ended up using DropBox to deliver the package to the client.
