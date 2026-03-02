import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

RETRY_EXCEPTIONS = (
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.ConnectTimeout,
    httpx.RemoteProtocolError,
    httpx.NetworkError,
)


retry_harvey_call = retry(
    retry=retry_if_exception_type(RETRY_EXCEPTIONS),
    wait=wait_exponential(min=30, max=45),
    stop=stop_after_attempt(3),
    reraise=True,
)
