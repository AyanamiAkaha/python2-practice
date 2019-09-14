import io, sqlite3, random

SELECT = {
  'qmark':    r'SELECT * FROM markov WHERE w1=? ORDER BY cnt',
  'numeric':  r'SELECT * FROM markov WHERE w1=:1 ORDER BY cnt',
  'named':    r'SELECT * FROM markov WHERE w1=:w1 ORDER BY cnt',
  'format':   r'SELECT * FROM markov WHERE w1=%s ORDER BY cnt',
  'pyformat': r'SELECT * FROM markov WHERE w1=%(w1)s ORDER BY cnt',
}

def random_from(wordstats):
  """
  Selects random word from the array of tuples given.
  :param wordstats array of tuples (firstword, secondword, count)
  :returns randomly selected word
  """
  total = reduce((lambda sum, (w1, w2, cnt): sum+cnt), wordstats, 0)
  rnd = random.randint(0, total-1)
  for _, w, cnt in wordstats:
    rnd -= cnt
    if rnd < 0: return w

class Generator:
  """
  Generates random texts using Markov chains principle, from given
  database.
  :param db database to use
  :param connstr connection string for the db.connect call
  """
  def __init__(self, db, connstr):
    self._db = db.connect(connstr)
    self.last_word = None
    self.SELECT = SELECT[db.paramstyle]
    self.SELECT_FIRST = 'SELECT * FROM markov WHERE w1 IS NULL ORDER BY cnt'
    self._cursor = self._db.cursor()

  def close(self):
    self._cursor.close()
    self._db.close()

  def next_word(self):
    """
    Generates next word in the chain
    """
    if self.last_word:
      self._cursor.execute(self.SELECT, (self.last_word,))
    else:
      self._cursor.execute(self.SELECT_FIRST)
    wordstat = self._cursor.fetchall()
    print wordstat
    w = random_from(wordstat)
    self.last_word = w
    return w
