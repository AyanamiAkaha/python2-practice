import io

from word_parser import Parser, is_WORD

UPDATE = {
  'qmark':    r'UPDATE ? SET cnt=cnt+1 WHERE w1=? AND w2=?, ',
  'numeric':  r'UPDATE :1 SET cnt=cnt+1 WHERE w1=:2 AND w2=:3',
  'named':    r'UPDATE :table SET cnt=cnt+1 WHERE w1=:w1 AND w2=:w2,',
  'format':   r'UPDATE %s SET cnt=cnt+1 WHERE w1=%s AND w2=%s,',
  'pyformat': r'UPDATE %(table)s SET cnt=cnt+1 WHERE w1=%(w1)s AND w2=%(w2)s,',
}
INSERT = {
  'qmark':    r'INSERT INTO ? (w1, w2, cnt) VALUES (?, ?, 1)',
  'numeric':  r'INSERT INTO :1 (w1, w2, cnt) VALUES (:2, :3, 1)',
  'named':    r'INSERT INTO :table VALUES(w1=:w1, w2=:w2, 1)',
  'format':   r'INSERT INTO %s VALUES(%s, %s, 1)',
  'pyformat': r'INSERT INTO %(table)s VALUES(%(w1)s, %(w2)s, 1)i)',
}
CREATE = {
  'qmark':    'CREATE TABLE IF NOT EXISTS ? (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)',
  'numeric':  'CREATE TABLE IF NOT EXISTS :1 (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)',
  'named':    'CREATE TABLE IF NOT EXISTS :table (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)',
  'format':   'CREATE TABLE IF NOT EXISTS %s (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)',
  'pyformat': 'CREATE TABLE IF NOT EXISTS %(table)s (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)'
}

class Analyzer:
  """
  Class for analyzing given input stream, and collecting results in
  database.

  :param stream input stream to process
  :param db database for results
  :param table name of the table to hold data
  """

  def __init__(self, stream, db, table):
    self._parser = Parser(stream, is_WORD)
    self._db = db.open()
    self.UPDATE = UPDATE[db.paramstyle]
    self._table = table
    self._create_table()
    self.__update_cursor = self._db.cursor()
    self.__insert_cursor = self._db.cursor()

  def __del__(self):
    self.close()

  def close(self):
    """
    Close underlying resources.
    Analyzer cannot be used after closing.
    """
    self._parser.close()
    self.__update_cursor.close()
    self.__insert_cursor.close()
    self._db.close()

  def _create_table(self):
    """
    Create table for storing data.
    """
    cursor = self._db.cursor();
    cursor.execute(CREATE, (self._table,))
    cursor.close()

  def __upsert(self, w1, w2):
    """
    Update record, or insert a new one, if no rows were updated.
    :param w1 first word
    :param w2 second word
    """
    self.__update_cursor.execute(UPDATE, (self._table, w1, w2))
    if self.__update_cursor.rowcount == 0:
      self.__insert_cursor.execute(INSERT, (self._table, w1, w2))

  def parse(self):
    """
    Parse stream into word pairs, using None for beginning and end of the sentence.
    """
    last = None
    for current in self._parser:
      self.__upsert(last, current)
      last = current
      if current[-1:] == '.':
        self.upsert(current, None)
        last = None
