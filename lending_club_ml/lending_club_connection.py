from itertools import cycle

from cytoolz.dicttoolz import merge
import requests

from config import API_CONFIG


class LendingClubConnection(object):
    """
    Main class for interacting for interacting with Lending Club.

    Parameters
    ----------

    logger : `Logger <http://docs.python.org/2/library/logging.html>`_
        A python logger used to get debugging output from this module.

    authorization: HMAC authorization provided by lendingclub

    Examples
    --------

    """

    base_url = '/'.join([
        API_CONFIG['base_url'],
        API_CONFIG['version']
    ])

    def __init__(self, investor_id=None, authorization=None, logger=None):
        self.__auth = authorization
        self.__investor_id = investor_id
        self.logger = logger

    def __log(self, log):
        if self.logger is not None:
            self.logger.info(log)

    def build_url(self, path):
        """
        Build a LendingClub URL from a URL path (without the domain).

        Parameters
        ----------
        path : string
            The path part of the URL after the domain. i.e. 'https://api.lending_club_ml.com/api/'
        """
        url = '/'.join([self.base_url, path])
        return url

    def request(self, url, method, data=None, params=None, headers=None, json=None):
        header = {'Authorization': self.__auth}
        if headers is not None:
            header = merge(header, headers)

        try:
            url = self.build_url(url)
            method = method.upper()
            self.__log('{0} request to: {1}'.format(method, url))
            request = requests.request(
                method=method,
                url=url,
                data=data,
                json=json,
                params=params,
                headers=header
            )
            self.__log('Status code: {0}'.format(request.status_code))
            return request
        except:
            raise Exception('{0} request failed to: {1}'.format(method, url))

    def get_listed_loans(self, showAll=True):
        req = self.request(method='GET', url='loans/listing', params={'showAll': showAll})
        return req

    def get_balance(self):
        req = self.request(
            method='GET', url='accounts/{}/availablecash'.format(self.__investor_id)
        )
        return req

    def get_loans_owned(self):
        req = self.request(
            method='GET', url='accounts/{}/notes'.format(self.__investor_id)
        )
        return req

    def submit_order(self, loan_ids, loan_amounts, portfolio_id, safe_mode=True):
        if not safe_mode:
            order = Order(
                loan_amounts=loan_amounts,
                loan_ids=loan_ids,
                portfolio_id=portfolio_id,
                investor_id=self.__investor_id
            )
            print order.construct_json()
            # req=self.request(method='POST',
            #                  url='accounts/{}/orders'.format(self.__investor_id),
            #                  json=order.construct_json())

            req=self.request(url='accounts/{}/orders'.format(self.__investor_id), method='POST', json=order.construct_json())

            return req


class Order(object):
    def __init__(self, loan_amounts, loan_ids, investor_id, portfolio_id):
        self.loan_amounts = loan_amounts
        self.loan_ids = loan_ids
        self.investor_id = investor_id
        self.portfolio_id = portfolio_id

    def construct_json(self):
        assert isinstance(self.portfolio_id, int)
        return {'aid': self.investor_id,
                'orders':[{'loanId': i, 'requestedAmount': a, 'portfolioId': self.portfolio_id}
                          for i, a in zip(self.loan_ids, self.loan_amounts)]}

