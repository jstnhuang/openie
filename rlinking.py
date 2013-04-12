import openie.constants as constants
import sqlite3

class RelationLinker:
  def __init__(self, dbPath=constants.PBTABLES_DB_PATH):
    self.connection = sqlite3.connect(dbPath)

  def get_relation_links(self, rel):
    rlinks = set()
    cursor = self.connection.cursor()
    cursor.execute(
      'SELECT pb, prob, count '
      'FROM str_to_pb_syn '
      'WHERE vp=? '
      'ORDER BY prob DESC LIMIT 10', 
      (rel,)
    )
    for (pb, prob, count) in cursor:
      rlinks.add(pb)
    return rlinks
