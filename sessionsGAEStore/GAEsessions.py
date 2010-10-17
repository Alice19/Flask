####--My GAE Store---###
class DataBaseStore(SessionStore):
    def __init__(self,tablename,session_class=None):
        SessionStore.__init__(self,session_class)
        self.table=tablename

    def get_sessionrow_db(self,sid):
        query=db.Query(self.table).filter('sessid =',sid)
        return query.get()

    def save(self,session):
        rowwithsid=self.get_sessionrow_db(session.sid)
        if rowwithsid is None:
            rowwithsid=self.table(sessid=session.sid,sessiondata=dumps(dict(session)))
            rowwithsid.put()
            return
        rowwithsid.sessiondata=dumps(dict(session))
        rowwithsid.put()
        return

    def delete(self,session):
        rowwithsid=self.get_sessionrow_db(session.sid)
        rowwithsid.delete()
        return

    def get(self,sid):
        if not self.is_valid_key(sid):
            return self.new()
        rowwithsid=self.get_sessionrow_db(sid)
        if rowwithsid is not None:
            data=loads(rowwithsid.sessiondata)
        return self.session_class(data,sid,False)
