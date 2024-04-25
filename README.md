# Event Mapper

### Developed by : Rajdeep, Raagam Parmar and Souransu Roy

<br>

### About

Our application provides a convenient way to manage the events taking place in IIT-Palakkad, making use of the campus's map.

There are two modes available : Visitor and Organizer. <br>
The Visitor mode allows users to take a look at the various events that are taking place in the campus.<br>
The Organizer mode allows users to add or remove events at various locations, on top of the functionality that the visitors have.

<br>

### How to use

The application starts with a home page, prompting the user to choose one of the two modes : Visitor or Organizer

<b> Visitor: </b><br>
The campus's map is displayed on the screen. The user is free to interact with the map. They can pan it, rotate it and zoom in and out of it as per their convenience. Various pre-defined locations are clickable on the map. Users can click on any of the locations' buttons to open a pop-up window that displays all events taking place at that location, sorted by their date and time. A short description of the event is displayed as well.
The reset button resets the map and the home button takes the user back to the starting page.

<b> Organizer: </b><br>
Clicking on the Organizer button on the home page opens up a login page. The `i` button on the top-right corner opens a pop-up that displays the rules for making a new username or password. The login page has options to log in or sign up. Only the encrypted passwords are stored. The user can either sign in with valid credentials, or sign up with new credentials. This leads them to the map page.<br>
This map page has additional features to enable the organizer to manage events. Clicking on one of the pre-defined locations opens up a pop-up window. At the top is a button for the user to add a new event. Clicking on the button opens a form, where the user is prompted to add information about the event that they want to define, namely the event name, date, time and a short description. Only event names that don't already exist can be defined. A validation is performed on the entered date and time, and the new event is added to the list of events. Events that the user is organizing are displayed below the "Add event" button, sorted by their date and time. The user has an option to remove each of these events. Below these events, the other events being organized at the venue are displayed, along with information about their date and time and a short description. These events are sorted by their date and time as well.
The reset button resets the map and the logout button logs the user out and takes them back to the home page.

<br>

### Implementation details

- We have used the Python based module, Kivy, for developing our GUI.
- For encryption the passwords, the SHA512 function has been used.
- Dictionaries have been used to implement hash tables on the events to enable fast look-ups.
- Input validation has been performed on all text inputs.
