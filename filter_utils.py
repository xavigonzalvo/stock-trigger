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
from absl import logging


def _second_order_root(poly):
  """Returns the positive root of a 2nd-order polynomial."""
  a = poly.coef[0]
  b = poly.coef[1]
  c = poly.coef[2]
  if 4 * a * c > b * b:
    return 0.0
  return - b + math.sqrt(b * b - 4 * a * c) / (2 * a)


def filter(data, data_filter):
  """Decides whether to filter a symbol.

  Returns:
    True if the symbol has to be filtered out.
  """
  for word in data_filter["to_filter"]:
    if word.lower() in data["name"].lower():
      logging.debug("Symbol filtered")
      return True

  if "market_cap" in data:
    if (data["market_cap"] < data_filter["min_market_cap"] or
        data["market_cap"] > data_filter["max_market_cap"]):
      logging.debug("Filtered by market cap")
      return True
  else:
    if data_filter["filter_if_no_market_cap"]:
      logging.debug("Filter if not market cap")
      return True

  if (data["mean"] - data["std"] < 0 and
      not data_filter["negative_gradient_variation"]):
    logging.debug("Filtered by negative gradient variation")
    return True  # mean variation can go negative
  if data["mean"] < data_filter["min_mean"]:
    logging.debug("Filtered by minimum mean")
    return True  # if increases less than X% in average
  for poly in data["poly"]:
    if poly["order"] == 1:
      if poly["coef"][0] < data_filter["min_linear_gradient"]:
        logging.debug("Filtered by min_linear_gradient")
        return True
      if poly["coef"][1] < data_filter["min_linear_offset"]:
        logging.debug("Filtered by min_linear_offset")
        return True
      #for coef in poly.coef:
      #    if coef < data_filter.min_linear_gradient:
      #        return True
      #    break
    if poly["order"] == 2:
      if poly["convex"] != data_filter["convex"]:
        logging.debug("Filtered by convex")
        return True
      if (x_convex_poly in data_filter and
          _second_order_root(poly) < data_filter["x_convex_poly"]):
        logging.debug("Filtered by second order root")
        return True

  # Remove penny shares.
  if min_value in data_filter and mean_value in data:
    penny_share = data["mean_value"] < data_filter["min_value"]
    if penny_share:
      logging.debug("Filtered by penny share")
    return penny_share

  return False
