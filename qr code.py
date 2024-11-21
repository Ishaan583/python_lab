import qrcode


features = qrcode.QRCode(version=1, box_size=10, border=4)
features.add_data('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
features.make(fit=True)
img = features.make_image(fill_color='black', back_color='white')
img.save('youtube_qr.png')
