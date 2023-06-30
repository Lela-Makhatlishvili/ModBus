import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AccountCreationPage(Gtk.Window):
    def __init__(self, login_window):
        Gtk.Window.__init__(self, title="Create Account")
        self.set_default_size(300, 200)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.09, 0.47, 0.43, 1.0)) #deep sea green
        self.login_window = login_window

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(50)
        vbox.set_margin_bottom(50)
        vbox.set_margin_start(50)
        vbox.set_margin_end(50)
        self.add(vbox)

        username_label = Gtk.Label(label="Username:")
        vbox.pack_start(username_label, False, False, 0)

        self.username_entry = Gtk.Entry()
        vbox.pack_start(self.username_entry, False, False, 0)

        password_label = Gtk.Label(label="Password:")
        vbox.pack_start(password_label, False, False, 0)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        vbox.pack_start(self.password_entry, False, False, 0)

        create_button = Gtk.Button(label="Create Account")
        create_button.get_style_context().add_class("suggested-action")
        create_button.connect("clicked", self.on_create_clicked)
        vbox.pack_start(create_button, False, False, 0)

        self.result_label = Gtk.Label()
        self.result_label.set_line_wrap(True)
        self.result_label.set_xalign(0.0)
        vbox.pack_start(self.result_label, False, False, 0)

        self.db_config = {
            'user': 'root',
            'password': '123456789',
            'host': 'localhost',
            'database': 'db_ModBus',
            'raise_on_warnings': True
        }

    def on_create_clicked(self, button):
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()

        if self.create_account(username, password):
            self.result_label.set_text("Account created successfully")
            self.login_window.show()
            self.destroy()
        else:
            self.result_label.set_text("Failed to create account")

    def create_account(self, username, password):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()

            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))

            cnx.commit()

            cursor.close()
            cnx.close()

            return True

        except mysql.connector.Error as err:
            traceback.print_exc()
            self.result_label.set_text(f"Error creating account: {err}")
            return False






class LoginPage(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Login")
        self.set_default_size(300, 200)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.09, 0.47, 0.43, 1.0))


        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(50)
        vbox.set_margin_bottom(50)
        vbox.set_margin_start(50)
        vbox.set_margin_end(50)
        self.add(vbox)

        username_label = Gtk.Label(label="მომხმარებელი:")
        vbox.pack_start(username_label, False, False, 0)

        self.username_entry = Gtk.Entry()
        vbox.pack_start(self.username_entry, False, False, 0)

        password_label = Gtk.Label(label="პაროლი:")
        vbox.pack_start(password_label, False, False, 0)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        vbox.pack_start(self.password_entry, False, False, 0)

        login_button = Gtk.Button(label="სისტემაში შესვლა")
        login_button.get_style_context().add_class("suggested-action")
        login_button.connect("clicked", self.on_login_clicked)
        vbox.pack_start(login_button, False, False, 0)

        create_account_button = Gtk.Button(label="რეგისტრაცია")
        create_account_button.connect("clicked", self.on_create_account_clicked)
        vbox.pack_start(create_account_button, False, False, 0)

        self.result_label = Gtk.Label()
        self.result_label.set_line_wrap(True)
        self.result_label.set_xalign(0.0)
        vbox.pack_start(self.result_label, False, False, 0)

        self.db_config = {
            'user': 'root',
            'password': '123456789',
            'host': 'localhost',
            'database': 'db_ModBus',
            'raise_on_warnings': True
        }

    def on_login_clicked(self, button):
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()

        if self.validate_credentials(username, password):
            self.hide()
            main_window = MainWindow()
            main_window.connect("destroy", Gtk.main_quit)
            main_window.show_all()
            Gtk.main()
        else:
            self.result_label.set_text("არასწორი მონაცემები")

    def on_create_account_clicked(self, button):
        account_creation_window = AccountCreationPage(self)
        account_creation_window.show_all()

    def validate_credentials(self, username, password):
        try:
            cnx = mysql.connector.connect(**self.db_config)
            cursor = cnx.cursor()

            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            cursor.close()
            cnx.close()

            return result is not None

        except mysql.connector.Error as err:
            traceback.print_exc()
            self.result_label.set_text(f"Error accessing database: {err}")
            return False
