import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
   
def retrieve_data(sensor_id, date_time, procedure_name):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

    
        cursor.callproc(procedure_name, [sensor_id, date_time])

        result = None
        for result in cursor.stored_results():
            data = result.fetchall()
            break

        cursor.close()
        conn.close()

        if result is not None:
            return data
        else:
            return None
    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)

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

        # 
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_margin_top(20)
        grid.set_margin_bottom(20)
        grid.set_margin_start(20)
        grid.set_margin_end(20)

        # 
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

        # 
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
        # Retrieve the selected sensor
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

        #
        sensor_id_entry_text = self.sensor_id_entry.get_text()
        if not sensor_id_entry_text.isdigit():
            print('Invalid sensor ID entered')
            return

        sensor_id = int(sensor_id_entry_text)

        # 
        year, month, day = self.calendar.get_date()

        # 
        hour = self.hour_spin.get_value_as_int()
        minute = self.minute_spin.get_value_as_int()
        second = self.second_spin.get_value_as_int()

        # 
        date_str = f'{year}-{month + 1:02d}-{day:02d}'
        time_str = f'{hour:02d}:{minute:02d}:{second:02d}'
        date_time_str = f'{date_str} {time_str}'

        #
        pressure_data = retrieve_data(sensor_id, date_time_str, 'search_pressure_data')
        temp_data = retrieve_data(sensor_id, date_time_str, 'search_temp_data')
        gas_co_data = retrieve_data(sensor_id, date_time_str, 'search_gas_co_data')

        # 
        self.pressure_label.set_text(f'წნევა:     {pressure_data} pa')
        self.temp_label.set_text(f'ტემპერატურა:      {temp_data} °C')
        self.gas_co_label.set_text(f'ბუნებრივი აირი:         {gas_co_data} ppm ')

    def logout(self, button):
        self.hide()
        search_window =  MainWindow()
        search_window.connect("destroy", Gtk.main_quit)
        search_window.show_all()
        Gtk.main()


