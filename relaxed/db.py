from .core import RelaxedDecorators, CouchError, AllowedKeys


class Database():
  def __init__(self, **kwargs):
    self.session = kwargs.get('session', None)
    self._db = kwargs.get('db', '_global_changes')
    self._predefined_segments = {'db': self._db}

  @RelaxedDecorators.endpoint('/:db:', method='head')
  def headers(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:', method='head')
  def exists(self, couch_data):
    """
    Convenience method

    :returns CouchError if an error occured accessing the couch api
    :returns bool True if the database exists, otherwise false.
    """
    return False if isinstance(couch_data, CouchError) else True

  @RelaxedDecorators.endpoint('/:db:')
  def get(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:', method='put', query_keys=AllowedKeys.DATABASE__DB__CREATE_PARAMS)
  def create(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:', method='delete')
  def delete(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:', method='post', query_keys=AllowedKeys.DATABASE__DB__SAVE__PARAMS)
  def save_doc(self, couch_data):
    """
    Saves a document to the specified database

    :returns CouchError if an error occured accessing the couch api
    """
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_ensure_full_commit', method='post')
  def flush(self, couch_data):
    """
    Force a manual request to commit documents created, updated, or deleted using CouchDB batch mode to persistent
    storage.

    See: http://docs.couchdb.org/en/stable/api/database/common.html#batch-mode-writes

    :returns CouchError if an error occured accessing the couch api
    """
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/:docid:', method='head', query_keys=AllowedKeys.DATABASE__DOCUMENT__PARAMS)
  def get_doc_info(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/:docid:', query_keys=AllowedKeys.DATABASE__DOCUMENT__PARAMS)
  def get_doc(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/:docid:', method='put', query_keys=AllowedKeys.DATABASE__DOCUMENT__NAMED_DOC__PARAMS)
  def save_named_doc(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/:docid:', method='delete', query_keys=AllowedKeys.DATABASE__DOCUMENT__DELETE__PARAMS)
  def delete_doc(self, couch_data):
    return couch_data

  # TODO: implement custom verb handling in endpoint decorator
  # TODO: CouchDB COPY command uses custom headers to send data...need to implement a way to handle this too
  # see https://requests.readthedocs.io/en/master/user/advanced/
  # @RelaxedDecorators.endpoint('/:db:/:docid:', method='copy', query_keys=AllowedKeys.DATABASE__DOCUMENT__COPY__PARAMS)
  # def copy_doc(self, couch_data):
  #   return couch_data

  @RelaxedDecorators.endpoint('/:db:/:docid:/:attname:', method='head', query_keys=AllowedKeys.DATABASE__ATTACHMENT__INFO_PARAMS)
  def get_attachment_info(self, couch_data):
    return couch_data

  # TODO: implement ability for endpoint to return non-json data
  @RelaxedDecorators.endpoint('/:db:/:docid:/:attname:', query_keys=AllowedKeys.DATABASE__ATTACHMENT__GET__PARAMS)
  def get_attachment(self, couch_data):
    return couch_data

  # TODO: confirm ability to pass custom headers to endpoint decorator
  @RelaxedDecorators.endpoint('/:db:/:docid:/:attname:', method='put', query_keys=AllowedKeys.DATABASE__ATTACHMENT__SAVE__PARAMS)
  def save_attachment(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/:docid:/:attname:', method='delete', query_keys=AllowedKeys.DATABASE__ATTACHMENT__DELETE__PARAMS)
  def delete_attachment(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:', method='head', query_keys=AllowedKeys.DATABASE__DOCUMENT__PARAMS)
  def get_ddoc_info(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:/_info')
  def get_ddoc_details(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:', query_keys=AllowedKeys.DATABASE__DOCUMENT__PARAMS)
  def get_ddoc(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:', method='put', query_keys=AllowedKeys.DATABASE__DOCUMENT__NAMED_DOC__PARAMS)
  def save_named_ddoc(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:', method='delete', query_keys=AllowedKeys.DATABASE__DOCUMENT__DELETE__PARAMS)
  def delete_ddoc(self, couch_data):
    return couch_data

  # TODO: implement custom verb handling in endpoint decorator
  # TODO: CouchDB COPY command uses custom headers to send data...need to implement a way to handle this too
  # see https://requests.readthedocs.io/en/master/user/advanced/
  # @RelaxedDecorators.endpoint('/:db:/_design/:docid:', method='copy', query_keys=AllowedKeys.DATABASE__DOCUMENT__COPY__PARAMS)
  # def copy_ddoc(self, couch_data):
  #   return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:/:attname:', method='head', query_keys=AllowedKeys.DATABASE__ATTACHMENT__INFO_PARAMS)
  def get_ddoc_attachment_info(self, couch_data):
    return couch_data

  # TODO: implement ability for endpoint to return non-json data
  @RelaxedDecorators.endpoint('/:db:/_design/:docid:/:attname:', query_keys=AllowedKeys.DATABASE__ATTACHMENT__GET__PARAMS)
  def get_ddoc_attachment(self, couch_data):
    return couch_data

  # TODO: confirm ability to pass custom headers to endpoint decorator
  @RelaxedDecorators.endpoint('/:db:/_design/:docid:/:attname:', method='put', query_keys=AllowedKeys.DATABASE__ATTACHMENT__SAVE__PARAMS)
  def save_ddoc_attachment(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:/:attname:', method='delete', query_keys=AllowedKeys.DATABASE__ATTACHMENT__DELETE__PARAMS)
  def delete_ddoc_attachment(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:/_view/:view:', query_keys=AllowedKeys.VIEW__PARAMS)
  def get_view(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:/_view/:view:', query_keys=AllowedKeys.VIEW__PARAMS)
  def get_view(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:/_view/:view:', method='post', data_keys=AllowedKeys.DATABASE__VIEW_BY_KEY__DATA)
  def filter_view(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design/:docid:/_view/:view:/queries', method='post', data_keys=AllowedKeys.DATABASE__VIEW_QUERIES__DATA)
  def filter_view_with_queries(self, couch_data):
    return couch_data











  @RelaxedDecorators.endpoint('/:db:/_all_docs', query_keys=AllowedKeys.VIEW__PARAMS)
  def get_docs(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_all_docs', method='post', data_keys=AllowedKeys.DATABASE__ALL_DOCS__DATA)
  def filter_docs(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_all_docs', query_keys=AllowedKeys.DATABASE__LOCAL_DOCS__PARAMS)
  def get_local_docs(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_all_docs', method='post', data_keys=AllowedKeys.DATABASE__LOCAL_DOCS__DATA)
  def get_local_docs_by_key(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_local/:docid:', query_keys=AllowedKeys.DATABASE__DOCUMENT__PARAMS)
  def get_local_doc(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_local/:docid:', method='put', query_keys=AllowedKeys.DATABASE__DOCUMENT__NAMED_DOC__PARAMS)
  def save_local_named_doc(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_local/:docid:', method='delete', query_keys=AllowedKeys.DATABASE__DOCUMENT__DELETE__PARAMS)
  def delete_local_doc(self, couch_data):
    return couch_data

  # TODO: implement custom verb handling in endpoint decorator
  # TODO: CouchDB COPY command uses custom headers to send data...need to implement a way to handle this too
  # see https://requests.readthedocs.io/en/master/user/advanced/
  # @RelaxedDecorators.endpoint('/:db:/_local/:docid:', method='copy', query_keys=AllowedKeys.DATABASE__DOCUMENT__COPY__PARAMS)
  # def copy_local_doc(self, couch_data):
  #   return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design_docs', query_keys=AllowedKeys.VIEW__PARAMS)
  def get_design_docs(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design_docs', method='post', data_keys=AllowedKeys.DATABASE__DESIGN_DOCS__DATA)
  def get_design_docs_by_key(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_all_docs/queries', method='post', data_keys=AllowedKeys.DATABASE__ALL_DOCS_QUERIES__DATA)
  def filter_docs_with_queries(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design_docs/queries', method='post', data_keys=AllowedKeys.DATABASE__DESIGN_DOCS_QUERIES__DATA)
  def filter_ddocs_with_queries(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_local_docs/queries', method='post', data_keys=AllowedKeys.DATABASE__LOCAL_DOCS_QUERIES__DATA)
  def filter_local_docs_with_queries(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_bulk_get', method='post',
                              data_keys=AllowedKeys.DATABASE__BULK_GET__DATA,
                              query_keys=AllowedKeys.DATABASE__BULK_GET__PARAMS)
  def bulk_get(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_bulk_docs', method='post', data_keys=AllowedKeys.DATABASE__BULK_DOCS__DATA)
  def bulk_save(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_find', method='post', data_keys=AllowedKeys.DATABASE__FIND__DATA)
  def find(self, couch_data):
    return couch_data

  # TODO: confirm body or query parameters.  couchdb docs suggest query parameters and not json body data
  @RelaxedDecorators.endpoint('/:db:/_index', method='post', data_keys=AllowedKeys.DATABASE__INDEX__DATA)
  def save_index(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_index', query_keys=AllowedKeys.VIEW__PARAMS)
  def get_indices(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_index/:ddoc:/json/:index:')
  def get_index(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_index/:ddoc:/json/:index:', method='delete')
  def delete_index(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_explain', method='post', data_keys=AllowedKeys.DATABASE__FIND__DATA)
  def explain(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_shards')
  def get_shards(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_shards/:shard:')
  def get_shard(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_sync_shards', method='post')
  def sync_shards(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_changes', query_keys=AllowedKeys.DATABASE__CHANGES__PARAMS)
  def get_changes(self, couch_data):
    return couch_data

    # TODO: make note in this doc string about the lack of data_keys since it supports query keys as well as find data keys
  @RelaxedDecorators.endpoint('/:db:/_changes', method='post', query_keys=AllowedKeys.DATABASE__CHANGES__PARAMS)
  def get_filtered_changes(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_compact', method='post')
  def compact(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_compact/:ddoc:', method='post')
  def compact_design_doc(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_view_cleanup', method='post')
  def flush_unused_view_cache(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_security')
  def get_security_info(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_security', method='put', data_keys=AllowedKeys.DATABASE__SECURITY__DATA)
  def set_security_info(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_purge', method='post')
  def purge(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_purged_infos_limit')
  def get_purge_tracking_limit(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_purged_infos_limit', method='put')
  def set_purge_tracking_limit(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_missing_revs', method='post')
  def check_missing_revs(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_revs_diff', method='post')
  def get_revs_diff(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_revs_limit')
  def get_revs_limit(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_revs_limit', method='put')
  def set_revs_limit(self, couch_data):
    return couch_data
