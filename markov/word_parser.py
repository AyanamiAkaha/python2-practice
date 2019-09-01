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

def is_word(c):
  """
  :param c character to check
  :returns True if c is alphanumeric
  """
  return c.isalnum()

def is_WORD(c):
  """
  :param c character to check
  :returns True if c is not whitespace
  """
  return c and not c.isspace()

class Parser:
  """
  Class for parsing given file into words.

  Parses the given file into words, in a pull-parser way. The goal is to
  be albe to parse huge files, orstreams, that would not fit in memroy.
  Example use case is gathering statistics for a marrkov chaindatabase.

  Example 1: alphanumeric words
  >>> import io
  >>> from word_parser import Parser
  >>> p=Parser(io.StringIO(u'some text stream.'))
  >>> for w in p:
  ...   print w
  ...
  some
  text
  stream
  >>> p.close()

  Example 2: space-delimited words
  >>> import io
  >>> from word_parser import *
  >>> p=Parser(io.StringIO(u'Some test, String stream.'))
  >>> p=Parser(io.StringIO(u'Some test, String stream.'), is_WORD)
  >>> for w in p:
  ...   print w
  ...
  Some
  test,
  String
  stream.
  >>> p.close()

  :param stream stream to parse from
  :param word_char_cb = is_word callback returning true for a characters to be considered words.
  """

  def __init__(self, stream, word_char_cb = is_word):
    self._stream = stream
    self.word_char_callback = word_char_cb

  def __del__(self):
    self._stream.close()

  def __iter__(self):
    return self

  def __next__(self):
    return self.next()

  def close(self):
    """
    closes the underlying stream.
    After close the object can no longer be used.
    """
    self._stream.close()

  def next(self):
    """
    Returns next word from a file stream.
    The word is a continuous alphanumeric string. Skips non-alphanumeric
    characters at the start.
    """
    word = ''
    # skip non-alphanumeric
    c=self._stream.read(1)
    while c and not self.word_char_callback(c):
      c=self._stream.read(1)
    while self.word_char_callback(c):
      word += c
      c = self._stream.read(1)
    if not word:
      raise StopIteration
    return word

