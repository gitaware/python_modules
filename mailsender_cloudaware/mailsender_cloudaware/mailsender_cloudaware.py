#!/usr/bin/python3

import email, mimetypes, smtplib
import os

class Mailsender:
  def __init__( self, subject=None, body=None, sender={'name': None, 'address': None }, recipient={'name': None, 'address': None } , cc={'name': None, 'address': None }, bcc={'name': None, 'address': None }, mailserver={'hostname': 'localhost', 'port': 25 } ):
    self.subject   = subject
    self.body      = body
    self.sender    = sender
    self.recipient = recipient
    self.CC        = cc
    self.BCC       = bcc
    self.mailserver= mailserver
    self.message   = email.message.EmailMessage()

    if self.subject is not None:                           self.message.add_header("Subject", self.subject)
    if self.sender    != {'name': None, 'address': None }: self.message.add_header("From", '"%s" <%s>'%(self.sender['name'], self.sender['address']) )
    if self.recipient != {'name': None, 'address': None }: self.message.add_header("To",   '"%s" <%s>'%(self.recipient['name'], self.recipient['address']) )
    if self.CC        != {'name': None, 'address': None }: self.message.add_header("Cc",   '"%s" <%s>'%(self.CC['name'], self.CC['address']) )
    if self.BCC       != {'name': None, 'address': None }: self.message.add_header("Bcc", '"%s" <%s>'%(self.BCC['name'], self.BCC['address']) )
    if self.body is not None:                              self.message.set_content(self.body)

  def set_subject(self, subject):
    self.subject = subject
    if self.subject is not None:                           self.message.add_header("Subject", self.subject)

  def set_body(self, body):
    self.body = body
    if self.body is not None:                              self.message.set_content(self.body)

  def set_sender(self, sender):
    self.sender = sender
    if self.sender    != {'name': None, 'address': None }: self.message.add_header("From", '"%s" <%s>'%(self.sender['name'], self.sender['address']) )

  def set_recipient(self, recipient):
    self.recipient = recipient
    if self.recipient != {'name': None, 'address': None }: self.message.add_header("To", '"%s" <%s>'%(self.recipient['name'], self.recipient['address']) )

  def add_attachment(self, filepath):
    with open(filepath, "rb") as attachment:
      self.message.add_attachment(attachment.read(), maintype='text', subtype='html', filename=os.path.basename(filepath))

  def send(self):
    with smtplib.SMTP(self.mailserver['hostname'], self.mailserver['port']) as server:
      #server.login(sender_email, password)
      server.send_message(msg=self.message)
    #safety for mailings
    self.message.clear()
