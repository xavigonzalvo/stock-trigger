import gae_config
import alpha_finance_fetcher
import iexcloud_finance_fetcher


class FinanceFetcherFactory(object):

  @staticmethod
  def create():
    if gae_config.FINANCE_FETCHER == "alpha":
      return alpha_finance_fetcher.FinanceFetcher(
          api_key=gae_config.ALPHA_ADVANTAGE_API,
          iexcloud_token=gae_config.IEXCLOUD_TOKEN
      )
    elif gae_config.FINANCE_FETCHER == "iexcloud":
      return iexcloud_finance_fetcher.FinanceFetcher(
          api_key=gae_config.IEXCLOUD_TOKEN
      )
