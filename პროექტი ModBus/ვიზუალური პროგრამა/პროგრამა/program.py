import mysql.connector
import traceback
import gi
import matplotlib.pyplot as plt
import matplotlib.backends.backend_gtk3 as gtk3
from datetime import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GLib
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas


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
          
          
class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="მთავარი")
        self.set_default_size(700, 600)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.09, 0.47, 0.43, 1.0))  # deep sea green
        self.setup_ui()

    def setup_ui(self):
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Logo
        logo = Gtk.Image.new_from_file("/home/lela/Downloads/Screenshot_from_2023-06-21_22-24-14-removebg-preview.png")
        grid.attach(logo, 0, 0, 3, 1)

        # Buttons for Key Actions
        create_button = Gtk.Button(label="🎛 მოწყობილობების კონტროლი")
        open_button = Gtk.Button(label=" 🔎 მონაცემების ძებნა")
        search_button = Gtk.Button(label="📈 მონაცემების ვიზუალიზაცია")

        create_button.set_size_request(200, 50)
        open_button.set_size_request(200, 50)
        search_button.set_size_request(200, 50)

        grid.attach(create_button, 0, 1, 3, 1)
        grid.attach(open_button, 0, 2, 3, 1)
        grid.attach(search_button, 0, 3, 3, 1)

       

       
        grid.set_halign(Gtk.Align.CENTER)

       
        create_button.connect("clicked", self.on_create_clicked)
        open_button.connect("clicked", self.on_open_clicked)
        search_button.connect("clicked", self.on_search_clicked)
        

        self.show_all()

    def on_create_clicked(self, button):
        self.hide()
        search_window = DeviceWindow()
        search_window.connect("destroy", Gtk.main_quit)
        search_window.show_all()
        Gtk.main()

    def on_open_clicked(self, button):
        self.hide()
        search_window = SearchWindow()
        search_window.connect("destroy", Gtk.main_quit)
        search_window.show_all()
        Gtk.main()

    def on_search_clicked(self, button):
        self.hide()
        search_window = DataVisualizationWindow()
        search_window.connect("destroy", Gtk.main_quit)
        search_window.show_all()
        Gtk.main()
       
 
 
class DeviceWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="მოწყობილობების კონტროლი")
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.09, 0.47, 0.43, 1.0)) #deep sea green
        self.set_default_size(500, 400)
        


       
        self.label_id = Gtk.Label(label="Device ID:")
        self.entry_id = Gtk.Entry()
        self.label_name = Gtk.Label(label="Device Name:")
        self.entry_name = Gtk.Entry()
        self.button_add = Gtk.Button(label="მოწყობილობის დამატება")
        self.button_add.connect("clicked", self.on_add_button_clicked)
        self.liststore = Gtk.ListStore(int, str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        self.create_treeview_columns()
        self.button_delete = Gtk.Button(label="მოწყობილობის წაშლა")
        self.button_delete.connect("clicked", self.on_delete_button_clicked)

       
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(self.label_id, False, False, 0)
        vbox.pack_start(self.entry_id, False, False, 0)
        vbox.pack_start(self.label_name, False, False, 0)
        vbox.pack_start(self.entry_name, False, False, 0)
        vbox.pack_start(self.button_add, False, False, 0)
        vbox.pack_start(self.treeview, True, True, 0)
        vbox.pack_start(self.button_delete, False, False, 0)
        
      
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_vbox.set_margin_start(20)
        main_vbox.set_margin_end(20)
        main_vbox.set_margin_top(20)
        main_vbox.set_margin_bottom(20)
        main_vbox.pack_start(vbox, True, True, 0)

        logout_button = Gtk.Button.new_with_label("გამოსვლა")
        logout_button.connect("clicked", self.logout)
        main_vbox.pack_start(logout_button, False, False, 0)

        self.add(main_vbox)

    
        self.db_config = {
            'user': 'root',
            'password': '123456789',
            'host': 'localhost',
            'database': 'db_ModBus',
            'raise_on_warnings': True
        }

      
        self.timeout_id = GLib.timeout_add_seconds(5, self.refresh_data)

       
        self.load_devices()

    def create_treeview_columns(self):
        renderer_id = Gtk.CellRendererText()
        column_id = Gtk.TreeViewColumn("Device ID", renderer_id, text=0)
        self.treeview.append_column(column_id)

        renderer_name = Gtk.CellRendererText()
        column_name = Gtk.TreeViewColumn("Device Name", renderer_name, text=1)
        self.treeview.append_column(column_name)

    def clear_entries(self):
        self.entry_id.set_text("")
        self.entry_name.set_text("")

    def load_devices(self):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

   
        cursor.execute("SELECT dev_id, dev_name FROM t_device")

   
        self.liststore.clear()

    
        for row in cursor:
            self.liststore.append(row)

        cursor.close()
        conn.close()

    def refresh_data(self):
        self.load_devices()
        return True

    def on_add_button_clicked(self, button):
        dev_id_text = self.entry_id.get_text()
        dev_name = self.entry_name.get_text()

        try:
            dev_id = int(dev_id_text)
        except ValueError:
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Invalid Device ID! Please enter a valid integer."
            )
            dialog.run()
            dialog.destroy()
            return

        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

      
        insert_query = "INSERT INTO t_device (dev_id, dev_name) VALUES (%s, %s)"
        values = (dev_id, dev_name)
        cursor.execute(insert_query, values)

        if cursor.rowcount > 0:
          
            self.clear_entries()
        else:
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Failed to add device!"
            )
            dialog.run()
            dialog.destroy()

        cursor.close()
        conn.commit()
        conn.close()

    def on_delete_button_clicked(self, button):
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            dev_id = model[treeiter][0]  
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

           
            delete_query = "DELETE FROM t_device WHERE dev_id = %s"
            cursor.execute(delete_query, (dev_id,))

            if cursor.rowcount > 0:
               
                self.clear_entries()
            else:
                dialog = Gtk.MessageDialog(
                    parent=self,
                    flags=0,
                    message_type=Gtk.MessageType.WARNING,
                    buttons=Gtk.ButtonsType.OK,
                    text="Failed to delete device!"
                )
                dialog.run()
                dialog.destroy()

            cursor.close()
            conn.commit()
            conn.close()

    def logout(self, button):
        self.hide()
        search_window = MainWindow()
        search_window.connect("destroy", Gtk.main_quit)
        search_window.show_all()
        Gtk.main()

    def destroy(self, *args):
       
        GLib.source_remove(self.timeout_id)
        Gtk.Window.destroy(self, *args)
        
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="db_ModBus"
)

cur = conn.cursor()


class DataVisualizationWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="მონაცემების ვიზუალიზაცია")
        self.set_default_size(1000, 800)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.start_date = Gtk.Calendar()
        self.end_date = Gtk.Calendar()

        self.start_date.set_size_request(200, 200)
        self.end_date.set_size_request(200, 200)

        self.grid.attach(self.start_date, 0, 0, 1, 1)
        self.grid.attach(self.end_date, 1, 0, 1, 1)

        self.device_combo = Gtk.ComboBoxText()

        # 
        self.initialize_database()
        self.fetch_devices()

        self.grid.attach(self.device_combo, 2, 0, 1, 1)

        self.refresh_button = Gtk.Button(label="განახლება")
        self.refresh_button.connect("clicked", self.refresh_data)
        self.refresh_button.set_size_request(200, 50)

        self.grid.attach(self.refresh_button, 0, 1, 3, 1)
        self.refresh_button.set_halign(Gtk.Align.CENTER)
        self.refresh_button.set_valign(Gtk.Align.CENTER)

        self.graph_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.grid.attach(self.graph_box, 0, 2, 3, 1)
        self.graph_box.set_hexpand(True)
        self.graph_box.set_vexpand(True)

        logout_button = Gtk.Button.new_with_label("გამოსვლა")
        logout_button.connect("clicked", self.logout)
        self.grid.attach(logout_button, 0, 3, 3, 1)

        self.show_all()

    def initialize_database(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="db_ModBus"
        )
        self.cur = self.conn.cursor()

    def fetch_devices(self):
        self.cur.execute("SELECT id, dev_name FROM t_device")
        devices = self.cur.fetchall()
        for device in devices:
            device_id = device[0]
            dev_name = device[1]
            self.device_combo.append_text(dev_name)

    def create_graph(self, table_name, name):
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        
        start_datetime = datetime(start_date[0], start_date[1] + 1, start_date[2])
        end_datetime = datetime(end_date[0], end_date[1] + 1, end_date[2])

        self.cur.execute(f"SELECT * FROM {table_name} WHERE date_time BETWEEN %s AND %s",
                    (start_datetime, end_datetime))
        rows = self.cur.fetchall()

        x_data = [row[3] for row in rows]
        y_data = [row[2] for row in rows]

        fig, ax = plt.subplots()

        ax.plot(x_data, y_data)

        ax.set_xlabel("Datetime")
        ax.set_ylabel("Meaning")
        ax.set_title(table_name)

        canvas = FigureCanvas(fig)
        canvas.set_size_request(300, 200)

        self.graph_box.pack_start(canvas, True, True, 0)

    def refresh_data(self, button):
        for child in self.graph_box.get_children():
            self.graph_box.remove(child)

        self.create_graph("t_gas_co", "ბუნებრივი აირი")
        self.create_graph("t_pressure", "წნევა")
        self.create_graph("t_temp", "ტემპერატურა")


        self.show_all()
        plt.close()

    def logout(self, button):
        self.hide()
        self.cur.close()
        self.conn.close()
        search_window = MainWindow()
        search_window.connect("destroy", Gtk.main_quit)
        search_window.show_all()
        Gtk.main()

class SearchWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='მონაცემების ძებნა')
        self.set_default_size(500, 400)
        self.connect('destroy', Gtk.main_quit)
        

      
        self.combo_box = Gtk.ComboBoxText()
        self.combo_box.append_text('წნევის სენსორი')
        self.combo_box.append_text('ტემპერატურის სენსორი')
        self.combo_box.append_text('ბუნებრივი აირის სენსორი')

        
        self.sensor_id_entry = Gtk.Entry()

     
        self.calendar = Gtk.Calendar()

      
        self.hour_spin = Gtk.SpinButton()
        self.hour_spin.set_range(0, 23)
        self.hour_spin.set_increments(1, 1)

        self.minute_spin = Gtk.SpinButton()
        self.minute_spin.set_range(0, 59)
        self.minute_spin.set_increments(1, 1)

        self.second_spin = Gtk.SpinButton()
        self.second_spin.set_range(0, 59)
        self.second_spin.set_increments(1, 1)

        self.button = Gtk.Button(label='ძებნა')
        self.button.connect('clicked', self.on_button_clicked)

        self.pressure_label = Gtk.Label(label='წნევის სენსორი:')
        self.temp_label = Gtk.Label(label='ტემპერატურის სენსორი:')
        self.gas_co_label = Gtk.Label(label='ბუნებრივი აირის სენსორი:')

       
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_margin_top(20)
        grid.set_margin_bottom(20)
        grid.set_margin_start(20)
        grid.set_margin_end(20)

        
        grid.attach(Gtk.Label(label='სენსორი:'), 0, 0, 1, 1)
        grid.attach(self.combo_box, 1, 0, 1, 1)
        grid.attach(Gtk.Label(label='სენსორის ID:'), 0, 1, 1, 1)
        grid.attach(self.sensor_id_entry, 1, 1, 1, 1)
        grid.attach(Gtk.Label(label='თარიღი:'), 0, 2, 1, 1)
        grid.attach(self.calendar, 1, 2, 1, 1)
        grid.attach(Gtk.Label(label='საათი:'), 0, 3, 1, 1)
        grid.attach(self.hour_spin, 1, 3, 1, 1)
        grid.attach(Gtk.Label(label='წუთი:'), 0, 4, 1, 1)
        grid.attach(self.minute_spin, 1, 4, 1, 1)
        grid.attach(Gtk.Label(label='წამი:'), 0, 5, 1, 1)
        grid.attach(self.second_spin, 1, 5, 1, 1)
        grid.attach(self.button, 0, 6, 2, 1)
        grid.attach(self.pressure_label, 0, 7, 1, 1)
        grid.attach(self.temp_label, 0, 8, 1, 1)
        grid.attach(self.gas_co_label, 0, 9, 1, 1)

        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.pack_start(grid, True, True, 0)

        logout_button = Gtk.Button.new_with_label("გამოსვლა")
        logout_button.connect("clicked", self.logout)
        vbox.pack_start(logout_button, False, False, 0)

        self.add(vbox)

    def on_button_clicked(self, widget):
      
        sensor_id_text = self.combo_box.get_active_text()
        sensor_id_mapping = {
            'წნევის სენსორი': 1,
            'ტემპერატურის სენსორი': 2,
            'ბუნებრივი აირის სენსორი': 3
        }
        sensor_id = sensor_id_mapping.get(sensor_id_text)

        if sensor_id is None:
            print('Invalid sensor selected')
            return

        
        sensor_id_entry_text = self.sensor_id_entry.get_text()
        if not sensor_id_entry_text.isdigit():
            print('Invalid sensor ID entered')
            return

        sensor_id = int(sensor_id_entry_text)

        
        year, month, day = self.calendar.get_date()

       
        hour = self.hour_spin.get_value_as_int()
        minute = self.minute_spin.get_value_as_int()
        second = self.second_spin.get_value_as_int()

       
        date_str = f'{year}-{month + 1:02d}-{day:02d}'
        time_str = f'{hour:02d}:{minute:02d}:{second:02d}'
        date_time_str = f'{date_str} {time_str}'

       
        pressure_data = retrieve_data(sensor_id, date_time_str, 'search_pressure_data')
        temp_data = retrieve_data(sensor_id, date_time_str, 'search_temp_data')
        gas_co_data = retrieve_data(sensor_id, date_time_str, 'search_gas_co_data')

      
        self.pressure_label.set_text(f'წნევა:     {pressure_data} pa')
        self.temp_label.set_text(f'ტემპერატურა:      {temp_data} °C')
        self.gas_co_label.set_text(f'ბუნებრივი აირი:         {gas_co_data} ppm ')

    def logout(self, button):
        self.hide()
        search_window = MainWindow()
        search_window.connect("destroy", Gtk.main_quit)
        search_window.show_all()
        Gtk.main() 
        
        
            
win = LoginPage()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main() 

