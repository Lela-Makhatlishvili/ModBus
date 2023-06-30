from gi.repository import Gtk, Gdk
from datasearch import SearchWindow
from devicecontrol import DeviceWindow
from devicecontrol import DeviceWindow
from visualization import DataVisualizationWindow




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

        # Buttons
        create_button = Gtk.Button(label="🎛 მოწყობილობების კონტროლი")
        open_button = Gtk.Button(label=" 🔎 მონაცემების ძებნა")
        search_button = Gtk.Button(label="📈 მონაცემების ვიზუალიზაცია")

        create_button.set_size_request(200, 50)
        open_button.set_size_request(200, 50)
        search_button.set_size_request(200, 50)

        grid.attach(create_button, 0, 1, 3, 1)
        grid.attach(open_button, 0, 2, 3, 1)
        grid.attach(search_button, 0, 3, 3, 1)

       

        # 
        grid.set_halign(Gtk.Align.CENTER)

        # 
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

   
