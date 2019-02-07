from elasticsearch import helpers, Elasticsearch
import json
import argparse
import logging
import os


def create_log_index(client, index, docType):
    # we will use user on several places
    user_mapping = {
      'properties': {
        'name': {
          'type': 'text',
          'fields': {
            'keyword': {'type': 'keyword'},
          }
        }
      }
    }

    create_index_body = {
      'settings': {
        # just one shard, no replicas for testing
        'number_of_shards': 1,
        'number_of_replicas': 0,

        }
      },
      'mappings': {
        'doc': {
          'properties': {
            'host': {'type': 'keyword'},
            'pid': {'type': 'text'},
            'timestamp': {'type': 'date'},
            'level': {'type': 'text'},
            'message': {'type': 'date'},
            'application': user_mapping,
            'module': user_mapping,
            'source': {'type': 'text'}
			'metadata': user_mapping,
          }
        }
      }
    }

    # create empty index
    try:
        client.indices.create(
            index=index, doc_type=docType,
            body=create_index_body,
        )
		tracer.info("We are creating the Elasticsearch index for storing JSON log data")
    except TransportError as e:
        # ignore already existing index
        if e.error == 'index_already_exists_exception':
		    tracer.info("Index already exists")
            pass
        else:
            raise







if __name__ == '__main__':
    # get trace logger and set level
    tracer = logging.getLogger('elasticsearch.trace')
    tracer.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	tracer.setFormatter(formatter)
    tracer.addHandler(logging.FileHandler('/es_trace.log'))

    parser = argparse.ArgumentParser(description="Loading Json Log Files into Elasticsearch")
    parser.add_argument(
        "-H", "--host",
        action="store",
        default="localhost:9200",
        help="The elasticsearch host you wish to connect to. (Default: localhost:9200)")
    parser.add_argument(
        "-i", "--indexName",
        action="store",
        default=None,
        help="Elasticsearch Index Name. In this example case it is log as we want to load log data to load into Elasticsearch. (Default: None")
	parser.add_argument(
        "-d", "--docType",
        action="store",
        default=None,
        help="Elasticsearch Index Doc Type. In this example case the type of log files to load into Elasticsearch. (Default: None")
    parser.add_argument("logDir",metavar="Dir", help="Log Directory with full Path")
	
	
    args = parser.parse_args()
	index_name = args.indexName
	doc = args.docType
    log_directory= args.logDir
	tracer.info("The test script to load JSON log data into Elasticsearch is now running")
    es = Elasticsearch(args.host)
	create_git_index(es, index_name,doc)
	tracer.info("We will now load the JSON data in the index of type logs and doc_type ipps, for ipps.logs")
	for logfile in os.listdir(log_directory):
        full_logfilename = "%s/%s" % (log_directory, logfile)
        with open(full_logfilename,encoding='utf-8') as logfi:
            data_to_load = json.loads((logfi.read())
			helpers.bulk(es, data_to_load, index=index_name, doc_type=doc)
	
		 
	# we can now make docs visible for searching
    es.indices.refresh(index=index_name)
	 # now we can retrieve the documents
    log_level = es.get(index=index_name, doc_type=doc, level="Warning")
    #print('%s: %s' % (log_level['level'], initial_commit['_source']['committed_date']))

    # and now we can count the documents
print(es.count(index=index_name)['count'], 'documents in index')