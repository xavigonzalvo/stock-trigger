"""Definitions of data user by the deep-trading system."""

from google.appengine.ext import ndb


class ReportProperty(ndb.Model):
    # When the report was generated.
    date = ndb.DateTimeProperty(indexed=True)

    # Hard filtered good symbols.
    hard_good_symbols = ndb.StringProperty(repeated=True)

    # Medium filtered good symbols.
    medium_good_symbols = ndb.StringProperty(repeated=True)

    # Number of correct symbols analyzed.
    count_correct_analysis = ndb.IntegerProperty()

    # Number of total symbols analyzed.
    count_total = ndb.IntegerProperty()


class ReportsProperty(ndb.Model):
    # Date when symbols were processed. When generating a report,
    # this is the date referring to when the data of the symbols
    # was generated. 
    last = ndb.DateTimeProperty()


class AnalysisProperty(ndb.Model):
    # When the data was saved for this analysis.
    date = ndb.DateTimeProperty()

    # serialized protobuf
    data = ndb.BlobProperty()


class SymbolProperty(ndb.Model):
    # Name of the symbol (eg. BPI.L).
    name = ndb.StringProperty()

    # A list of analysis data.
    analysis = ndb.StructuredProperty(AnalysisProperty, repeated=True)
