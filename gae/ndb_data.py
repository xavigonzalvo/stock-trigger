"""Definitions of data used by the deep-trading system.

The MIT License (MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
