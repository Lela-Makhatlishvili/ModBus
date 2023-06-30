
class DeviceWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="მოწყობილობების კონტროლი")
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.09, 0.47, 0.43, 1.0)) #deep sea green
        self.set_default_size(500, 400)
        


        # 
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

        # 
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(self.label_id, False, False, 0)
        vbox.pack_start(self.entry_id, False, False, 0)
        vbox.pack_start(self.label_name, False, False, 0)
        vbox.pack_start(self.entry_name, False, False, 0)
        vbox.pack_start(self.button_add, False, False, 0)
        vbox.pack_start(self.treeview, True, True, 0)
        vbox.pack_start(self.button_delete, False, False, 0)
        
        # 
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

        # Database
        self.db_config = {
            'user': 'root',
            'password': '123456789',
            'host': 'localhost',
            'database': 'db_ModBus',
            'raise_on_warnings': True
        }

        # 
        self.timeout_id = GLib.timeout_add_seconds(5, self.refresh_data)

        # 
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

    # 
        cursor.execute("SELECT dev_id, dev_name FROM t_device")

    # 
        self.liststore.clear()

    # 
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

        # 
        insert_query = "INSERT INTO t_device (dev_id, dev_name) VALUES (%s, %s)"
        values = (dev_id, dev_name)
        cursor.execute(insert_query, values)

        if cursor.rowcount > 0:
            # 
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

            # 
            delete_query = "DELETE FROM t_device WHERE dev_id = %s"
            cursor.execute(delete_query, (dev_id,))

            if cursor.rowcount > 0:
                #
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
        # 
        GLib.source_remove(self.timeout_id)
        Gtk.Window.destroy(self, *args)
     
