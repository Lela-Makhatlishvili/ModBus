import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from login_page import LoginPage

if __name__ == "__main__":
   win = LoginPage()
   win.connect("destroy", Gtk.main_quit)
   win.show_all()
   Gtk.main()

