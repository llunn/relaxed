# TODO: figure out how to implement hooks
from functools import wraps
import requests
from re import sub


class User():
  class __This():
    __allowed_keys = ['session', 'db']

    def __init__(self, **kwargs):
      for k in kwargs.keys():
        if k in self.__allowed_keys:
          self.__setattr__(k, kwargs.get(k, None))

    def create(self, name, password, **kwargs):
      docid = f'org.couchdb.user:{name}'
      userdoc = {'name': name, 'password': password, 'roles': kwargs.get('roles', []), 'type': "user"}
      userdoc.update(**kwargs)
      return self.db.save_named_doc(uri_segments={'db': '_users', 'docid': docid}, data=userdoc)

    def get(self, id):
      docid = f'org.couchdb.user:{id}';
      return self.db.get_doc(uri_segments={'db': '_users', 'docid': docid})

  __self = None

  def __init__(self, **kwargs):
    if not User.__self:
      User.__self = User.__This(**kwargs)
    else:
      for k in kwargs.keys():
        self.__self.__setattr__(k, kwargs.get(k, getattr(self.__self, k)))

  def __getattr__(self, name):
    return getattr(self.__self, name)


class CouchDB():
    """
    Exposes an interface for interating with a CouchDB server's REST API.

    Usage:
      couchDb = CouchDB([username=<user>[, password=<password>][,<arg=<value>])
    """

    def __init__(self, **kwargs):
      self._context_manager = False
      self.session = Session(**kwargs)
      self.server = Server(session=self.session)
      self.db = Database(session=self.session, **kwargs)
      self.user = User(session=self.session, db=self.db)

    def __enter__(self):
      self._context_manager = True
      return self

    def __exit__(self, type, value, traceback):
      self._context_manager = False




class CouchError():
  def __init__(self, **kwargs):
    self.error = kwargs.get('error', None)
    self.reason = kwargs.get('reason', None)
    self.status_code = kwargs.get('code', None)


class InvalidKeysException(Exception):
  """The passed data contains keys that are not allowed"""
  pass

class AllowedKeys():
  SERVER__ALL_DBS__PARAMS = {'descending': bool, 'limit': int, 'skip': int,
                             'startkey': [], 'start_key': [], 'endkey': [], 'end_key': []}
  SERVER__DBS_INFO__PARAMS = {'keys': []}
  SERVER__CLUSTER_SETUP__PARAMS = {'ensure_dbs_exist': []}
  SERVER__CLUSTER_SETUP__DATA = {'action': str, 'bind_address': str,
                                 'host': str, 'port': int,
                                 'node_code': int, 'remote_node': str,
                                 'username': str, 'password': str,
                                 'remote_current_user': str, 'remote_current_password': str,
                                 'ensure_dbs_exist': [], }
  SERVER__DB_UPDATES__PARAMS = {'feed': str, 'timeout': int, 'heartbeat': int, 'since': str}
  SERVER__REPLICATE__DATA = {'cancel': bool, 'continuous': bool,
                             'create_target': bool, 'doc_ids': [],
                             'filter': str, 'proxy': str,
                             'source': {}, 'target': {}}
  SERVER__SCHEDULER_JOBS__PARAMS = {'limit': int, 'skip': int}
  SERVER__SCHEDULER_DOCS__PARAMS = {'limit': int, 'skip': int}
  SERVER__UUIDS__PARAMS = {'count': int}

  DATABASE__DB__CREATE_PARAMS = {'q': int, 'n': int}
  DATABASE__DB__SAVE__PARAMS = {'batch': str}

  VIEW__PARAMS = {'conflicts': bool, 'descending': bool,
                  'startkey': [], 'start_key': [],
                  'startkey_docid': str, 'start_key_doc_id': str,
                  'endkey': [], 'end_key': [],
                  'endkey_docid': str, 'end_key_doc_id': str,
                  'group': bool, 'group_level': int,
                  'attachments': bool, 'att_encoding_info': bool,
                  'include_docs': bool, 'inclusive_end': bool,
                  'key': [], 'keys': [[]],
                  'limit': int, 'skip': int, 'reduce': bool, 'sorted': bool,
                  'stable': bool, 'stale': str,
                  'update': str, 'update_seq': bool}
  DATABASE__ALL_DOCS__DATA = {'keys': []}
  DATABASE__ALL_DOCS_QUERIES__DATA = {'queries': []}
  DATABASE__DESIGN_DOCS_QUERIES__DATA = {'queries': []}
  DATABASE__DESIGN_DOCS__DATA = {'keys': []}
  DATABASE__LOCAL_DOCS_QUERIES__DATA = {'queries': []}
  DATABASE__BULK_GET__PARAMS = {'revs': bool}
  DATABASE__BULK_GET__DATA = {'docs': [{}]}
  DATABASE__BULK_DOCS__DATA = {'docs': [{}], 'new_edits': bool}
  DATABASE__FIND__DATA = {'selector': {}, 'limit': int, 'skip': int,
                          'sort': {}, 'fields': [], 'use_index': [], 'r': int,
                          'bookmark': str, 'update': bool,
                          'stable': bool, 'stale': str, 'execution_stats': bool}
  DATABASE__INDEX__DATA = {'index': {}, 'ddoc': str, 'name': str,
                           'type': str, 'partial_filter_selector': {}}
  DATABASE__CHANGES__PARAMS = {'doc_ids': [], 'conflicts': bool, 'descending': bool,
                               'feed': str, 'filter': str, 'heartbeat': int,
                               'include_docs': bool, 'attachments': bool, 'att_encoding_info': bool,
                               'last-event-id': int, 'limit': int, 'since': str, 'style': str,
                               'timeout': int, 'view': str, 'seq_interval': int}
  DATABASE__CHANGES__DATA = {'doc_ids': []}
  DATABASE__SECURITY__DATA = {'admins': {}, 'members': {}}
  DATABASE__DOCUMENT__PARAMS = {'attachments': bool, 'att_encoding_info': bool,
                                'atts_since': [], 'conflicts': bool, 'deleted_conflicts': bool,
                                'latest': bool, 'local_seq': bool, 'meta': bool, 'open_revs': [],
                                'rev': str, 'revs': bool, 'revs_info': bool}
  DATABASE__DOCUMENT__NAMED_DOC__PARAMS = {'rev': str, 'batch': str, 'new_edits': bool}
  DATABASE__DOCUMENT__DELETE__PARAMS = {'rev': str, 'batch': str}
  DATABASE__DOCUMENT__COPY__PARAMS = {'rev': str, 'batch': str}
  DATABASE__ATTACHMENT__GET__PARAMS = {'rev': str}
  DATABASE__ATTACHMENT__SAVE__PARAMS = {'rev': str}
  DATABASE__ATTACHMENT__INFO_PARAMS = {'rev': str}
  DATABASE__ATTACHMENT__DELETE__PARAMS = {'rev': str, 'batch': str}
  DATABASE__LOCAL_DOCS__PARAMS = {'conflicts': bool, 'descending': bool,
                                  'startkey': [], 'start_key': [],
                                  'startkey_docid': str, 'start_key_doc_id': str,
                                  'endkey': [], 'end_key': [],
                                  'endkey_docid': str, 'end_key_doc_id': str,
                                  'include_docs': bool, 'inclusive_end': bool,
                                  'key': [], 'keys': [[]],
                                  'limit': int, 'skip': int, 'update_seq': bool}
  DATABASE__LOCAL_DOCS__DATA = {'keys': []}
  DATABASE__VIEW_BY_KEY__DATA = {'keys': []}
  DATABASE__VIEW_QUERIES__DATA = {'queries': []}

class RelaxedDecorators():
  def _process_filter_format(filter_format, filter):
    if (filter_format is not None):
      for key in filter.keys():
        if key not in filter_format:
          raise InvalidKeysException("The provided filter does not meet the expected format.")

  def _build_uri(template: str, segments: dict):
    def replace_with_segment(matches):
      #  dynamic segments are expected, but not provided at all
      if segments is None and len(matches.groups()) > 0:
        identifier = matches.group(1)
        raise Exception((
          'Invalid URI. This endpoint contains dynamic segments, but none were provided.  '
          f'Expected segment definition for "{identifier}".  '
          'Did you forget to pass a uri_segments dict?'))

      # a specific segment not provided
      elif len(matches.groups()) == 1 and matches.group(1) not in segments:
        identifier = matches.group(1)
        raise Exception(f'Invalid URI. Expected a dynamic segment for "{identifier}", but none was provided.')
      else:
        return segments[matches.group(1)]

    return sub(':([\w_]+):', replace_with_segment, template)

  def endpoint(*args, **kwargs):
    endpoint = args[0]

    allowed_query_parameter_keys = kwargs.get('query_keys', None)
    allowed_data_keys = kwargs.get('data_keys', None)

    request_method = kwargs.get('method', 'get')
    request_action = getattr(requests, request_method)

    def set_endpoint(*eargs):
      fn = eargs[0]

      @wraps(fn)
      def wrapper(self, *query_params, **kwargs):
        dynamic_segments = getattr(self, '_predefined_segments', {})
        dynamic_segments.update(kwargs.get('uri_segments', {}))
        cookies = {'AuthSession': self.session.auth_token or None}
        uri = RelaxedDecorators._build_uri(endpoint, dynamic_segments)

        if ('data' in kwargs):
          RelaxedDecorators._process_filter_format(allowed_data_keys, kwargs.get('data'))

        if ('params' in kwargs):
          RelaxedDecorators._process_filter_format(allowed_query_parameter_keys, kwargs.get('params'))

        if (request_method == 'post'or request_method == 'put'):
          response = request_action(f'{self.session.address}{uri}',
                                    headers=self.session._headers,
                                    cookies=cookies,
                                    params=kwargs.get('params', None),
                                    json=kwargs.get('data'))
        elif request_method == 'head':
          response = request_action(f'{self.session.address}{uri}',
                                    headers=self.session._headers,
                                    cookies=cookies,
                                    params=kwargs.get('params', None),
                                    json=kwargs.get('data'))
          return fn(self, response.headers.get('ETag'))
        else:
          response = request_action(f'{self.session.address}{uri}',
                                    headers=self.session._headers,
                                    cookies=cookies,
                                    params=kwargs.get('params', None))

        if (response.status_code in [requests.codes['ok'], requests.codes['created'], requests.codes['accepted']]):
          self.session.set_auth_token_from_headers(response.headers)
          ret_val = response.json()
          if isinstance(ret_val, str):
            ret_val = {'data': ret_val}
        else:
          result = response.json()
          if isinstance(result, str):
            result = {'data': result}
          result['code'] = response.status_code
          ret_val = CouchError(**result)

        return fn(self, ret_val)
      return wrapper
    return set_endpoint

from .session import Session
from .server import Server
from .db import Database
