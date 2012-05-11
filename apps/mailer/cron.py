from cronjob.loading import cronreg
from mailer.management.commands.send_mail import Command as SendMailCommand
from mailer.management.commands.retry_deferred import Command as DeferredMailCommand

@cronreg.register
def send_mail():
    """ send mail """
    SendMailCommand().handle_noargs()

@cronreg.register
def send_deferred_mail():
    """ send deferred mail """
    DeferredMailCommand().handle_noargs()
