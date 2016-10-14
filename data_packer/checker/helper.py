# coding=utf-8
import re
from six.moves.urllib.parse import urlsplit, urlunsplit
from ._base import BaseChecker, CheckerWrapper, ReChecker, TypeChecker
from .. import constant, err
from ..util import ip

class URLChecker(ReChecker):
    ul = '\u00a1-\uffff'  # unicode letters range (must be a unicode string, not a raw string)

    # IP patterns
    ipv4_re = r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}'
    ipv6_re = r'\[[0-9a-f:\.]+\]'  # (simple regex, validated later)

    # Host patterns
    hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
    # Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
    domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
    tld_re = (
        '\.'  # dot
        '(?!-)'  # can't start with a dash
        '(?:[a-z' + ul + '-]{2,63}'  # domain label
                         '|xn--[a-z0-9]{1,59})'  # or punycode label
                         '(?<!-)'  # can't end with a dash
                         '\.?'  # may have a trailing dot
    )
    host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'
    schemes = ['http', 'https', 'ftp', 'ftps']

    def __init__(self):
        super(URLChecker, self).__init__(
            r'^(?:[a-z0-9\.\-\+]*)://'  # scheme is validated separately
            r'(?:\S+(?::\S*)?@)?'  # user:pass authentication
            r'(?:' + self.ipv4_re + '|' + self.ipv6_re + '|' + self.host_re + ')'
            r'(?::\d{2,5})?'  # port
            r'(?:[/?#][^\s]*)?'  # resource path
            r'\Z', re.IGNORECASE
        )

    def verify(self, src_name, dst_name, value):
        # Check first if the scheme is valid
        scheme = value.split('://')[0].lower()
        if scheme not in self.schemes:
            raise err.DataPackerCheckError(
                src_name, dst_name, value, self,
                'Invalid scheme({})'.format(scheme)
            )

        # Then check full URL
        try:
            super(URLChecker, self).verify(src_name, dst_name, value)
        except err.DataPackerCheckError as e:
            # Trivial case failed. Try for possible IDN domain
            if value:
                scheme, netloc, path, query, fragment = urlsplit(value)

                try:
                    netloc = netloc.encode('idna').decode('ascii')  # IDN -> ACE
                except UnicodeError:  # invalid domain part
                    raise e
                url = urlunsplit((scheme, netloc, path, query, fragment))
                super(URLChecker, self).verify(src_name, dst_name, url)
            else:
                raise
        else:
            # Now verify IPv6 in the netloc part
            host_match = re.search(r'^\[(.+)\](?::\d{2,5})?$', urlsplit(value).netloc)
            if host_match:
                potential_ip = host_match.groups()[0]
                ipv6_checker.verify(potential_ip)
            url = value

        # The maximum length of a full host name is 253 characters per RFC 1034
        # section 3.1. It's defined to be 255 bytes or less, but this includes
        # one byte for the length of the name and one byte for the trailing dot
        # that's used to indicate absolute names in DNS.
        if len(urlsplit(value).netloc) > 253:
            raise err.DataPackerCheckError(
                src_name, dst_name, value, self,
                'netloc is too long'
            )


class EmailChecker(BaseChecker):
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE
    )
    domain_regex = re.compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
        re.IGNORECASE)
    literal_regex = re.compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r'\[([A-f0-9:\.]+)\]\Z',
        re.IGNORECASE)
    domain_whitelist = ['localhost']

    def verify(self, src_name, dst_name, value):
        if not value or '@' not in value:
            raise err.DataPackerCheckError(
                src_name, dst_name, value, self,
                'email is null or NOT contain @'
            )

        user_part, domain_part = value.rsplit('@', 1)

        if not self.user_regex.match(user_part):
            raise err.DataPackerCheckError(
                src_name, dst_name, value, self,
                'Invalid user part({})'.format(user_part)
            )

        if (domain_part not in self.domain_whitelist and
                not self.validate_domain_part(domain_part)):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode('idna').decode('ascii')
                if self.validate_domain_part(domain_part):
                    return
            except UnicodeError:
                pass

            raise err.DataPackerCheckError(
                src_name, dst_name, value, self,
                'Invalid domain part({})'.format(domain_part)
            )

    def validate_domain_part(self, domain_part):
        if self.domain_regex.match(domain_part):
            return True

        literal_match = self.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match.group(1)
            try:
                ipv46_checker.verify('', '', ip_address)
                return True
            except err.DataPackerCheckError:
                pass
        return False


class IPChecker(BaseChecker):


    def __init__(self, version):
        """

        :param version: 请使用constant.IP_VERSION.
        :type version: int
        """
        super(IPChecker, self).__init__()
        if version not in (constant.IP_VERSION.BOTH,
                           constant.IP_VERSION.IPV4,
                           constant.IP_VERSION.IPV6):
            raise err.DataPackerProgramError('Invalid ip version({})'.format(version))

        self._version = version

    def verify(self, src_name, dst_name, value):
        if self._version == constant.IP_VERSION.IPV4:
            ipv4_checker.verify(src_name, dst_name, value)
        elif self._version == constant.IP_VERSION.IPV6:
            ipv6_checker.verify(src_name, dst_name, value)
        else:  # BOTH
            try:
                ipv4_checker.verify(src_name, dst_name, value)
            except err.DataPackerCheckError:
                ipv6_checker.verify(src_name, dst_name, value)


email_checker = EmailChecker()
url_checker = URLChecker()
ipv4_checker = CheckerWrapper(lambda src_name,dst_name,value: ip.is_valid_ipv4(value))
ipv6_checker = CheckerWrapper(lambda src_name,dst_name,value: ip.is_valid_ipv6(value))
ipv46_checker = IPChecker(constant.IP_VERSION.BOTH)
text_checker = TypeChecker((str, unicode))