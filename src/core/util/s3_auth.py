# link https://gist.github.com/pk5ls20/3081ac14286842da31fdf187bbd5ffef

import hmac
import hashlib
import datetime
import urllib.parse
from httpx import Request as httpxRequest


class FakeRequest:
    def __init__(self, method: str, url: str, headers: dict, content: bytes):
        self.method = method
        self.url = url
        self.headers = headers
        self.content = content


class S3RequestsAuth:
    def __init__(self,
                 access_key: str,
                 secret_access_key: str,
                 endpoint: str,
                 region: str,
                 bucket: str,
                 service: str = "s3",
                 token: str = None,
                 checksum_payload: bool = True):
        self.aws_bucket = bucket
        self.aws_access_key = access_key
        self.aws_secret_access_key = secret_access_key
        self.aws_endpoint = endpoint
        self.aws_region = region
        self.service = service
        self.aws_token = token
        self.checksum_payload = checksum_payload

    def __call__(self, req: httpxRequest | FakeRequest) -> httpxRequest | FakeRequest:
        _time = datetime.datetime.utcnow()
        amz_date = _time.strftime('%Y%m%dT%H%M%SZ')
        datestamp = _time.strftime('%Y%m%d')
        credential_scope = f"{datestamp}/{self.aws_region}/{self.service}/aws4_request"
        canonical_headers, signed_headers = self._make_headers(req, amz_date, method="header")
        aws_headers = self._sign_detail(req, amz_date, datestamp, credential_scope,
                                        canonical_headers, signed_headers, method="header")
        canonical_headers_dict = {line.split(':', 1)[0]: line.split(':', 1)[1].strip()
                                  for line in canonical_headers.strip().split('\n')}
        req.headers.update(aws_headers | canonical_headers_dict)
        return req

    def presign(self, url: str, expires: int = 86400) -> str:
        _time = datetime.datetime.utcnow()
        amz_date = _time.strftime('%Y%m%dT%H%M%SZ')
        datestamp = _time.strftime('%Y%m%d')
        credential_scope = f"{datestamp}/{self.aws_region}/{self.service}/aws4_request"
        fake_req = FakeRequest(
            method="GET",
            url=f"{url}?"
                f"X-Amz-Algorithm=AWS4-HMAC-SHA256&"
                f"X-Amz-Credential={self.aws_access_key}/{credential_scope}&"
                f"X-Amz-Date={amz_date}&"
                f"X-Amz-Expires={expires}&"
                f"X-Amz-SignedHeaders=host",
            headers={
                'x-amz-expires': str(expires),
            },
            content=b""
        )
        canonical_headers, signed_headers = self._make_headers(fake_req, amz_date, method="param")
        aws_param = self._sign_detail(fake_req, amz_date, datestamp, credential_scope,
                                      canonical_headers, signed_headers, method="param")
        return f"{url}?{aws_param}"

    def _sign_detail(self, req: httpxRequest | FakeRequest, amz_date: str, datestamp: str,
                     credential_scope: str, canonical_headers: str, signed_headers: str, method: str) -> str | dict:
        # step1
        date_key = self.hmac_sha256(f"AWS4{self.aws_secret_access_key}".encode(), datestamp)
        # step2
        date_region_key = self.hmac_sha256(date_key, self.aws_region)
        # step3
        date_region_service_key = self.hmac_sha256(date_region_key, self.service)
        # step4
        signing_key = self.hmac_sha256(date_region_service_key, 'aws4_request')
        # step5
        (algorithm, request_date_time,
         credential_scope, hashed_canonical_request) = self._create_string_to_sign(req,
                                                                                   amz_date,
                                                                                   credential_scope,
                                                                                   canonical_headers,
                                                                                   signed_headers).values()
        string_to_sign = self.hmac_sha256(signing_key,
                                          f"{algorithm}\n{request_date_time}"
                                          f"\n{credential_scope}\n{hashed_canonical_request}")
        # step6
        signature = string_to_sign.hex()
        if method == "header":
            return {
                'Authorization': f"AWS4-HMAC-SHA256 Credential={self.aws_access_key}/{credential_scope},"
                                 f"SignedHeaders={signed_headers},Signature={signature}",
            }
        if method == "param":
            return (f"X-Amz-Algorithm={algorithm}&"
                    f"X-Amz-Credential={self._make_uri_encode(f'{self.aws_access_key}/{credential_scope}')}&"
                    f"X-Amz-Date={request_date_time}&"
                    f"X-Amz-Expires={req.headers['x-amz-expires']}&"
                    f"X-Amz-SignedHeaders={signed_headers}&"
                    f"X-Amz-Signature={signature}")
        raise NotImplementedError(f"Unknown method {method}")

    def _canonical_request(self, req: httpxRequest | FakeRequest, canonical_headers: str, signed_headers: str) -> str:
        # step1
        http_method = req.method.upper()
        # step2
        _urllib_url = urllib.parse.urlparse(str(req.url))
        canonical_uri = f"{'/' if _urllib_url.path == '' else self._make_uri_encode(_urllib_url.path, is_key=True)}"
        # step3
        _canonical_query_string = _urllib_url.query
        canonical_query_string = self._make_canonical_query_string(_canonical_query_string)
        # step4
        if self.checksum_payload and not isinstance(req, FakeRequest):
            hashed_payload = hashlib.sha256(req.content).hexdigest()
        else:
            hashed_payload = 'UNSIGNED-PAYLOAD'
        # finally
        return (f"{http_method}\n{canonical_uri}\n{canonical_query_string}"
                f"\n{canonical_headers}\n{signed_headers}\n{hashed_payload}")

    def _create_string_to_sign(self, req: httpxRequest | FakeRequest, amz_date: str, credential_scope: str,
                               canonical_headers: str, signed_headers: str) -> dict:
        algorithm = "AWS4-HMAC-SHA256"
        request_date_time = amz_date
        hashed_canonical_request = hashlib.sha256(
            self._canonical_request(req, canonical_headers, signed_headers).encode()
        ).hexdigest()
        return {
            'algorithm': algorithm,
            'request_date_time': request_date_time,
            'credential_scope': credential_scope,
            'hashed_canonical_request': hashed_canonical_request
        }

    @staticmethod
    def _make_uri_encode(path: str, is_key: bool = False) -> str:
        # noinspection SpellCheckingInspection
        safe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
        if is_key:
            safe += "/"
        return urllib.parse.quote(path, safe=safe).replace(' ', '%20')

    def _make_canonical_query_string(self, query_string: str) -> str:
        query_params = urllib.parse.parse_qs(query_string, keep_blank_values=True)
        encoded_params = sorted(
            (self._make_uri_encode(key), self._make_uri_encode(value[0]))
            for key, value in query_params.items()
        )
        return '&'.join(f"{key}={value}" for key, value in encoded_params)

    def _make_headers(self, req: httpxRequest | FakeRequest, amz_date: str, method: str) -> tuple[str, str]:
        # Only need to sign headers with prefix 'x-amz-' and 'host'
        sign_headers = {
            'host': urllib.parse.urlparse(str(req.url)).netloc.lower(),
        }
        if method == "header":
            sign_headers.update(
                {
                    'x-amz-date': amz_date,
                    'x-amz-content-sha256': self._make_amz_content_sha256(req.content),
                    **{k: v for k, v in req.headers.items() if k.lower().startswith('x-amz')}
                }
            )
        if self.aws_token:
            sign_headers['x-amz-security-token'] = self.aws_token
        canonical_headers = ''.join(
            sorted(f"{key.lower()}:{value.strip()}\n" for key, value in sign_headers.items())
        )
        signed_headers = ';'.join(
            sorted(key.lower() for key, value in sign_headers.items())
        )
        return canonical_headers, signed_headers

    def _make_amz_content_sha256(self, content: bytes) -> str:
        if self.checksum_payload:
            return hashlib.sha256(content).hexdigest()
        return 'UNSIGNED-PAYLOAD'

    @staticmethod
    def hmac_sha256(key, msg):
        return hmac.new(key, msg.encode(), hashlib.sha256).digest()

    def resolve_endpoint(self):
        parsed_url = urllib.parse.urlparse(self.aws_endpoint)
        if self.aws_bucket in parsed_url.netloc.split('.'):
            return self.aws_endpoint
        else:
            return f"{self.aws_endpoint}/{self.aws_bucket}"