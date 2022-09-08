from typing import Literal
from Crypto.Hash import MD5, SHA256, SHA512


def H(hash_cls, data):
    hasher = hash_cls.new()
    hasher.update(data.encode())
    return hasher.hexdigest()


def KD(hash_cls, secret, data):
    return H(hash_cls, secret + ":" + data)


class SHA512_256:
    @staticmethod
    def new(truncate=256):
        return SHA512.new(truncate=str(truncate))


class AuthorizationHF:
    response: str = None
    username: str = None
    realm: str = None
    uri: str = None
    qop: Literal["auth", "auth-int"] = None
    cnonce: str = None
    nc: str = None
    userhash: Literal["true", "false"] = "false"
    _hash_class: MD5

    @classmethod
    def build(
        cls,
        realm=None,
        uri=None,
        nonce=None,
        cnonce=None,
        nc=None,
        algorithm="MD5",
        qop=None,
        username=None,
        opaque=None,
        userhash=None,
        _hash_cls=MD5,
    ):
        out = AuthorizationHF()
        out.realm = realm
        out.nonce = nonce
        out.cnonce = cnonce
        out.nc = nc
        out.opaque = opaque
        out.algorithm = algorithm
        out.qop = qop
        out.username = username
        out.uri = uri
        out.opaque = opaque
        out.userhash = userhash
        if algorithm == "MD5":
            out._hash_cls = MD5
        elif algorithm == "SHA-256":
            out._hash_cls = SHA256
        elif algorithm == "SHA-512-256":
            out._hash_cls = SHA512_256

        return out

    def __str__(self):
        values = []
        if self.username:
            values.append(f'realm="{self.username}"')
        if self.realm:
            values.append(f'realm="{self.realm}"')
        if self.nonce:
            values.append(f'nonce="{self.nonce}"')
        if self.uri:
            values.append(f'uri="{self.uri}"')
        if self.response:
            values.append(f'response="{self.response}"')
        if self.cnonce:
            values.append(f'cnonce="{self.cnonce}"')
        if self.opaque:
            values.append(f'opaque="{self.opaque}"')

        if self.qop:
            values.append(f"qop={self.qop}")
        if self.nc:
            values.append(f"nc={self.nc}")
        if self.algorithm != "MD5":
            values.append(f"algorithm={self.algorithm}")
        if self.userhash is not None:
            values.append(f"userhash={self.userhash}")

        return " ".join(values)

    def create_response(self, method, password):
        A1 = ":".join([self.username, self.realm, password])
        if self.qop is None or self.qop == "auth":
            A2 = ":".join([method, self.uri])

        if self.userhash == "true":
            print("username(hashed) =", H(self._hash_cls, self.username + ":" + self.realm))
        return KD(
            self._hash_cls,
            H(self._hash_cls, A1),
            ":".join([self.nonce, self.nc, self.cnonce, self.qop, H(self._hash_cls, A2)]),
        )


class ChallengeHF:
    realm: str = None
    domain: str = None
    nonce: str = None
    opaque: str = None
    stale: str = None
    algorithm: Literal["MD5", "SHA-256", "SHA=512-256"] = "MD5"
    qop: Literal["auth", "auth-int"] = None
    charset: Literal["UTF-8"] = None
    userhash: Literal["true", "false"] = None

    @classmethod
    def build(
        cls,
        realm=None,
        domain=None,
        nonce=None,
        opaque=None,
        stale=None,
        algorithm="MD5",
        qop=None,
    ):
        out = ChallengeHF()
        out.realm = realm
        out.domain = domain
        out.nonce = nonce
        out.opaque = opaque
        out.stale = stale
        out.algorithm = algorithm
        out.qop = qop

        return out

    def __str__(self):
        values = []
        if self.realm:
            values.append(f'realm="{self.realm}"')
        if self.domain:
            values.append(f'domain="{self.realm}"')
        if self.nonce:
            values.append(f'nonce="{self.nonce}"')
        if self.opaque:
            values.append(f'opaque="{self.opaque}"')

        if self.stale:
            values.append(f"stale={self.stale}")
        if self.algorithm != "MD5":
            values.append(f"algorithm={self.algorithm}")

        return " ".join(values)


if __name__ == "__main__":

    ch = ChallengeHF.build(
        realm="http-auth@example.org",
        qop="auth, auth-int",
        algorithm="SHA-256",
        nonce="7ypf/xlj9XXwfDPEoM4URrv/xwf94BcCAzFZH4GiTo0v",
        opaque="FQhe/qaU925kfnzjCev0ciny7QMkPqMAFRtzCUYo5tdS",
    )

    print(f"ch = 'Digest {ch}'")

    auth = AuthorizationHF.build(
        realm="http-auth@example.org",
        uri="/dir/index.html",
        algorithm="MD5",
        nonce="7ypf/xlj9XXwfDPEoM4URrv/xwf94BcCAzFZH4GiTo0v",
        nc="00000001",
        cnonce="f2/wE4q74E6zIJEtWaHKaf5wv/H5QzzpXusqGemxURZJ",
        qop="auth",
        opaque="FQhe/qaU925kfnzjCev0ciny7QMkPqMAFRtzCUYo5tdS",
        username="Mufasa",
    )

    expect_response = "8ca523f5e9506fed4657c9700eebdbec"
    auth.response = auth.create_response("GET", "Circle of Life")
    assert auth.response == expect_response

    print(80 * "=")
    print(f"auth = 'Digest {auth}'")

    auth = AuthorizationHF.build(
        realm="http-auth@example.org",
        uri="/dir/index.html",
        algorithm="SHA-256",
        nonce="7ypf/xlj9XXwfDPEoM4URrv/xwf94BcCAzFZH4GiTo0v",
        nc="00000001",
        cnonce="f2/wE4q74E6zIJEtWaHKaf5wv/H5QzzpXusqGemxURZJ",
        qop="auth",
        opaque="FQhe/qaU925kfnzjCev0ciny7QMkPqMAFRtzCUYo5tdS",
        username="Mufasa",
    )

    expect_response = "753927fa0e85d155564e2e272a28d1802ca10daf4496794697cf8db5856cb6c1"
    auth.response = auth.create_response("GET", "Circle of Life")
    assert auth.response == expect_response

    print(80 * "=")
    print(f"auth = 'Digest {auth}'")

    auth = AuthorizationHF.build(
        username="Jäsøn Doe",
        realm="api@example.org",
        uri="/doe.json",
        algorithm="SHA-512-256",
        nonce="5TsQWLVdgBdmrQ0XsxbDODV+57QdFR34I9HAbC/RVvkK",
        nc="00000001",
        cnonce="NTg6RKcb9boFIAS3KrFK9BGeh+iDa/sm6jUMp2wds69v",
        qop="auth",
        opaque="HRPCssKJSGjCrkzDg8OhwpzCiGPChXYjwrI2QmXDnsOS",
        userhash="true",
    )

    expect_response = "3798d4131c277846293534c3edc11bd8a5e4cdcbff78b05db9d95eeb1cec68a5"
    auth.response = auth.create_response("GET", "Secret, or not?")
    assert auth.response == expect_response

    print(80 * "=")
    print(f"auth = 'Digest {auth}'")
