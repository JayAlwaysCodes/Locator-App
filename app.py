import phonenumbers
import folium
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from phoneNumber import key

# Replace with your OpenCage API key
key = key

class PhoneNumberDetails(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Phone number input
        self.phone_input = TextInput(
            hint_text="Enter phone number (with country code)",
            multiline=False,
            size_hint=(1, None),  # Width: full, Height: manual
            height=40  # Set a fixed height for the TextInput
        )
        self.layout.add_widget(self.phone_input)

        # Button to trigger tracking
        self.track_button = Button(text="Get Phone Number Details", size_hint=(1, None), height=50)
        self.track_button.bind(on_press=self.track_phone_number)
        self.layout.add_widget(self.track_button)

        return self.layout

    def track_phone_number(self, instance):
        number = self.phone_input.text.strip()

        if not number:
            self.show_popup("Error", "Please enter a valid phone number.")
            return

        try:
            # Parse and get location description
            pepnumber = phonenumbers.parse(number)
            location = geocoder.description_for_number(pepnumber, "en")

            # Get service provider
            service_provider = carrier.name_for_number(phonenumbers.parse(number), "en")

            # Use OpenCage Geocoder to get coordinates
            geocoder_api = OpenCageGeocode(key)
            results = geocoder_api.geocode(location)

            if results and len(results):
                latitude = results[0]['geometry']['lat']
                longitude = results[0]['geometry']['lng']

                # Create a map
                map = folium.Map(location=[latitude, longitude], zoom_start=9)
                folium.Marker([latitude, longitude], popup=location).add_to(map)
                map.save("Location.html")

                # Display results in a popup
                result_text = f"Location: {location}\nService Provider: {service_provider}\nCoordinates: {latitude}, {longitude}"
                self.show_popup("Results", result_text)
            else:
                self.show_popup("Error", "No results found for the location.")
        except Exception as e:
            self.show_popup("Error", f"An error occurred: {str(e)}")

    def show_popup(self, title, message):
        # Create a popup to display results or errors
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, size_hint=(1, 0.8))
        close_button = Button(text="Close", size_hint=(1, None), height=40)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == "__main__":
    PhoneNumberDetails().run()