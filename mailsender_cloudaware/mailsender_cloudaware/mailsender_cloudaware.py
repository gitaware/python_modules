#!/usr/bin/python3

import smtplib
from email import encoders
from email.utils import formataddr
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mimetypes import guess_type
import os

class Mailsender:
  def __init__( self, subject=None, body=None, html_body=None, sender=None, recipient=None , cc=None, bcc=None, mailserver={'hostname': 'localhost', 'port': 25 } ):
    self.subject   = subject
    self.txt_body  = body
    self.html_body = html_body
    self.sender    = None if sender is None    else formataddr((sender['name'], sender['address']))
    self.recipient = None if recipient is None else formataddr((recipient['name'], recipient['address']))
    self.CC        = None if cc is None        else formataddr((cc['name'], cc['address']))
    self.BCC       = None if bcc is None       else formataddr((bcc['name'], bcc['address']))
    self.mailserver= mailserver
    self.message   = MIMEMultipart('mixed')

  def set_subject(self, subject):
    self.subject = subject

  def set_body(self, body):
    self.set_txt_body(body)
  
  def set_txt_body(self, body):
    self.txt_body = body

  def set_html_body(self, body):
    self.html_body = body

  def set_sender(self, sender):
    self.sender = formataddr((sender['name'], sender['address']))

  def set_recipient(self, recipient):
    self.recipient = formataddr((recipient['name'], recipient['address']))

  def set_cc(self, cc):
    self.CC = formataddr((cc['name'], cc['address']))

  def set_bcc(self, bcc):
    self.BCC = formataddr((bcc['name'], bcc['address']))

  def add_attachment(self, filepath):
    mimetype, encoding = guess_type(filepath)
    mimetype = mimetype.split('/', 1)
    with open(filepath, "rb") as attachment:
      part = MIMEBase(mimetype[0], mimetype[1])
      part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
    "Content-Disposition", 'attachment',
    filename="%s"%(os.path.basename(filepath))
    )
    self.message.attach(part)

  def send(self):
    self.message['Subject'] = self.subject
    self.message['From']    = self.sender
    self.message['To']      = self.recipient
    if self.CC:
      self.message['Cc']      = self.CC
    if self.BCC:
      self.message['Bcc']     = self.BCC
    #MIXED
    #| ALTERNATIVE
    #| | text part
    #| | html part
    #| attachment
    body = MIMEMultipart('alternative')
    if self.txt_body is not None:
      body.attach(MIMEText(self.txt_body, "plain"))
    if self.html_body is not None:
      body.attach(MIMEText(self.html_body, "html"))
    self.message.attach(body)

    with smtplib.SMTP(self.mailserver['hostname'], self.mailserver['port']) as server:
      #server.login(sender_email, password)
      server.send_message(self.message )
    #safety for mailings
    self.subject   = None
    self.txt_body  = None
    self.html_body = None
    self.sender    = None
    self.recipient = None
    self.CC        = None
    self.BCC       = None
    self.message   = MIMEMultipart('mixed')
