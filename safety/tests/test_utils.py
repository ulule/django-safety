# -*- coding: utf-8 -*-
from safety import utils

from .base import BaseTestCase


class DeviceTest(BaseTestCase):
    def test_ie(self):
        self.assertEqual(
            'Internet Explorer, Windows XP',
            utils.get_device('Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.1; SV1; '
                   '.NET CLR 2.0.50727)'))

        self.assertEqual(
            'Internet Explorer, Windows Vista',
            utils.get_device('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; '
                   'Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322;'
                   ' InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; '
                   'MS-RTC LM 8; OfficeLiveConnector.1.4; OfficeLivePatch.1.3;'
                   ' .NET CLR 3.0.30729)'))

        self.assertEqual(
            'Internet Explorer, Windows 7',
            utils.get_device('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; '
                   'Trident/6.0)'))

        self.assertEqual(
            'Internet Explorer, Windows 8',
            utils.get_device('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; '
                   'Win64; x64; Trident/6.0)'))

        self.assertEqual(
            'Internet Explorer, Windows 8.1',
            utils.get_device('Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; '
                   '.NET4.0E; .NET4.0C; rv:11.0) like Gecko'))

    def test_apple(self):
        self.assertEqual(
            'Safari, iPad',
            utils.get_device('Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; ja-jp) '
                   'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 '
                   'Mobile/8C148 Safari/6533.18.5'))

        self.assertEqual(
            'Safari, iPhone',
            utils.get_device('Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) '
                   'AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 '
                   'Mobile/11A465 Safari/9537.53'))

        self.assertEqual(
            'Safari, OS X',
            utils.get_device('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
                   'AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 '
                   'Safari/536.26.17'))

    def test_android(self):
        # androids identify themselves as Safari to get the good stuff
        self.assertEqual(
            'Safari, Android',
            utils.get_device('Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic '
                   'Build/CRB17) AppleWebKit/528.5+ (KHTML, like Gecko) '
                   'Version/3.1.2 Mobile Safari/525.20.1'))

    def test_firefox(self):
        self.assertEqual(
            'Firefox, Windows 7',
            utils.get_device('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) '
                   'Gecko/20130328 Firefox/22.0'))

    def test_chrome(self):
        self.assertEqual(
            'Chrome, Windows 8.1',
            utils.get_device('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 ('
                   'KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'))
