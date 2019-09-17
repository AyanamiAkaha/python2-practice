from __future__ import print_function
import io, sys
import codecs
import argparse

import markov

def analyze(args):
  #TODO prepare args
  if(args.instream):
    in_stream = io.open(args.instream)
    custom=True
  else:
    in_stream = codecs.getreader('utf8')(sys.stdins)
  analyzer = markov.Analyzer(in_stream, sqlite3, args.db)
  analyzer.parse()
  analyzer.close()
  if(custom): in_stream.close()

def _inc_count(args, counter, chars):
  if args.units == 'words':
    return counter+1
  elif args.units == 'bytes' or args.units == 'b':
    return counter+chars+1 # +1 for the space
  elif args.units == 'kilobytes' or args.units == 'kb':
    return counter + (chars/1024.0)
  elif args.units == 'megabytes' or args.units == 'mb':
    return counter + (chars/1024.0/1024.0)
  raise 'Unknown unit '+args.units

def parse(args):
  count = 0.0
  generator = markov.Generator(sqlite, args.db)
  for w in generator:
    # TODO handle --out
    print(w+' ')
    count += _inc_count(args, count, len(w))
    if(count > args.count): break
  # TODO close out file if needed

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
