# uix\repo_api\session_setup.py

import ssl
from requests.adapters import HTTPAdapter

class SystemTrustAdapter(HTTPAdapter):
    def __init__(self):
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Relax strict chain validation for corporate MITM proxies
        if hasattr(context, "verify_flags"):
            context.verify_flags &= ~ssl.VERIFY_X509_STRICT

        self.ssl_context = context
        super().__init__()

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)
