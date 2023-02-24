import pyqrcode
import png
data = 'bayram karahan'
file_iso = 'QR_ISO.png'
file_utf = 'QR_Utf.png'
file_svg = 'qr.svg'
#creating QR codes
qr_iso = pyqrcode.create(data) #creates qr code using iso-8859-1 encoding
qr_utf = pyqrcode.create(data, encoding = 'utf-8') #creates qr code using utf-8 encoding
#saving png files
qr_iso.svg(file_iso, scale=8, background="white", module_color="#000000")
qr_iso.svg(file_svg, scale=20, background="white", module_color="#000000")
qr_utf.png(file_utf, scale = 8)
qr_iso.png('uca-colors.png', scale=6,module_color=[0, 0, 0, 128],background=[0xff, 0xff, 0xcc])
