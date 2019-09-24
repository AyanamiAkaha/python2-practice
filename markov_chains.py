#!/usr/bin/env python
from __future__ import print_function
import io, sys, sqlite3
import codecs
import argparse

import markov

def analyze(args):
  custom=False
  if(args.instream):
    in_stream = io.open(args.instream)
    custom=True
  else:
    in_stream = codecs.getreader('utf8')(sys.stdin)
  analyzer = markov.Analyzer(in_stream, sqlite3, args.db)
  analyzer.parse()
  analyzer.close()
  if(custom): in_stream.close()

def _increment(args, chars):
  if not chars: return 0.0
  if args.unit == 'words':
    return 1
  elif args.unit == 'bytes' or args.unit == 'b':
    return chars+1 # +1 for the space
  elif args.unit == 'kilobytes' or args.unit == 'kb':
    return (chars/1024.0)
  elif args.unit == 'megabytes' or args.unit == 'mb':
    return (chars/1024.0/1024.0)
  raise 'Unknown unit '+args.units

def generate(args):
  count = 0.0
  generator = markov.Generator(sqlite3, args.db)
  custom = False
  if(args.outstream):
    out_stream = io.open(args.outstream, mode='w')
    custom=True
  else:
    out_stream = codecs.getwriter('utf8')(sys.stdout)
  while count < args.count: # generator ends sequence on None
    for w in generator:
      if not w: continue
      out_stream.write(w.encode('utf8') + u' ')
      count += _increment(args, len(w))
      if(count > args.count): break
    out_stream.write(u'\n')
  if(custom): out_stream.close()

def main():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument(
    '--db',
    dest='db',
    default='markov.db',
    help='Database file to use',
    metavar='database'
  )
  arg_parser.add_argument(
    '--in',
    dest='instream',
    default=None,
    help='input file to use instead of stdin',
    metavar='input file'
  )
  arg_parser.add_argument(
    '--out',
    dest='outstream',
    default=None,
    help='output file to use instead of stdout',
    metavar='output file'
  )
  subp = arg_parser.add_subparsers()
  analyze_parser = subp.add_parser('analyze')
  analyze_parser.set_defaults(command=analyze)
  generate_parser = subp.add_parser('generate')
  generate_parser.set_defaults(command=generate)
  generate_parser.add_argument('count', type=int)
  generate_parser.add_argument('unit', choices=['words',
                                                'bytes', 'b',
                                                'kilobytes', 'kb',
                                                'megabytes', 'mb'])
  args = arg_parser.parse_args()
  args.command(args)

if __name__ == '__main__':
  main()
