#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2019 <name of copyright holder>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

import io

def open(fname):
  """
  Opens give file as word stream.
  :param fname name of the file to open
  :returns Parser instance
  """
  return Parser(io.open(fname))

class Parser:
  """
  Class for parsing given file into words.

  Parses the given file into words, in a pull-parser way. The goal is to
  be albe to parse huge files, orstreams, that would not fit in memroy.
  Example use case is gathering statistics for a marrkov chaindatabase.

  Example 1: alphanumeric words
	>>> import io
	>>> from Parser import Parser
	>>> p=Parser(io.StringIO(u'Big black boobs!'))
	>>> p.next_word()
	u'Big'
	>>> p.next_word()
	u'black'
	>>> p.next_word()
	u'boobs'
	>>> p.next_word()
	>>> p.next_word()
	>>> p.close()

	Example 2: space-delimited words
	>>> p=Parser(io.StringIO(u'Big black boobs!'))
	>>> p.next_WORD()
	u'Big'
	>>> p.next_WORD()
	u'black'
	>>> p.next_WORD()
	u'boobs!'
	>>> p.next_WORD()
	>>> p.next_WORD()
	>>> p.close()

  :param stream stream to parse from
  """
  def __init__(self, stream):
    self._stream = stream

  def __del__(self):
    self._stream.close()

  def close(self):
    """
    closes the underlying stream.
    After close the object can no longer be used.
    """
    self._stream.close()

  def next_word(self):
    """
    Returns next word from a file stream.
    The word is a continuous alphanumeric string. Skips non-alphanumeric
    characters at the start.
    """
    word = ''
    # skip non-alphanumeric
    c=self._stream.read(1)
    while c and not c.isalnum():
      c=self._stream.read(1)
    while c.isalnum():
      word += c
      c = self._stream.read(1)
    return word or None

  def next_WORD(self):
    """
    Returns next WORD from a file stream.
    The WORD is a series of characters delimited by whitespace. Skips
    whitespace at the beginning, untif non-whitespace is found.
    """
    word = ''
    # skip non-alphanumeric
    c=self._stream.read(1)
    while c.isspace():
      c=self._stream.read(1)
    while c and not c.isspace():
      word += c
      c = self._stream.read(1)
    return word or None

