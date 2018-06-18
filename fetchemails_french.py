import imaplib # pour la connexion au serveur
import email # pour la gestion des emails
import os # pour la sauvearde des pièces-jointes

def lecture_emails(boite, mot_de_passe, serveur_imap = 'imap.free.fr'):
    """
    Se connecte à la boite aux lettres
    Vérifie le nombre de mails
    Enregistre les pièces-jointes des emails
    """
    connection = imaplib.IMAP4_SSL(serveur_imap, 993)
    connection.login(boite, mot_de_passe)
    (email_status, nombre_de_messages) = connection.select() # connexion au dossier par défaut (INBOX)
    print("\nLe nombre d'emails de la boite {} sur le serveur {} est de {}".format(boite, serveur_imap, int(nombre_de_messages[0])))
    #connection.search(None, 'ALL') # renvoie la liste des messages : ('OK', [b'1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19'])
    #connection.search(None, 'UNSEEN') # renvoie la liste des emails non lus : ('OK', [b'17 18 19'])

    (email_status, [nombre_de_mails]) = connection.search(None, 'ALL')
    for dummy_email in nombre_de_mails.split():
        print('\n *** Traitement du mail numéro {}'.format(dummy_email.decode('utf8'))) # car dummy_email est au format binaire
        #connection.store('1', '+FLAGS', '(%s)' % 'SEEN') => renvoie ('OK', [b'1 (FLAGS (\\Seen SEEN))'])
        connection.store(dummy_email, '+FLAGS', '(%s)' % 'SEEN')
        (type_email, msg_data) = connection.fetch(dummy_email, '(RFC822)')
        email_body = msg_data[0][1] #reçoit tout le mail (source du mail)
        mail = email.message_from_string(email_body.decode('utf8'))
        #print('Sujet du mail : ', mail['Subject']) #renvoie le sujet de l'email
        #print('mail.get_content_maintype() : ', mail.get_content_maintype())

        if mail.is_multipart(): # => renvoie True
            compteur = 0
            for part in mail.walk():
                compteur += 1
                print('Partie {} dans mail.walk avec comme Content Type : {}'.format(compteur, part.get_content_type()))
                fileName = part.get_filename() #Renvoie None si pas de fichier attaché
                if bool(fileName): # None => False
                    print('Fichier détecté : {}'.format(fileName))
                    filePath = os.path.join('', fileName)
                    if not os.path.isfile(filePath): # Vérifie si le fichier existe déjà
                        print('Écriture du fichier')
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

    connection.close()
    connection.logout()

lecture_emails('username', 'passwd')
