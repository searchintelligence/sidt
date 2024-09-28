from datetime import datetime
import sys
import time
from typing import Optional, Union
import tls_client.response
import tqdm
import tls_client
from sidt.utils.io import CLIF
from sidt.utils import proxy

class Scraper:
    def __init__(self, auto_vpn: bool = True, retry_on_429: bool = True) -> None:
        self.tls_session = self.new_tls_session()
        self.tqdm = tqdm.tqdm
        self.auto_vpn = auto_vpn
        self.retry_on_429 = retry_on_429
        self.os = sys.platform
        self.log(f"Scraper Initialised [OS:{self.os}] [VPN:{self.auto_vpn}]", level=0)

    def __del__(self) -> None:
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def new_tls_session(self) -> tls_client.Session:
        return tls_client.Session(
            client_identifier="chrome128",
            random_tls_extension_order=True
        )
        
    
    def refresh_tls_session(self) -> None:
        self.tls_session = self.new_tls_session()

    def vpn_connect(self, country: Optional[str] = None) -> None:
        match self.os:
            case "darwin":
                self.log("Auto VPN not supported on MacOS", level=2)
            case "win32":
                with proxy.Nord() as nordvpn:
                    nordvpn.connect()
                self.log("VPN connected for Windows", level=-1)
            case "linux":
                self.log("VPN connected for Linux", level=-1)
            case _:
                self.log("Unsupported OS, must be MacOS, Windows, or Linux", level=2)
                raise OSError("Unsupported OS")

    def request(
            self,
            method: str,
            url: str,
            params: Optional[dict] = None,
            data: Optional[Union[str, dict]] = None,
            headers: Optional[dict] = None,
            cookies: Optional[dict] = None,
            json: Optional[dict] = None,
            allow_redirects: Optional[bool] = False,
            insecure_skip_verify: Optional[bool] = False,
            timeout_seconds: Optional[int] = None,
            proxy: Optional[dict] = None,
            attempt: int = 1,
            retry_timer: int = 600
        ) -> tls_client.response.Response:
        response = self.tls_session.execute_request(
            url=url,
            method=method,
            headers=headers,
            cookies=cookies,
            params=params,
            json=json,
            allow_redirects=allow_redirects,
            data=data,
            insecure_skip_verify=insecure_skip_verify,
            timeout_seconds=timeout_seconds,
            proxy=proxy
        )
        match response.status_code:
            case 200:
                self.log(f"200 Response from {url}", level=-1)
            case 429:
                if self.retry_on_429:
                    self.log(f"429 Response from {url} on attempt {attempt}, retrying in {retry_timer/60} seconds", level=1)
                    time.sleep(retry_timer)
                    return self.request(
                        method=method,
                        url=url,
                        params=params,
                        data=data,
                        headers=headers,
                        cookies=cookies,
                        json=json,
                        allow_redirects=allow_redirects,
                        insecure_skip_verify=insecure_skip_verify,
                        timeout_seconds=timeout_seconds,
                        proxy=proxy,
                        attempt=attempt+1
                    )
                else:
                    self.log(f"429 Response from {url}", level=2)
            case _:
                self.log(f"{response.status_code} Response from {url}", level=2)

    def log(self, message: str, level: int = 0) -> None:
        now = datetime.now().strftime("%H:%M")
        match level:
            case -1:
                # Success
                self.tqdm.write(CLIF.fmt(f"█ {now} ▏ {message}", CLIF.Color.GREEN))
            case 0:
                # Info
                self.tqdm.write(f"█ {now} ▏ {message}")
            case 1:
                # Warning
                self.tqdm.write(CLIF.fmt(f"█ {now} ▏ {message}", CLIF.Color.YELLOW))
            case 2:
                # Error
                self.tqdm.write(CLIF.fmt(f"█ {now} ▏ {message}", CLIF.Color.RED))
            case _:
                raise ValueError("Incorrect log level")