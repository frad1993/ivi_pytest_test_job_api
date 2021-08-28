import logging
from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict


logger = logging.getLogger('test')

MAX_RESPONSE_LENGTH = 500


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class InvalidLoginException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

        self.csrf_token = None
        self.sessionid_gtp = None

    @staticmethod
    def log_pre(method, url, headers, data, expected_status):
        logger.info(f'Performing {method} request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'expected status: {expected_status}\n\n')

    @staticmethod
    def log_post(response):
        log_str = 'Got response:\n' \
                  'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n\n')
            elif logger.level == logging.DEBUG:
                logger.debug(f'{log_str}\n'
                             f'RESPONSE CONTENT: {response.text}\n\n')
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n\n')

    def _request(self, method, location, headers=None, data=None, expected_status=200, jsonify=True):
        url = urljoin(self.base_url, location)

        self.log_pre(method, url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data)
        self.log_post(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')

        if jsonify:
            json_response = response.json()
            if json_response.get('bStateError'):
                error = json_response.get('bErrorMsg', 'Unknown')
                raise ResponseErrorException(f'Request "{url}" return error "{error}"!')
            return json_response
        return response

    @property
    def post_headers(self):
        return {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    def get_token(self):
        headers = self._request('GET', self.base_url, jsonify=False).headers['Set-Cookie'].split(';')
        token_header = [h for h in headers if 'csrftoken' in h]
        if not token_header:
            raise Exception('CSRF token not found in main page headers')

        token_header = token_header[0]
        token = token_header.split('=')[-1]

        return token

    def post_login(self, user, password):
        location = '/login/'

        csrf_token = self.get_token()

        headers = self.post_headers
        headers['Cookie'] = f'csrftoken={csrf_token}'

        data = {
            'csrfmiddlewaretoken': csrf_token,
            'login': user,
            'password': password
        }

        result = self._request('POST', location, headers=headers, data=data, jsonify=False)
        try:
            response_cookies = result.headers['Set-Cookie'].split(';')
        except Exception as e:
            raise InvalidLoginException(e)

        new_csrf_token = [c for c in response_cookies if 'csrftoken' in c][0].split('=')[-1]
        sessionid_gtp = [c for c in response_cookies if 'sessionid_gtp' in c][0].split('=')[-1]

        self.session.cookies = cookiejar_from_dict({'csrftoken': new_csrf_token, 'sessionid_gtp': sessionid_gtp})
        self.csrf_token = new_csrf_token
        self.sessionid_gtp = sessionid_gtp

        return result

    def post_topic_create(self, blog_id, title, text, publish=True):
        location = f'/blog/{blog_id}/topic/create/'

        data = {
            'csrfmiddlewaretoken': self.csrf_token,
            'blog': blog_id,
            'title': title,
            'text': text,
            'publish': 'on' if publish else ''
        }

        return self._request('POST', location, headers=self.post_headers, data=data)

    def get_topic_feed(self, feed_type='all'):
        location = f'/feed/update/stream/?type={feed_type}'

        return self._request('GET', location)

    def post_topic_delete(self, topic_id):
        location = f'/blog/topic/delete/{topic_id}/'

        data = {
            'csrfmiddlewaretoken': self.csrf_token,
            'submit': 'Удалить'
        }

        return self._request('POST', location, headers=self.post_headers, data=data, jsonify=False)

    def get_topic(self, topic_id, expected_status=200):
        location = f'blog/topic/view/{topic_id}/'
        return self._request('GET', location, expected_status=expected_status, jsonify=False)

    def post_topic_vote(self, topic_id):
        location = f'/blog/topic/vote/{topic_id}/'

        data = {
            'csrfmiddlewaretoken': self.csrf_token,
            'vote': 1
        }
        return self._request('POST', location, headers=self.post_headers, data=data)