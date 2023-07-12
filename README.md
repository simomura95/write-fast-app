# Write fast app
A GUI app to force fast writing: if no input is given for 5 seconds, all text is deleted (but it's possible to save results). Done with Custom TKinter for a more beautiful design.<br>
It's also possible to switch between light and dark mode.

![fast-writing](https://github.com/simomura95/write-fast-app/assets/134875169/482e9d18-560b-48f7-8c19-7f7387fd489d)

There is a placeholder on the textbox to tell the user to start typing; when the user clicks on the box, the placeholder is deleted.
It comes back if the cursor is moved out of the box without having typed anything, and the focus is lost too.

When the user starts typing, the timer is shown on the bottom of the app and is reset to 5 whenever a new character is typed.<br>
If it reaches 0, a CTk messagebox pops up asking the user if he wants to start over and if results are to be saved.
If so, a new folder is created in the same directory of the app and the text is saved in a .txt file.
The file contains the current time in its name, so a file previously created is never overwritten.
