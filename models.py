class MyNewSessionTable(db.Model):
    sessid=db.StringProperty(multiline=True)
    sessiondata=db.BlobProperty()
