import time
import logging
from requests import (get, post, RequestException, Response)

logger: logging.Logger = logging.getLogger(__name__)

class HTTPHandler:
    get_type: str = "GET"
    post_type: str = "POST"

    def __init__(self, base_url: str = ""):
        self.base_url: str = base_url.rstrip("/")

    def get(
        self,
        endpoint: str,
        params: dict = None,
        headers: dict = None,
        timeout: int = 10
    ) -> Response:
        get_package: dict = {
            "params": params,
            "headers": headers,
            "timeout": timeout
        }
        response: Response = self._request_with_retries(endpoint, self.get_type, get_package)
        return response

    def post(
        self,
        endpoint: str,
        data: dict = None,
        json: dict = None,
        headers: dict = None,
        timeout: int = 10
    ) -> Response:
        get_package: dict = {
            "data": data,
            "json": json,
            "headers": headers,
            "timeout": timeout
        }
        response: Response = self._request_with_retries(endpoint, self.post_type, get_package)
        return response

    def _request_with_retries(
        self,
        endpoint: str,
        request_type: str,
        request_package: dict,
        max_retries: int = 3
    ) -> Response:
        url: str = f"{self.base_url}/{endpoint.lstrip('/')}"
        retry_count: int = 0
        retry_delay: int = 1
        while retry_count <= max_retries:
            try:
                logger.info(f"Attempt #{retry_count}")

                match request_type:
                    case self.get_type:
                        response: Response = get(
                            url, 
                            params=request_package["params"], 
                            headers=request_package["headers"], 
                            timeout=request_package["timeout"]
                        )

                    case self.post_type:
                        response: Response = post(
                            url, 
                            data=request_package["data"], 
                            json=request_package["json"], 
                            headers=request_package["headers"], 
                            timeout=request_package["timeout"]
                        )
    
                response.raise_for_status()
                return response
            
            except RequestException as e:
                logger.warning(f"GET request failed: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    logger.info(f"Retrying GET request to {url} ({retry_count}/{max_retries}) in {retry_delay} seconds")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error(f"Max retries reached for GET request to {url}")
                    raise
        return None
