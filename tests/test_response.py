import pytest
from six.moves.http_client import BadStatusLine
from six import BytesIO
from wex.response import Response, DEFAULT_READ_SIZE


with_content_length = b'''{protocol_version} {code} {reason}\r
Content-length: {content_length}\r
\r
{content}'''

without_content_length = b'''HTTP/1.1 200 OK\r
\r
{content}'''

content = b'HELLO'


def build_response(content, response=with_content_length, **kw):

    fmt = {
        'content': content,
        'content_length': len(content),
        'protocol_version': 'HTTP/1.1',
        'code': 200,
        'reason': 'OK',
    }

    for k in fmt:
        if k in kw:
            fmt[k] = kw.pop(k)

    response_bytes = response.format(**fmt)
    return Response.from_readable(BytesIO(response_bytes), **kw)


def test_read():
    response = build_response(content)
    assert response.read() == content
    assert response.geturl() == None
    # the other attributes don't have accessors
    assert response.protocol == 'HTTP'
    assert response.version == (1, 1)
    assert response.code == 200
    assert response.reason == 'OK'
    assert response.request_url == None
    assert response.schedule == None


def test_read_seek_read():
    response = build_response(content)
    assert response.read() == content
    response.seek(0) == content
    assert response.read() == content


def test_unexpected_keyword_argument():
    with pytest.raises(ValueError):
        build_response(content, foo='bar')


def test_read_no_content_length():
    response = build_response(content, without_content_length)
    assert response.read() == content


def test_read_negative_content_length():
    response = build_response(content, content_length='-1')
    assert response.read() == content


def test_read_non_integer_content_length():
    response = build_response(content, content_length='X')
    assert response.read() == content


def test_read_large_content():
    large_content = 'X' * DEFAULT_READ_SIZE * 2
    response = build_response(large_content, without_content_length)
    assert response.read() == large_content


def test_read_non_integer_code():
    with pytest.raises(BadStatusLine):
        build_response(content, code='X')


def test_read_bad_protocol_version():
    with pytest.raises(BadStatusLine):
        build_response(content, protocol_version='HTTP/X')


def test_items_from_readable():
    readable = BytesIO(b'FTP/1.0 200 OK\r\n\r\nhello')
    def extractor(src):
        yield (src.read(),)
    items = list(Response.items_from_readable(extractor, readable))
    assert items == [('hello',)]