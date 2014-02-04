

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
    return False
