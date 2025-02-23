from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import mysql.connector

Window.clearcolor = (1, 1, 1, 1)  # Set background color to white

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="electricity_subscribers"
        )
        self.create_layout()

    def create_layout(self):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Title label
        label = Label(text="Electricity Subscribers Management System", size_hint=(1, 0.1), color=(0, 0, 1, 1), font_size=24, bold=True)
        layout.add_widget(label)

        # Add subscriber button
        add_subscriber_button = Button(text="Add Subscriber", size_hint=(1, 0.1), background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        add_subscriber_button.bind(on_press=lambda instance: self.add_subscriber())
        layout.add_widget(add_subscriber_button)

        # View subscribers button
        view_subscribers_button = Button(text="View All Subscribers", size_hint=(1, 0.1), background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        view_subscribers_button.bind(on_press=lambda instance: self.view_subscribers())
        layout.add_widget(view_subscribers_button)

        # Add subscription button
        add_subscription_button = Button(text="Add Subscription", size_hint=(1, 0.1), background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        add_subscription_button.bind(on_press=lambda instance: self.add_subscription())
        layout.add_widget(add_subscription_button)

        # View subscriptions button
        view_subscriptions_button = Button(text="View All Subscriptions", size_hint=(1, 0.1), background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        view_subscriptions_button.bind(on_press=lambda instance: self.view_subscriptions())
        layout.add_widget(view_subscriptions_button)

        # Search by meter number button
        search_by_meter_number_button = Button(text="Search by Meter Number", size_hint=(1, 0.1), background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        search_by_meter_number_button.bind(on_press=lambda instance: self.search_by_meter_number())
        layout.add_widget(search_by_meter_number_button)

        # Exit button
        exit_button = Button(text="Exit", size_hint=(1, 0.1), background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        exit_button.bind(on_press=lambda instance: self.exit())
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def add_subscriber(self):
        # Create a popup for adding subscriber information
        popup_layout = BoxLayout(orientation="vertical", spacing=10)

        # Input fields
        name_input = TextInput(hint_text="Enter subscriber's name", multiline=False, size_hint=(1, 0.1))
        address_input = TextInput(hint_text="Enter subscriber's address", multiline=False, size_hint=(1, 0.1))
        phone_number_input = TextInput(hint_text="Enter subscriber's phone number", multiline=False, size_hint=(1, 0.1))
        meter_number_input = TextInput(hint_text="Enter subscriber's meter number", multiline=False, size_hint=(1, 0.1))

        # Add input fields to popup layout
        popup_layout.add_widget(name_input)
        popup_layout.add_widget(address_input)
        popup_layout.add_widget(phone_number_input)
        popup_layout.add_widget(meter_number_input)

        # Add button to submit subscriber information
        submit_button = Button(text="Add Subscriber", size_hint=(1, 0.1), background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        popup_layout.add_widget(submit_button)

        # Create the popup
        popup = Popup(title="Add Subscriber", content=popup_layout, size_hint=(0.8, 0.8))
        popup.open()

        # Bind submit button to add subscriber to database
        submit_button.bind(on_press=lambda x: self.submit_subscriber(name_input.text, address_input.text, phone_number_input.text, meter_number_input.text, popup))

    def submit_subscriber(self, name, address, phone_number, meter_number, popup):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO subscribers (name, address, phone_number, meter_number) VALUES (%s, %s, %s, %s)", (name, address, phone_number, meter_number))
        self.connection.commit()
        cursor.close()
        popup.dismiss()
        print("Subscriber added successfully!")

    def view_subscribers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM subscribers")
        subscribers = cursor.fetchall()
        cursor.close()

        popup_layout = BoxLayout(orientation="vertical", spacing=10)

        for subscriber in subscribers:
            subscriber_info_label = Label(text=f"Name: {subscriber[1]}\nAddress: {subscriber[2]}\nPhone Number: {subscriber[3]}\nMeter Number: {subscriber[4]}", color=(1, 1, 1, 1), font_size=16)
            popup_layout.add_widget(subscriber_info_label)

        Popup(title="All Subscribers", content=popup_layout, size_hint=(0.8, 0.8)).open()

    def add_subscription(self):
        popup_layout = BoxLayout(orientation="vertical", spacing=10)

        subscribers = self.get_subscribers()
        subscriber_spinner = Spinner(text="Select subscriber", values=subscribers, size_hint=(1, 0.1))
        popup_layout.add_widget(subscriber_spinner)

        issue_date_input = TextInput(hint_text="Enter issue date (YYYY-MM-DD)", multiline=False, size_hint=(1, 0.1))
        due_date_input = TextInput(hint_text="Enter due date (YYYY-MM-DD)", multiline=False, size_hint=(1, 0.1))
        amount_input = TextInput(hint_text="Enter amount", multiline=False, size_hint=(1, 0.1))
        payment_status_input = Spinner(text="Select payment status", values=["Paid", "Unpaid"], size_hint=(1, 0.1))

        popup_layout.add_widget(issue_date_input)
        popup_layout.add_widget(due_date_input)
        popup_layout.add_widget(amount_input)
        popup_layout.add_widget(payment_status_input)

        submit_button = Button(text="Add Subscription", size_hint=(1, 0.1), background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        popup_layout.add_widget(submit_button)

        popup = Popup(title="Add Subscription", content=popup_layout, size_hint=(0.8, 0.8))
        popup.open()

        submit_button.bind(on_press=lambda x: self.submit_subscription(subscriber_spinner.text, issue_date_input.text, due_date_input.text, amount_input.text, payment_status_input.text, popup))

    def submit_subscription(self, subscriber_name, issue_date, due_date, amount, payment_status, popup):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM subscribers WHERE name = %s", (subscriber_name,))
        subscriber_id = cursor.fetchone()[0]
        cursor.close()

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO subscriptions (subscriber_id, issue_date, due_date, amount, payment_status) VALUES (%s, %s, %s, %s, %s)", (subscriber_id, issue_date, due_date, amount, payment_status))
        self.connection.commit()
        cursor.close()
        popup.dismiss()
        print("Subscription added successfully!")

    def get_subscribers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM subscribers")
        subscribers = [subscriber[0] for subscriber in cursor.fetchall()]
        cursor.close()
        return subscribers

    def view_subscriptions(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT subscriptions.id, subscribers.name, subscriptions.issue_date, subscriptions.due_date, subscriptions.amount, subscriptions.payment_status FROM subscriptions JOIN subscribers ON subscriptions.subscriber_id = subscribers.id")
        subscriptions = cursor.fetchall()
        cursor.close()

        popup_layout = BoxLayout(orientation="vertical", spacing=10)

        for subscription in subscriptions:
            subscription_info_label = Label(text=f"ID: {subscription[0]}\nName: {subscription[1]}\nIssue Date: {subscription[2]}\nDue Date: {subscription[3]}\nAmount: {subscription[4]}\nPayment Status: {subscription[5]}", color=(1, 1, 1, 1), font_size=16)
            popup_layout.add_widget(subscription_info_label)

        Popup(title="All Subscriptions", content=popup_layout, size_hint=(0.8, 0.8)).open()

    def search_by_meter_number(self):
        # Create a popup for searching by meter number
        popup_layout = BoxLayout(orientation="vertical", spacing=10)

        # Input field for meter number
        meter_number_input = TextInput(hint_text="Enter meter number", multiline=False, size_hint=(1, 0.1))
        popup_layout.add_widget(meter_number_input)

        # Button to search
        search_button = Button(text="Search", size_hint=(1, 0.1), background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        popup_layout.add_widget(search_button)

        # Create the popup
        popup = Popup(title="Search by Meter Number", content=popup_layout, size_hint=(0.8, 0.4))
        popup.open()

        # Bind search button to search by meter number
        search_button.bind(on_press=lambda x: self.display_subscription_by_meter_number(meter_number_input.text, popup))

    def display_subscription_by_meter_number(self, meter_number, popup):
        cursor = self.connection.cursor()
        cursor.execute("SELECT subscriptions.id, subscribers.name, subscriptions.issue_date, subscriptions.due_date, subscriptions.amount, subscriptions.payment_status FROM subscriptions JOIN subscribers ON subscriptions.subscriber_id = subscribers.id WHERE subscribers.meter_number = %s", (meter_number,))
        subscriptions = cursor.fetchall()
        cursor.close()

        popup_layout = BoxLayout(orientation="vertical", spacing=10)

        for subscription in subscriptions:
            subscription_info_label = Label(text=f"ID: {subscription[0]}\nName: {subscription[1]}\nIssue Date: {subscription[2]}\nDue Date: {subscription[3]}\nAmount: {subscription[4]}\nPayment Status: {subscription[5]}", color=(1, 1, 1, 1), font_size=16)
            popup_layout.add_widget(subscription_info_label)

        Popup(title="Subscriptions for Meter Number: " + meter_number, content=popup_layout, size_hint=(0.8, 0.8)).open()
  
    def exit(self):
        App.get_running_app().stop()

class ElectricityApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainScreen(name="main"))
        return screen_manager

if __name__ == "__main__":
    ElectricityApp().run()

