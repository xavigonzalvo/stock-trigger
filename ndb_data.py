"""Definitions of data user by the deep-trading system."""

from google.appengine.ext import ndb


class ReportProperty(ndb.Model):
    # Date when symbols were processed. When generating a report,
    # this is the date referring to when the data of the symbols
    # was generated. 
    last = ndb.DateProperty()


class AnalysisProperty(ndb.Model):
    # When the data was saved for this analysis.
    date = ndb.DateProperty()

    # serialized protobuf
    data = ndb.BlobProperty()


class SymbolProperty(ndb.Model):
    # Name of the symbol (eg. BPI.L).
    name = ndb.StringProperty()

    # A list of analysis data.
    analysis = ndb.StructuredProperty(AnalysisProperty, repeated=True)
