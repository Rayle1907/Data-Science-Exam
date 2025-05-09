import requests, os, importlib, inspect
from .exceptions import HTTP400Error, HTTP401Error, HTTP403Error, HTTP404Error, HTTP429Error, HTTP500Error, HTTP503Error, HTTP504Error, HTTPUnknownError

class API:

    def __init__(self, client_id, client_secret):

        """ API Keys """
        self.client_id      = client_id         # <--- self.client_id
        self.client_secret  = client_secret     # <--- self.client_secret
        self.access_token   = None              # <--- self.access_token

        """ API URLs for regions (US, EU, KR, TW) """
        self.api_url        = 'https://{0}.api.blizzard.com{1}'
        self.oauth_url      = 'https://{0}.battle.net{1}'

        """ API URLs for regions (CN) """
        self.api_url_cn     = 'https://gateway.battlenet.com.cn{0}'
        self.oauth_url_cn   = 'https://www.battlenet.com.cn{0}'

        """ Session """
        self.session        = requests.Session()

    def format_url(self, region, api, format_url='api'):
        """
        It takes a region, an api, and a format_url, and returns a url

        :param region: The region of the server you want to connect to
        :param api: The API you want to call
        :param format_url: This is the type of URL you want to format, defaults to api (optional) Options: api, oauth
        :return: The url is being returned.
        """

        if format_url == 'api':
            if region == 'cn':
                url = self.api_url_cn.format(api)
            else:
                url = self.api_url.format(region, api)

        elif format_url == 'oauth':
            if region == 'cn':
                url = self.oauth_url_cn.format(api)
            else:
                url = self.oauth_url.format(region, api)

        else:
            raise ValueError('format_url must be either api or oauth')

        return url

    def get_client_token(self, region):
        """
        It takes no parameters, and returns the access token

        :return: The access token is being returned.
        """
        url = self.format_url(region, '/oauth/token', 'oauth')
        data = {
            'grant_type': 'client_credentials',
        }
        response = self.session.post(url, data=data, auth=(self.client_id, self.client_secret))

        return self.response_handler(response)

    def response_handler(self, response):
        """
        It takes a response object, and returns the response object's json() method

        :param response: The response object returned by the request
        :return: The response.json() method will convert the JSON string into a Python dictionary.
        """

        if response.status_code == 400:
            raise HTTP400Error(response.status_code, response.text)
        elif response.status_code == 401:
            raise HTTP401Error(response.status_code, response.text)
        elif response.status_code == 403:
            raise HTTP403Error(response.status_code, response.text)
        elif response.status_code == 404:
            raise HTTP404Error(response.status_code, response.text)
        elif response.status_code == 429:
            raise HTTP429Error(response.status_code, response.text)
        elif response.status_code == 500:
            raise HTTP500Error(response.status_code, response.text)
        elif response.status_code == 503:
            raise HTTP503Error(response.status_code, response.text)
        elif response.status_code == 504:
            raise HTTP504Error(response.status_code, response.text)
        elif response.status_code != 200:
            raise HTTPUnknownError(response.status_code, response.text)
        else:
            return response.json()

    def request_handler(self, url, region, query_params):

        if self.access_token is None:
            client_token = self.get_client_token(region)
            self.access_token = client_token['access_token']

        if query_params.get('access_token') is None:
            query_params['access_token'] = self.access_token
        self.session.headers.update({ "Authorization": f'Bearer {self.access_token}'})
        response = self.session.get(url, params=query_params)

        return self.response_handler(response)

    def get_api(self, **kwargs):
        """
        It takes a region, an api, and query_params, and returns the response

        :param region: The region of the server you want to connect to
        :param api: The API you want to call
        :param query_params: The query parameters you want to pass to the API (optional)
        :return: The response is being returned.
        """

        region          = kwargs.get('region')  or 'us'
        api             = kwargs.get('api')     or None
        query_params    = kwargs.get('query_params') or None

        if query_params is None:
            query_params = {}

        if 'access_token' not in query_params or query_params['access_token'] is None:
            query_params['access_token'] = self.access_token

        if 'locale' not in query_params:
            query_params['locale'] = ''
        elif query_params['locale'] is None:
            query_params['locale'] = ''

        if api is None:
            raise ValueError('api cannot be None')

        query_params['namespace'] = '{}-{}'.format(query_params['namespace'], region)

        url = self.format_url(region, api)

        return self.request_handler(url, region, query_params)

    def get_oauth(self, region, api, query_params=None):
        """
        It takes a region, an api, and query_params, and returns the response

        :param region: The region of the server you want to connect to
        :param api: The API you want to call
        :param query_params: The query parameters you want to pass to the API (optional)
        :return: The response is being returned.
        """
        if query_params is None:
            query_params = {}

        url = self.format_url(region, api, 'oauth')

        return self.request_handler(url, region, query_params)