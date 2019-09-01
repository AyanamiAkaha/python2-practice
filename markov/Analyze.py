import io

from word_parser import Parser, is_WORD

UPDATE = {
  'qmark':    r'UPDATE ? SET w1=?, w2=?, cnt=?',
  'numeric':  r'UPDATE :1 SET w1=:2, w2=:3, cnt=:4',
  'named':    r'UPDATE :table SET w1=:w1, w2=:w2, cnt=:cnt',
  'format':   r'UPDATE %s SET w1=%s, w2=%s, cnt=%s',
  'pyformat': r'UPDATE %(table)s SET w1=%(w1)s, w2=%(w2)s, cnt=%(cnt)i',
}
INSERT = {
  'qmark':    r'INSERT INTO ? (w1, w2, cnt) VALUES (?, ?, ?)',
  'numeric':  r'INSERT INTO :1 (w1, w2, cnt) VALUES (:2, :3, :4)',
  'named':    r'INSERT INTO :table VALUES(w1=:w1, w2=:w2, cnt=:cnt)',
  'format':   r'INSERT INTO %s VALUES(%s, %s, %s)',
  'pyformat': r'INSERT INTO %(table)s VALUES(%(w1)s, %(w2)s, %(cnt)i)',
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

  def __del__(self):
    self.close()

  def close(self):
    """
    Close underlying resources.
    Analyzer cannot be used after closing.
    """
    self._parser.close()
    self._db.close()

  def _create_table(self):
    """
    Create table for storing data.
    """
    cursor = self._db.cursor();
    cursor.execute(CREATE, (self._table,))
    cursor.close()

  def __upsert(self, word):
    # TODO universal upsert: update, if affects 0 rows insert
    raise NotImplementedError
