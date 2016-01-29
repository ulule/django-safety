# -*- coding: utf-8 -*-
from django.utils.translation import ugettext

from ua_parser import user_agent_parser

from . import app_settings
from . import utils
from .compat import GeoIP


def remote_addr_ip(request):
    """
    This is for the development setup.
    """
    return request.META.get('REMOTE_ADDR') or None


def x_forwarded_ip(request):
    """
    Amazon ELB stores the IP in the HTTP_X_FORWARDED_FOR META attribute.
    It is realiably the first one of the IP adresses sent and can be
    trusted (eg.: cannot be spoofed) Warning: This might not be true for
    other load balancers
    This function assumes that your Nginx is configured with:
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    """
    ip_address_list = request.META.get('HTTP_X_FORWARDED_FOR')

    if ip_address_list:
        ip_address_list = ip_address_list.split(',')
        return ip_address_list[0]


def real_ip(request):
    """
    Behind a Wsgi (Nginx) server.
    """
    return request.META.get('HTTP_X_REAL_IP') or None


def device(request):
    """
    Default device resolver using ua-parser.
    """
    ua = request.META.get('HTTP_USER_AGENT', '')
    parsed = user_agent_parser.Parse(ua)

    ua_parsed = (ugettext('unknown browser'), parsed['user_agent'])
    os_parsed = (ugettext('unknown system'), parsed['os'])

    infos = []
    for unknown, dct in (ua_parsed, os_parsed):
        d = dct.copy()

        family = d.pop('family')
        if family is None or family == 'Other':
            infos.append(unknown)
            continue

        version = '.'.join([d.get(k) for k in ('major', 'minor', 'patch') if d.get(k) is not None])
        if version:
            family = '%s %s' % (family, version)
        infos.append(family)

    return ' - '. join(infos)


def location(request):
    """
    Transform an IP address into an approximate location.
    """
    ip = utils.resolve(app_settings.IP_RESOLVER, request)

    try:
        location = GeoIP() and GeoIP().city(ip)
    except:
        # Handle 127.0.0.1 and not found IPs
        return ugettext('unknown')

    if location and location['country_name']:
        if location['city']:
            return '%s, %s' % (location['city'], location['country_name'])
        else:
            return location['country_name']

    return ugettext('unknown')
