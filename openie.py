import openie.rlinking as rlinking

class Query:
  """Not a fully featured class, represents an Open IE query.
  """
  def __init__(self, arg1=None, rel=None, arg2=None, arg1_type=None,
      arg2_type=None, arg1_entity=None, arg2_entity=None):
    self.arg1 = arg1
    self.rel = rel
    self.arg2 = arg2
    self.arg1_type = arg1_type
    self.arg2_type = arg2_type
    self.arg1_entity = arg1_entity
    self.arg2_entity = arg2_entity
    self.rlinker = rlinking.RelationLinker()

  def __repr__(self):
    items = [
      '{}={}'.format(k, v)
      for (k, v) in self.__dict__.items()
      if v is not None and k != 'rlinker'
    ]
    return ', '.join(items)

  def get_query_string(self, rlinking=False):
    """Assumes all fields are normalized."""
    query_parts = []
    if self.arg1 is not None:
      query_parts.append('+arg1: ("{}")'.format(self.arg1))
    if self.rel is not None:
      query_part = '+(rel: ("{}")'.format(self.rel)
      if rlinking:
        relation_links = self.rlinker.get_relation_links(self.rel)
        if len(relation_links) != 0:
          rlink_string = ' OR '.join(['"{}"'.format(x) for x in relation_links])
          query_part += ' OR rel_link_id: ({})'.format(rlink_string)
      query_part += ')'
      query_parts.append(query_part)
    if self.arg2 is not None:
      query_parts.append('+arg2: ("{}")'.format(self.arg2))
    if self.arg1_type is not None:
      query_parts.append('+arg1_types: ("{}")'.format(self.arg1_type))
    if self.arg2_type is not None:
      query_parts.append('+arg2_types: ("{}")'.format(self.arg2_type))

    return ' '.join(query_parts)
