# onelogin-userinfo-filter

OneLoginのUserInfoエンドポイントにアクセスしてユーザ情報を取得する[Pate](https://pypi.org/project/Paste/)向けのfilter。

## ユースケース

[OpenStack Keystone](https://docs.openstack.org/keystone/latest/)の認証プラグインとして[IFCA/keystoneauth-oidc](https://github.com/IFCA/keystoneauth-oidc)を使いIdPとしてOneLoginを利用すると、Keystone側にOneLoginのユーザ情報が渡らない。onelogin-userinfo-filterを使うことで、Keystoneにログインしたユーザの情報を渡すことができる。

## 使い方

### Keystoneコントローラ

インストール

```
pip install --upgrade git+https://github.com/buty4649/onelogin-userinfo-filter
```

keystone-paste.iniに以下の設定を入れる

```diff
  [pipeline:api_v3]
- pipeline = cors sizelimit http_proxy_to_wsgi osprofiler url_normalize request_id build_auth_context token_auth json_body ec2_extension_v3 s3_extension service_v3
+ pipeline = cors sizelimit http_proxy_to_wsgi osprofiler url_normalize request_id build_auth_context token_auth onelogin json_body ec2_extension_v3 s3_extension service_v3

+ [filter:onelogin]
+ use = egg:onelogin_userinfo_filter#userinfo
```

keystone.confに以下の設定を入れる

```
[onelogin]
issuer = https://pepabo.onelogin.com/oidc/2
userinfo_endpoint = https://pepabo.onelogin.com/oidc/2/me
prefix = ONELOGIN_
```

Apache2を再起動する

```
sudo systemctl restart apache2
```

### openstackコマンド

プラグインのインストール

```
pip install https://github.com/IFCA/keystoneauth-oidc
```

トークンの発行

```
openstack --os-auth-url https://keystone.example.org:5000/v3 \
    --os-auth-type v3oidc \
    --os-identity-provider <identity-provider> \
    --os-protocol <protocol> \
    --os-project-name <project> \
    --os-project-domain-id <project-domain> \
    --os-identity-api-version 3 \
    --os-openid-scope "openid profile email" \
    token issue
```
