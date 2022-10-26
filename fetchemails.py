import imaplib # to connect to the imap server
import email # to retrieve emails
import os # to save attachments
import argparse # gestion des arguments
from time import sleep # to do a pause

def fetchattachments(username, password, folder, verbose = True, delete = False, imapserver = 'imap.free.fr'):
    """
    Connect to the mailox
    Check emails
    Save attachments
    """
    connection = imaplib.IMAP4_SSL(imapserver, 993)
    connection.login(username, password)
    (email_status, emails_number) = connection.select() # connect to the default folder (INBOX)
    if verbose:
        print("\nThere is {} emails inside {} account from the imap server {}".format(int(emails_number[0]), username, imapserver))

    (email_status, [emails_number]) = connection.search(None, 'ALL')
    for dummy_email in emails_number.split():
        if verbose:
            print('\n *** Working on mail number {}'.format(dummy_email.decode('utf8'))) # dummy_email is in binary mode
        connection.store(dummy_email, '+FLAGS', '(%s)' % 'SEEN')
        (type_email, msg_data) = connection.fetch(dummy_email, '(RFC822)')
        email_body = msg_data[0][1] #retrieve all mail (same as mail source)
        mail = email.message_from_string(email_body.decode('utf8'))

        if mail.is_multipart():
            compteur = 0
            for part in mail.walk():
                compteur += 1
                if verbose:
                    print('Part {} in mail.walk with Content Type : {}'.format(compteur, part.get_content_type()))
                fileName = part.get_filename() #Renvoie None si pas de fichier attaché
                if bool(fileName): # None => False
                    if verbose:
                        print('Detected file : {}'.format(fileName))
                    filePath = os.path.join(folder, fileName)
                    if not os.path.isfile(filePath): # Check is there is already a file with the same name
                        if verbose:
                            print('Writing file')
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
        if delete:
            connection.store(dummy_email, '+FLAGS', '\\Deleted')
    if delete:
        connection.expunge()
        if verbose:
            print('\nEmails deleted')
    connection.close()
    connection.logout()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download all attachments from an email account")
    parser.add_argument('folder', help="the folder where you want to save your attachements")
    parser.add_argument('email', type=str, help="imap account user id")
    parser.add_argument('password', type=str, help="imap account password")
    parser.add_argument('-d', '--delete', action='store_true', help="delete emails after saving attachment")
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose mode")
    #parser.add_argument('-imap', help="imap server (by default is imap.free.fr)")
    args = parser.parse_args()
    folder = args.folder
    identifiant = args.email
    password = args.password
    if args.verbose:
        verbose = True
        print("\nVerbose mode activated\n")
    else:
        verbose = False
    if args.delete:
        delete = True
        print(f"\nMessages will be deleted from {identifiant}\nYou have now 5 seconds to cancel")
        sleep(5)
        print("\nOK, let's go")
    else:
        delete = False
    if args.imap:
        imap = args.imap
        fetchattachments(identifiant, password, folder, verbose, delete, imap)
    else:
        fetchattachments(identifiant, password, folder, verbose, delete)
