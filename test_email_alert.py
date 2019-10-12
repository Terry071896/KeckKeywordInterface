from email_alert import Email_Alert

emailList = ['tcox@keck.hawaii.edu',
            'tfcox12@gmail.com']
subject = 'ALERT: TEST TO WORK'
body = 'Hello everyone! There is an error that needs to be fixed blah blah blah'
test = Email_Alert(email_send=emailList, subject=subject, body=body)
test.send()

i = 0
while not test.receive():
    i += 1
    if i % 1000 == 0:
        test.receive()
