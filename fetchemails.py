import imaplib # to connect to the imap server
import email # to retrieve emails
import os # to save attachments

def fetchattachments(username, password, imapserver = 'imap.free.fr'):
    """
    Connect to the mailox
    Check emails
    Save attachments
    """
    connection = imaplib.IMAP4_SSL(imapserver, 993)
    connection.login(username, password)
    (email_status, emails_number) = connection.select() # connect to the default folder (INBOX)
    print("\nThere is {} emails inside {} account from the imap server {}".format(int(emails_number[0]), username, imapserver))

    (email_status, [emails_number]) = connection.search(None, 'ALL')
    for dummy_email in emails_number.split():
        print('\n *** Working on mail number {}'.format(dummy_email.decode('utf8'))) # dummy_email is in binary mode
        connection.store(dummy_email, '+FLAGS', '(%s)' % 'SEEN')
        (type_email, msg_data) = connection.fetch(dummy_email, '(RFC822)')
        email_body = msg_data[0][1] #retrieve all mail (same as mail source)
        mail = email.message_from_string(email_body.decode('utf8'))

        if mail.is_multipart():
            compteur = 0
            for part in mail.walk():
                compteur += 1
                print('Part {} in mail.walk with Content Type : {}'.format(compteur, part.get_content_type()))
                fileName = part.get_filename() #Renvoie None si pas de fichier attaché
                if bool(fileName): # None => False
                    print('Detected file : {}'.format(fileName))
                    filePath = os.path.join('', fileName)
                    if not os.path.isfile(filePath): # Check is there is already a file with the same name
                        print('Wirting file')
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

    connection.close()
    connection.logout()

fetchattachments('username', 'passwd')
