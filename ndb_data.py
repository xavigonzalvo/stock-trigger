"""Definitions of data user by the deep-trading system."""

from google.appengine.ext import ndb


class ReportProperty(ndb.Model):
    last = ndb.DateProperty()


class AnalysisProperty(ndb.Model):
    date = ndb.DateProperty()
    data = ndb.BlobProperty()  # serialized protobuf


class SymbolProperty(ndb.Model):
    name = ndb.StringProperty()
    analysis = ndb.StructuredProperty(AnalysisProperty, repeated=True)
