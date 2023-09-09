from django.conf import settings
from django.core.mail import send_mail, EmailMessage


class Mailer:
    from felicinema.apps.cinema.models import Payment

    @staticmethod
    def send_reserve_request_info(payment: Payment):
        subject = 'Reservation Request from Felicinema'
        message = f'Hi {payment.ticket.session.cinema.user},\n' \
                  f' you have a reservation request for: \n' \
                  f'date: {payment.ticket.session.date} \n' \
                  f'time: {payment.ticket.session.time} \n' \
                  f'movie: {payment.ticket.session.movie} \n' \
                  f'from: {payment.ticket.user} \n' \
                  f'the security code for this reservation is: {payment.code}\n' \
                  f'\n' \
                  f'To accept the reservation please go to the link below and enter the security code: \n' \
                  f'cinema/reservation/{payment.id}/' \
                  f'Or you can check your dashboard and accept the requests you want. \n' \
                  f'Regards, \n' \
                  f'Omid from FeliCinema'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [payment.ticket.user.email, ]
        # email_body = """\
        #     <html>
        #       <head></head>
        #       <body>
        #         <h2>%s</h2>
        #         <p>%s</p>
        #         <h5>%s</h5>
        #       </body>
        #     </html>
        #     """ % (payment.ticket.session.cinema.user, message.replace('\n', '<br>'), payment.ticket.user)
        # email = EmailMessage('A new mail!', email_body, to=recipient_list)
        # email.content_subtype = "html"
        # email.send()
        send_mail(subject, message, email_from, recipient_list)
