import hashlib
from functools import partial

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.metrics import dp


# Some global variables

buttons_names = ["Agora", "Samgatha", "Manogatha", "Main Parking", "Kaapi", "Bageshri", "Shikharam", "Tilang Parking", "Tilang A", "Tilang B", "Brindavani"]

current_username = "rajdeep"


def is_leap(year):
    return year%400 == 0 or (year%4 ==0 and year%100 != 0)


def comparison_function(input_list):
    return input_list[-1]


class MyLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.cols = 1
        
        # This is for demonstration purposes only.
        # Demo part : Start

        self.button_dict = {name:Button(text = name, font_size = 20, on_press = partial(self.location_button_pressed, name)) for name in buttons_names}

        for sample_button in self.button_dict.values():
            sample_button.size_hint_y = 1/len(self.button_dict)
            self.add_widget(sample_button)

        # Demo part : End
    
    def modify_label_string(self, string, k, substring):
        # Adds substring after every k characters
        output_string = ""
        index_counter = 0
        while len(string[index_counter:]) >= k:
            output_string += string[index_counter:index_counter+k] + substring
            index_counter += k
        output_string += string[index_counter:]
        return output_string

    def remove_button_pressed(self, *args): # Initiates the popup
        self.confirmation_popup = Popup(title = "Confirmation", size = (dp(400), dp(200)), size_hint = (None, None))
        confirmation_layout = GridLayout(cols = 1)
        confirmation_layout.add_widget(Label(text = "Are you sure?", font_size = 25))
        buttons_grid = GridLayout(cols = 2)
        buttons_grid.add_widget(Button(text = "Yes", on_release = partial(self.remove_event, *args), font_size = 22))
        buttons_grid.add_widget(Button(text = "No", on_release = self.confirmation_popup.dismiss, font_size = 22))
        confirmation_layout.add_widget(buttons_grid)
        self.confirmation_popup.content = confirmation_layout
        self.confirmation_popup.open()

    
    def remove_event(self, *args):
        self.confirmation_popup.dismiss()
        event_name = args[0]
        current_location = args[1]
        
        # Handling the events file
        
        with open("events.txt", "r") as events_file:
            data = events_file.read().split("\n")
        
        updated_events = "\n".join(entry for entry in data if entry.split("||")[0] != event_name)

        with open("events.txt", "w") as events_file:
            events_file.write(updated_events)
        
        self.event_list_popup.dismiss()
        self.location_button_pressed(current_location)

    
    def add_new_event(self, *args):
        self.new_event_popup = Popup(title = "New Event", size = (dp(550), dp(500)), size_hint = (None, None))
        self.popup_layout = GridLayout(cols = 2)
        
        self.popup_layout.add_widget(Label(text = "Event name", font_size = 20))
        self.name_input = TextInput(multiline = False, font_size = 20)
        self.name_input.bind(text = self.validate_name_input)
        self.popup_layout.add_widget(self.name_input)
        self.popup_layout.add_widget(Label(text = "Date (DD/MM/YYYY)", font_size = 20))
        self.date_input = TextInput(multiline = False, font_size = 20)
        self.date_input.bind(text = self.validate_date_input)
        self.popup_layout.add_widget(self.date_input)
        self.popup_layout.add_widget(Label(text = "Time (HH:MM)", font_size = 20))
        self.time_input = TextInput(multiline = False, font_size = 20)
        self.time_input.bind(text = self.validate_time_input)
        self.popup_layout.add_widget(self.time_input)
        self.popup_layout.add_widget(Label(text = "Description", font_size = 20))
        self.description_input = TextInput(multiline = False, font_size = 20)
        self.description_input.bind(text = self.validate_description_input)
        self.popup_layout.add_widget(self.description_input)
        
        self.popup_layout.add_widget(Button(text = "Add Event", on_release = partial(self.new_event_submission, *args), font_size = 20))
        self.popup_layout.add_widget(Button(text = "Cancel", on_release = self.new_event_popup.dismiss, font_size = 20))

        self.new_event_popup.content = self.popup_layout
        self.new_event_popup.open()

    def error_popup(self, error_message):
        Popup(title = "Error", content = Label(text = error_message, font_size = 28), size = (dp(450), dp(250)), size_hint = (None, None)).open()

    def new_event_submission(self, *args):
        venue = args[0]
        name, date, time, description = self.name_input.text, self.date_input.text, self.time_input.text, self.description_input.text
        # Input Validation here
        if not (name and date and time and description):
            self.error_popup("Please fill all entries")
        else:
            # Date validation
            if len(date) != 10:
                self.error_popup("Invalid date")
            else:
                get_date, get_month, get_year = int(date[:2]), int(date[3:5]), int(date[6:])
                days_in_month = [31, 28 + is_leap(get_year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                if get_month > 12 or get_date > days_in_month[get_month-1]:
                    self.error_popup("Invalid date")
                else:
                    # Time validation
                    if len(time) != 5:
                        self.error_popup("Invalid time")
                    else:
                        get_hours, get_minutes = int(time[:2]), int(time[3:])
                        if get_hours > 24 or get_minutes > 60:
                            self.error_popup("Invalid time")
                        else:
                            with open("events.txt", "r") as events_file:
                                events_list = [entry.split("||")[0] for entry in events_file.read().split("\n") if entry]
                            if name.strip() in events_list:
                                self.error_popup("Event name taken")
                            else:
                                with open("events.txt", "a") as events_file:
                                    events_file.write(name + "||" + "|".join([venue, current_username, date + " " + time, description]) + "\n")
                                self.new_event_popup.dismiss()
                                self.event_list_popup.dismiss()
                                self.location_button_pressed(venue)

    def validate_name_input(self, instance, value):
        if self.name_input.text[-1:] == "|":
            self.name_input.text = self.name_input.text[:-1]
    
    def validate_date_input(self, instance, value):
        current_length = len(self.date_input.text)
        digits = "0123456789"
        if current_length <= 2:
            if self.date_input.text[-1:] not in digits:
                self.date_input.text = self.date_input.text[:-1]
        elif current_length == 3:
            if self.date_input.text[-1] != "/":
                self.date_input.text = self.date_input.text[:-1]
        elif current_length <= 5:
            if self.date_input.text[-1] not in digits:
                self.date_input.text = self.date_input.text[:-1]
        elif current_length == 6:
            if self.date_input.text[-1] != "/":
                self.date_input.text = self.date_input.text[:-1]
        elif current_length <= 10:
            if self.date_input.text[-1] not in digits:
                self.date_input.text = self.date_input.text[:-1]
        else:
            self.date_input.text = self.date_input.text[:10]


    def validate_time_input(self, instance, value):
        current_length = len(self.time_input.text)
        digits = "0123456879"
        if current_length <= 2:
            if self.time_input.text[-1:] not in digits:
                self.time_input.text = self.time_input.text[:-1]
        elif current_length == 3:
            if self.time_input.text[-1] != ":":
                self.time_input.text = self.time_input.text[:-1]
        elif current_length <= 5:
            if self.time_input.text[-1] not in digits:
                self.time_input.text = self.time_input.text[:-1]
        else:
            self.time_input.text = self.time_input.text[:-1]


    def validate_description_input(self, instance, value):
        if self.description_input.text[-1:] == "|":
            self.description_input.text = self.description_input.text[:-1]

    def location_button_pressed(self, *args):
        location_name = args[0]
        
        # Handling the popup
        # Format of events_dict : {<event name>:[<location name>,<organizer username>,<DD.MM.YY hh:mm>,<Description>]}

        # Place for layout code

        events_dict = self.obtain_events(location_name)

        layout = GridLayout(cols = 1, size_hint_y = None) # The main layout inside the popup
        layout.bind(minimum_height = layout.setter("height"))
        
        events_by_user = {event:events_dict[event] for event in events_dict if events_dict[event][1] == current_username}
        events_not_by_user = {event:events_dict[event] for event in events_dict if event not in events_by_user}

        events_by_user = self.sort_events(events_by_user)
        events_not_by_user = self.sort_events(events_not_by_user)

        

        if current_username:
            layout.add_widget(Button(text = "Add event", font_size = 28, size = (dp(550), dp(100)), size_hint = (None, None), on_release = partial(self.add_new_event, location_name)))

        for event_name in events_by_user:
            layout.add_widget(Label(text = event_name, font_size = 24, size = (dp(550), dp(100)), size_hint = (None, None)))
            layout.add_widget(Button(text = "Remove above event", on_release = partial(self.remove_button_pressed, event_name, location_name), font_size = 22, size = (dp(550), dp(100)), size_hint = (None, None)))
        
        for event_name in events_not_by_user:
            layout.add_widget(Label(text = event_name, font_size = 24, size = (dp(550), dp(100)), size_hint = (None, None)))

        scroll = ScrollView()
        scroll.add_widget(layout)
        
        self.event_list_popup = Popup(title = location_name, content = scroll, size_hint = (None, None), size = (dp(550), dp(600)))
        self.event_list_popup.open()

        
        
        
    def sort_events(self, events_dict):
        if len(events_dict) == 0:
            return events_dict
        
        # Handling non empty inputs
        # Format of entries of events_list : [event_name, DD, MM, YYYY, hh, mm]
        events_list = []
        for event in events_dict:
            date_full, time_full = events_dict[event][2].split(" ")
            date = int(date_full[:2])
            month = int(date_full[3:5])
            year = int(date_full[-4:])

            days_in_months = [31, 28 + is_leap(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            hour = int(time_full[:2])
            minute = int(time_full[-2:])

            coordinate = (sum(365 + is_leap(year) for i in range(year)) + sum(days_in_months[i] for i in range(month-1)) + date - 1)*14400 + 60*(hour-1) + minute

            events_list.append([event, coordinate])
        
        events_list.sort(key = comparison_function)
        output_dict = {event[0]:events_dict[event[0]] for event in events_list}
        
        return output_dict

    
    def obtain_events(self, venue): # Returns a dictionary for events being organized at venue
        with open("events.txt", "r") as events_file:
            data = [entry for entry in events_file.read().split("\n") if entry]

        output_dict = {}

        for entry in data:
            event_name, other = entry.split("||")
            extracted_data = other.split("|")
            if extracted_data[0] == venue:
                output_dict[event_name] = extracted_data
        
        return output_dict


class MyApp(App):
    def build(self):
        return MyLayout()


MyApp().run()