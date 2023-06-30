import mysql.connector
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from datetime import datetime

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

