from unittest.mock import AsyncMock, patch
from fetcher import UrlFetcher, load_urls
import aiohttp
import pytest


@pytest.mark.asyncio
async def test_fetch_url_succes():
    fetcher = UrlFetcher(max_count_requests=2)
    with patch("aiohttp.ClientSession") as mock_client:
        mock_session = mock_client.return_value
        mock_session.__aenter__.return_value = mock_session

        mock_response = AsyncMock()
        mock_response.text.return_value = (
            "test content"
        )
        mock_session.get.return_value.__aenter__.return_value = mock_response

        result = await fetcher.fetch_url(mock_session, 'http://example.ru')

        assert result == 'test content'


@pytest.mark.asyncio
async def test_fetch_url_error():
    fetcher = UrlFetcher(max_count_requests=2)
    with patch("aiohttp.ClientSession") as mock_client:
        mock_session = mock_client.return_value
        mock_session.__aenter__.return_value = mock_session

        mock_session.get.side_effect = aiohttp.ClientError("Connection error")

        result = await fetcher.fetch_url(mock_session, 'http://example.ru')

        assert result == ''


@pytest.mark.asyncio
async def test_fetch_and_analyze():
    fetcher = UrlFetcher(max_count_requests=2)
    html_content = ("<html><body><p>Hellofsdfsfd worsfdfsld world!</p>"
                    "<div>Мама мыла раму раму раму рама</div>"
                    "<script>var a = 1; for (let i=0; i < 9; i++)"
                    "{}</script></body></html>")
    with patch.object(fetcher, "fetch_url",
                      return_value=html_content):
        result = await fetcher.fetch_and_analyze(None, 'http://example.ru', 1)
        assert result == ("URL: http://example.ru\nТоп 1 частых слов: " +
                          "{'раму': 3}")


def test_load_urls():
    expected_output = ['https://simple.wikipedia.org/wiki/JavaScript',
                       'https://ru.wikipedia.org/wiki/python',
                       'https://simple.wikipedia.org/wiki/apple']
    result = load_urls("./07/test_urls.txt")
    assert result == expected_output
