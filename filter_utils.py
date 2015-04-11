"""Defines utils to filter symbols.

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

import math


def SecondOrderRoot(poly):
    """Returns the positive root of a 2nd-order polynomial."""
    a = poly.coef[0]
    b = poly.coef[1]
    c = poly.coef[2]
    if 4 * a * c > b * b:
        return 0.0
    return - b + math.sqrt(b * b - 4 * a * c) / (2 * a)


def Filter(data, data_filter):
    """Decides whether to filter a symbol.

    Returns:
      True if the symbol has to be filtered out.
    """
    for word in data_filter.codeword:
        if word.lower() in data.name.lower():
            return True

    if data.HasField("market_cap"):
        if (data.market_cap < data_filter.min_market_cap or
            data.market_cap > data_filter.max_market_cap):
            return True
    else:
        if data_filter.filter_if_no_market_cap:
            return True

    if data.mean - data.std < 0 and not data_filter.negative_gradient_variation:
        return True  # mean variation can go negative
    if data.mean < data_filter.min_mean:
        return True  # if increases less than X% in average
    for poly in data.poly:
        if poly.order == 1:
            if poly.coef[0] < data_filter.min_linear_gradient:
                return True
            if poly.coef[1] < data_filter.min_linear_offset:
                return True
            #for coef in poly.coef:
            #    if coef < data_filter.min_linear_gradient:
            #        return True
            #    break
        if poly.order == 2:
            if poly.convex != data_filter.convex:
                return True
            if (data_filter.HasField('x_convex_poly') and
                SecondOrderRoot(poly) < data_filter.x_convex_poly):
                return True

    # Remove penny shares.
    if data_filter.HasField('min_value') and data.HasField('mean_value'):
        return data.mean_value < data_filter.min_value

    return False
