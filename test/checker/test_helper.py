# coding=utf-8
import pytest
import logging
from data_packer import checker
from data_packer import err
from data_packer.err import DataPackerCheckError


log = logging.getLogger()

class TestIPChecker:
    """
    testcase, see also: https://en.wikipedia.org/wiki/Module:IPAddress/testcases
    """
    valid_ipv4 = [
        '200.200.200.200',
        '255.255.255.255',
        '0.0.0.0',
    ]

    invalid_ipv4 = [
        ' 200.200.200.200',  # whitespace not currently allowed
        '200.200.200.200 ',  # whitespace not currently allowed
        '200.200.256.200',
        '200.200.200.200.',
        '200.200.200',
        '200.200.200.2d0',
        # '00.00.00.00',  # according to talkpage, leading zeroes unacceptable.
        # '100.100.020.100',  # according to talkpage, leading zeroes unacceptable.
        '-1.0.0.0',
        '200000000000000000000000000000000000000000000000000000000000000000000000000000.200.200.200',
        '00000000000005.10.10.10',
    ]

    valid_ipv6 = [
        '::',  # unassigned IPv6 address
        '::1',  # loopback IPv6 address
        '0::',  # another name for unassigned IPv6 address
        '0::0',  # another name for unassigned IPv6 address
        '00AB:0002:3008:8CFD:00AB:0002:3008:8CFD',  # full length
        '00ab:0002:3008:8cfd:00ab:0002:3008:8cfd',  # lowercase
        '00aB:0002:3008:8cFd:00Ab:0002:3008:8cfD',  # mixed case
        'AB:02:3008:8CFD:AB:02:3008:8CFD',  # abbreviated
        'AB:02:3008:8CFD::02:3008:8CFD',  # correct use of ::
    ]

    invalid_ipv6 = [
        '00AB:00002:3008:8CFD:00AB:0002:3008:8CFD',  # at most 4 digits per segment
        ':0002:3008:8CFD:00AB:0002:3008:8CFD',  # can't remove all 0s from first segment unless using ::
        '00AB:0002:3008:8CFD:00AB:0002:3008:',  # can't remove all 0s from last segment unless using ::
        'AB:02:3008:8CFD:AB:02:3008:8CFD:02',  # too long
        'AB:02:3008:8CFD::02:3008:8CFD:02',  # too long
        'AB:02:3008:8CFD::02::8CFD',  # can't have two ::s
        'GB:02:3008:8CFD:AB:02:3008:8CFD',  # Invalid character G
        '2:::3',  # illegal: three colons
    ]

    def test_valid_ipv4(self):
        for ip in self.valid_ipv4:
            log.debug('now check ip: %s', ip)
            checker.ipv4_checker.verify('', '', ip)

    def test_invalid_ipv4(self):
        for ip in self.invalid_ipv4:
            log.debug('now check ip: %s', ip)
            with pytest.raises(DataPackerCheckError):
                checker.ipv4_checker.verify('', '', ip)

    def test_valid_ipv6(self):
        for ip in self.valid_ipv6:
            log.debug('now check ip: %s', ip)
            checker.ipv6_checker.verify('', '', ip)

    def test_invalid_ipv6(self):
        for ip in self.invalid_ipv6:
            log.debug('now check ip: %s', ip)
            with pytest.raises(DataPackerCheckError):
                checker.ipv6_checker.verify('', '', ip)


class TestEmailChecker:
    """
    test case, see also: https://blogs.msdn.microsoft.com/testing123/2009/02/06/email-address-test-cases/
    """
    valid_emails = [
        'email@domain.com',  # Valid email
        'firstname.lastname@domain.com',  # Email contains dot in the address field
        'email@subdomain.domain.com',  # Email contains dot with subdomain
        'firstname+lastname@domain.com',  # Plus sign is considered valid character
        'email@123.123.123.123',  # Domain is valid IP address
        'email@[123.123.123.123]',  # Square bracket around IP address is considered valid
        # '“email”@domain.com',  # Quotes around email is considered valid
        '1234567890@domain.com',  # Digits in address are valid
        'email@domain-one.com',  # Dash in domain name is valid
        '_______@domain.com',  # Underscore in the address field is valid
        'email@domain.name',  # '.name is valid Top Level Domain name
        'email@domain.co.jp',  # Dot in Top Level Domain name also considered valid (use co.jp as example here)
        'firstname-lastname@domain.com',  # Dash in address field is valid
        'email@111.222.333.44444',  # Invalid IP format, BUT can be gregard as valid domain
    ]
    invalid_emails = [
        'plainaddress',  # Missing @ sign and domain
        '#@%^%#$@#$@#.com',  # Garbage
        '@domain.com',  # Missing username
        'Joe Smith <email@domain.com>',  # Encoded html within email is invalid
        'email.domain.com',  # Missing @
        'email@domain@domain.com',  # Two @ sign
        '.email@domain.com',  # Leading dot in address is not allowed
        'email.@domain.com',  # Trailing dot in address is not allowed
        'email..email@domain.com',  # Multiple dots
        'あいうえお@domain.com',  # Unicode char as address
        'email@domain.com (Joe Smith)',  # Text followed email is not allowed
        'email@domain',  # Missing top level domain (.com/.net/.org/etc)
        'email@-domain.com',  # Leading dash in front of domain is invalid
        # 'email@domain.web',  # '.web is not a valid top level domain
        'email@domain..com',  # Multiple dot in the domain portion is invalid
    ]

    def test_valid_email(self):
        for email in self.valid_emails:
            log.debug('Current test valid email: %s', email)
            checker.email_checker.verify('', '', email)

    def test_invalid_email(self):
        for email in self.invalid_emails:
            with pytest.raises(DataPackerCheckError):
                log.debug('Current test invalid email: %s', email)
                checker.email_checker.verify('', '', email)


class TestURLChecker:
    valid_urls = [
        'http://192.168.0.1',
        'HTTP://192.168.0.1',
        'hTTp://192.168.0.1',
        'HttP://192.168.0.1',
        'https://192.168.0.1',
        'ftp://192.168.0.1',
        'ftps://192.168.0.1',
        'http://example.com/path#fragment',
        'http://example.com/path?a=b#fragment',
        'http://example.com/path?key=value#fragment',
        'http://example.com/path?key=value&a=b#fragment',
        'http://example.com/?z=1&a=1&k=1&d=1',
        'http://example.com',
    ]

    invalid_urls = [
        'hiwpefhipowhefopw',  # MissingSchema
        'localhost:3128',  # InvalidSchema
        'localhost.localdomain:3128/',  # InvalidSchema
        '10.122.1.1:3128/',  # InvalidSchema
        'http://',  # InvalidURL
        'http://0.0.0.0/get/test case',
    ]

    def test_valid_url(self):
        for url in self.valid_urls:
            log.debug('now test url: %s', url)
            checker.url_checker.verify('', '', url)

    def test_invalid_url(self):
        for url in self.invalid_urls:
            with pytest.raises(DataPackerCheckError):
                log.debug('now test url: %s', url)
                checker.url_checker.verify('', '', url)