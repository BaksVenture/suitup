from mailer import send_mail

def test_send_mail():
    send_mail('test mailer', "<p>testing <b>kkirill's</b> mailer</p>", 'webmaster@tartu.kz', ['germanilyin@gmail.com'])
