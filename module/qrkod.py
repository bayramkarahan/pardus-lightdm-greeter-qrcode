import asyncio
import pyqrcode

qrpopover = None
qrimage = None

def _qrkod_button_event(widget=None):
    qrpopover.popup()

@asynchronous
def qrkod_control_event():
    if os.path.isfile("/tmp/qrkod.svg"):
        return
    lan_ip = ""
    for ip, dev in get_local_ip():
        lan_ip += "http://{}:8080\n".format(ip)
    qr = pyqrcode.create(lan_ip.strip())
    qr.svg("/tmp/qrkod.svg",scale=8, background="white", module_color="#000000")
    
    #img = qrcode.make(lan_ip.strip())
    #type(img)  # qrcode.image.pil.PilImage
    #img.save("/tmp/qrkod.png")

def update_qr_image():
    if not os.path.isfile("/tmp/qrkod.svg"):
        GLib.timeout_add(500,update_qr_image)
        return
    qrimage.set_from_file("/tmp/qrkod.svg")

def module_init():
    global qrpopover
    global qrimage
    qrpopover = Gtk.Popover()
    qrimage = Gtk.Image()
    qrpopover.add(qrimage)
    qrpopover.set_position(Gtk.PositionType.BOTTOM)
    button = Gtk.MenuButton(label="QR", popover=qrpopover)
    button.connect("clicked",_qrkod_button_event)
    loginwindow.o("ui_box_bottom_left").pack_end(button, False, True, 10)
    button.get_style_context().add_class("icon")
    button.show_all()
    qrimage.show()
    GLib.idle_add(qrkod_control_event)
    update_qr_image()
