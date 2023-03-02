import asyncio
import qrcode

qrpopover = None
qrimage = None
qrtext = None
qrfile ="/tmp/qrkod.png"

def _qrkod_button_event(widget=None):
    global ip_label_text
    ip_label_text=_("Loading...")
    #loginwindow.o("ui_popover_network").popup()
    os.system("rm /tmp/qrkod.png")
    qrpopover.popup()
    qrcode_control_event()

ip_label_text=""
_last_ip_label_text=""
def update_popover_qr_text():
    global _last_ip_label_text
    if _last_ip_label_text != ip_label_text:
        _last_ip_label_text = ip_label_text
        qrtext.set_text(ip_label_text)
        img = qrcode.make(ip_label_text)
        #qrtext.set_text(lan_ip.strip())
        img.save(qrfile)
        qrimage.set_from_file(qrfile)       
    GLib.timeout_add(500,update_popover_qr_text)

@asynchronous
def qrcode_control_event():
    global ip_label_text
    lan_ip = ""
    # Calculate line length
    i = 0
    for ip, dev in get_local_ip():
        j = len(ip) + len(dev) + 3
        if j > i:
            i = j
    ip_list = get_local_ip()
    if len(ip_list) == 0:
        ip_label_text=_("Network not available")
        return
    for ip, dev in ip_list:
        j = len(ip) + len(dev) + 2
        #lan_ip += "- {} {}{}\n".format(dev," "*(i-j), ip)
        lan_ip += "http://{}:8080\n".format(ip)
    ctx = _("{}").format(lan_ip)
    if get("show-wan-ip",False,"network"):
        wan_ip = get_ip()
        ctx +=_("{}").format(wan_ip)
    ip_label_text=ctx.strip()


def module_init():
    #if not get("show-widget",True,"network"):
        #loginwindow.o("ui_button_network").hide()
    global qrpopover
    global qrimage
    global qrtext
    #if os.path.isfile(qrfile):
        #os.unlink(qrfile)
    qrpopover = Gtk.Popover()
    qrimage = Gtk.Image()
    qrtext = Gtk.Label()
    b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    b.pack_start(qrimage,False,False,0)
    b.pack_start(qrtext,False,False,0)
    qrpopover.add(b)
    qrpopover.set_position(Gtk.PositionType.BOTTOM)
    button = Gtk.MenuButton(label="QR", popover=qrpopover)
    button.connect("clicked",_qrkod_button_event)
    loginwindow.o("ui_box_bottom_left").pack_end(button, False, True, 10)
    button.get_style_context().add_class("icon")
    button.show_all()
    b.show_all()
    #loginwindow.o("ui_button_network").connect("clicked",_qrkod_button_event)
    update_popover_qr_text()

