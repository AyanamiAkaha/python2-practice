import io

from word_parser import Parser, is_WORD

UPDATE = {
  'qmark':    r'UPDATE markov SET cnt=cnt+1 WHERE w1=? AND w2=?',
  'numeric':  r'UPDATE markov SET cnt=cnt+1 WHERE w1=:1 AND w2=:2',
  'named':    r'UPDATE markov SET cnt=cnt+1 WHERE w1=:w1 AND w2=:w2',
  'format':   r'UPDATE markov SET cnt=cnt+1 WHERE w1=%s AND w2=%s',
  'pyformat': r'UPDATE markov SET cnt=cnt+1 WHERE w1=%(w1)s AND w2=%(w2)s',
}
INSERT = {
  'qmark':    r'INSERT INTO markov (w1, w2, cnt) VALUES (?, ?, 1)',
  'numeric':  r'INSERT INTO markov (w1, w2, cnt) VALUES (:1, :2, 1)',
  'named':    r'INSERT INTO markov VALUES(w1=:w1, w2=:w2, 1)',
  'format':   r'INSERT INTO markov VALUES(%s, %s, 1)',
  'pyformat': r'INSERT INTO markov VALUES(%(w1)s, %(w2)s, 1)i)',
}
CREATE = {
  'qmark':    'CREATE TABLE IF NOT EXISTS markov (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)',
  'numeric':  'CREATE TABLE IF NOT EXISTS markov (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)',
  'named':    'CREATE TABLE IF NOT EXISTS markov (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)',
  'format':   'CREATE TABLE IF NOT EXISTS markov (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)',
  'pyformat': 'CREATE TABLE IF NOT EXISTS markov (w1 VARCHAR(191), w2 VARCHAR(191), cnt BIGINT)'
}

class Analyzer:
  """
  Class for analyzing given input stream, and collecting results in
  database.
  Table name for data is hardcoded to markov, because sqlite3 does not
  allow parametrizing it, and I don't want to bother with sanitizing
  input.

  WARNING about the examples. For simplicity (and for doctests) the
  in-memory database is used, thus to gain access to it protected
  variable _db is used. In real use cases please make your own
  connection to the database, instead of reusing the one from the
  module.

  Example 1 (no pair appears more than once in stream):
	>>> import io, sqlite3
	>>> from analyzer import Analyzer
	>>> markov_analyzer = Analyzer(io.StringIO(u'Some test string. Second sentence.'), sqlite3, ':memory:')
	>>> markov_analyzer.parse()
	>>> cursor = markov_analyzer._db.cursor()
	>>> cursor.execute('select * from markov')
	<sqlite3.Cursor object at 0x7f4040e991f0>
	>>> cursor.fetchall()
	[(None, u'Some', 1), (u'Some', u'test', 1), (u'test', u'string.', 1), (u'string.', None, 1), (None, u'Second', 1), (u'Second', u'sentence.', 1), (u'sentence.', None, 1)]
	>>> cursor.close()
	>>> markov_analyzer.close()
	>>>

  Example 2 (with 'and test' pair appearing more than once in stream):
	>>> import io, sqlite3
	>>> from analyzer import Analyzer
	>>> markov_analyzer = Analyzer(io.StringIO(u'Test A, and test B, and test C'), sqlite3, ':memory:')
	>>> markov_analyzer.parse()
	>>> cursor = markov_analyzer._db.cursor()
	>>> cursor.execute('select * from markov')
	<sqlite3.Cursor object at 0x7f409aabb1f0>
	>>> cursor.fetchall()
	[(None, u'Test', 1), (u'Test', u'A,', 1), (u'A,', u'and', 1), (u'and', u'test', 2), (u'test', u'B,', 1), (u'B,', u'and', 1), (u'test', u'C', 1)]
	>>> cursor.close()
	>>> markov_analyzer.close()
	>>>


  :param stream input stream to process
  :param db database for results
  :param connstr connection string to use with db.connect
  """

  def __init__(self, stream, db, connstr):
    self._parser = Parser(stream, is_WORD)
    self._db = db.connect(connstr)
    self.CREATE = CREATE[db.paramstyle]
    self.UPDATE = UPDATE[db.paramstyle]
    self.INSERT = INSERT[db.paramstyle]
    self._create_table()
    self.__update_cursor = self._db.cursor()
    self.__insert_cursor = self._db.cursor()

  def __del__(self):
    try:
      self.close()
    except:
      # error here most probably means it's closed already.
      # Even if not, we just have to hope OS releases the resources.
      pass

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
    cursor.execute(self.CREATE)
    cursor.close()

  def __upsert(self, w1, w2):
    """
    Update record, or insert a new one, if no rows were updated.
    :param w1 first word
    :param w2 second word
    """
    self.__update_cursor.execute(self.UPDATE, (w1, w2))
    if self.__update_cursor.rowcount == 0:
      self.__insert_cursor.execute(self.INSERT, (w1, w2))

  def parse(self):
    """
    Parse stream into word pairs, using None for beginning and end of the sentence.
    """
    last = None
    for current in self._parser:
      self.__upsert(last, current)
      last = current
      if current[-1:] == '.':
        self.__upsert(current, None)
        last = None
    self._db.commit()
