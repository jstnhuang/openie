import argparse
from .. import openie
import os.path
import pysolr

class QaExperiment:
  def __init__(self, solrUrl, inputDir, outputDir):
    self.solr = pysolr.Solr(solrUrl)
    self.inputDir = inputDir;
    self.outputDir = outputDir;

  def get_queries(self):
    queries = []
    queries_path = os.path.join(self.inputDir, 'benchmark-queries.tsv')
    queries_file = open(queries_path)
    for line in queries_file:
      columns = [
        column.strip() if column.strip() != '' else None
        for column in line.split('\t')
      ]
      arg1, rel, arg2 = columns[0], columns[1], columns[2]
      arg1_type, arg2_type = None, None
      if arg1 is not None and arg1.startswith('type:'):
        arg1_type = arg1[5:]
        arg1 = None
      if arg2 is not None and arg2.startswith('type:'):
        arg2_type = arg2[5:]
        arg2 = None
      queries.append(openie.Query(arg1=arg1, rel=rel, arg2=arg2,
        arg1_type=arg1_type, arg2_type=arg2_type))
    return queries
  
  def run(self):
    queries = self.get_queries()
    for query in queries:
      #if query.arg1 != 'Obama':
      #  continue
      results = self.solr.search(query.get_query_string())
      rlink_results = self.solr.search(query.get_query_string(True))
      print('Query: {}'.format(query.get_query_string()))
      print('Query: {}'.format(query.get_query_string(True)))
      print('{} results.'.format(len(results)))
      print('{} sentences.'.format(sum([result['size'] for result in results])))
      print('{} results with relation linking.'.format(len(rlink_results)))
      print('{} sentences with relation linking.'.format(sum(
        [result['size'] for result in rlink_results])))
      print()

def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument('solrUrl', help='URL of Solr instance to query.')
  argparser.add_argument('inputDir', help='Directory of other input files.')
  argparser.add_argument('outputDir', help='Directory to put output files.')
  args = argparser.parse_args()
  experiment = QaExperiment(args.solrUrl, args.inputDir, args.outputDir)
  experiment.run()
  
if __name__ == '__main__':
  main()
