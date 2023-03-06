from oslo_log import log
from keystone.common import wsgi
import keystone.conf
from keystone.conf import cfg

import requests

CONF = keystone.conf.CONF
LOG = log.getLogger(__name__)

class OneloginUserinfo(wsgi.Middleware):
    def __init__(self, app):
      super(OneloginUserinfo, self).__init__(app)

      CONF.register_opt(cfg.StrOpt("issuer"), group="onelogin")
      CONF.register_opt(cfg.StrOpt("userinfo_endpoint"), group="onelogin")
      CONF.register_opt(cfg.StrOpt("prefix", default="ONELOGIN_"), group="onelogin")

      self.issuer = CONF.onelogin.issuer
      self.userinfo_endpoint = CONF.onelogin.userinfo_endpoint
      self.prefix = CONF.onelogin.prefix

    def process_request(self, request):
      envs = request.environ
      if self._check_auth_by_onelogin(envs):
        auth_header = envs["HTTP_AUTHORIZATION"]
        headers = {"Authorization": auth_header}
        resp = requests.get(self.userinfo_endpoint, headers=headers)
        if resp.status_code != 200:
          LOG.error("invalid response. url:%(url)s status_code:%(status_code)s text:%(text)s", 
            {"url": resp.url, "status_code": resp.status_code, "text": resp.text})
        else:
          userinfo = {}
          for key, value in resp.json().items():
            if isinstance(value, dict):
              for k, v in value.items():
                name = "%s%s_%s" % (self.prefix, key, k)
                userinfo[name] = v
            else:
              name = "%s%s" % (self.prefix, key)
              userinfo[name] = value
          LOG.debug("userinfo: %s", userinfo)
          request.environ.update(userinfo)

    def _check_auth_by_onelogin(self, envs):
      return "HTTP_OIDC_ISS" in envs and envs["HTTP_OIDC_ISS"] == self.issuer
