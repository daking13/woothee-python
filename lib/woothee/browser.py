# -*- coding: utf-8 -*-
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)

import re
from . import dataset
from . import util


def challenge_msie(ua, result):
    if 'compatible; MSIE' not in ua and 'Trident/' not in ua\
            and 'IEMobile' not in ua:
        return False
    version = dataset.VALUE_UNKNOWN
    msie = re.search(r'MSIE ([.0-9]+);', ua)
    trident = re.search(
        r'Trident\/([.0-9]+);', ua)
    tridentVersion = re.search(r' rv:([.0-9]+)', ua)
    iemobile = re.search(r'IEMobile\/([.0-9]+);', ua)

    if msie:
        version = msie.group(1)
    elif trident and tridentVersion:
        version = tridentVersion.group(1)
    elif iemobile:
        version = iemobile.group(1)

    util.update_map(result, dataset.get('MSIE'))
    util.update_version(result, version)
    return True


def challenge_yandexbrowser(ua, result):
    if 'YaBrowser/' not in ua:
        return False
    obj = re.search(r'YaBrowser/(\d+\.\d+\.\d+\.\d+)', ua)
    version = obj.group(1) if obj else dataset.VALUE_UNKNOWN
    util.update_map(result, dataset.get('YaBrowser'))
    util.update_version(result, version)
    return True


def challenge_safari_chrome(ua, result):
    if 'Safari/' not in ua:
        return False
    if 'GSA/' in ua:
        return False
    if 'Chrome' in ua and 'wv' in ua:
        return False

    version = dataset.VALUE_UNKNOWN

    # Edge
    obj = re.search(r'(?:Edge|Edg|EdgiOS|EdgA)\/([.0-9]+)', ua)
    if obj:
        version = obj.group(1)
        util.update_map(result, dataset.get('Edge'))
        util.update_version(result, version)
        return True

    obj = re.search(r'FxiOS\/([.0-9]+)', ua)
    if obj:
        version = obj.group(1)
        util.update_map(result, dataset.get('Firefox'))
        util.update_version(result, version)
        return True

    obj = re.search('(?:Chrome|CrMo|CriOS)/([.0-9]+)', ua)
    if obj:
        chromeVersion = obj.group(1)
        obj = re.search('OPR/([.0-9]+)', ua)
        if obj:
            # Opera (blink)
            version = obj.group(1)
            util.update_map(result, dataset.get('Opera'))
            util.update_version(result, version)
            return True

        # Chrome
        util.update_map(result, dataset.get('Chrome'))
        util.update_version(result, chromeVersion)
        return True

    # Safari
    obj = re.search('Version/([.0-9]+)', ua)
    if obj:
        version = obj.group(1)
    util.update_map(result, dataset.get('Safari'))
    util.update_version(result, version)
    return True


def challenge_firefox(ua, result):
    if 'Firefox/' not in ua:
        return False
    obj = re.search('Firefox/([.0-9]+)', ua)
    version = obj.group(1) if obj else dataset.VALUE_UNKNOWN
    util.update_map(result, dataset.get('Firefox'))
    util.update_version(result, version)
    return True


def challenge_opera(ua, result):
    if 'Opera' not in ua:
        return False
    obj = re.search('Version/([.0-9]+)', ua)
    version = dataset.VALUE_UNKNOWN
    if obj:
        version = obj.group(1)
    else:
        obj = re.search('Opera[/ ]([.0-9]+)', ua)
        if obj:
            version = obj.group(1)
    util.update_map(result, dataset.get('Opera'))
    util.update_version(result, version)
    return True

def challenge_in_app(ua, result):
    instagram = re.search('Instagram ([.0-9]+)', ua)
    facebook = re.search(r';(fbav|fbsv)\/([\w\.]+);', ua, re.I)
    google = re.search(r'GSA\/([\w\.]+)', ua)
    wechat = re.search(r'micromessenger\/([\w\.]+)', ua, re.I)
    other_in_app = re.search('(Pinterest|dealmoon|Weibo|AppleNews)', ua)
    if not instagram and not facebook and not google and not wechat and not other_in_app:
        return False
    if instagram:
        version = instagram.group(1)
        util.update_map(result, dataset.get('Instagram'))
        util.update_version(result, version)
        return True
    if facebook:
        version = facebook.group(2)
        util.update_map(result, dataset.get('Facebook'))
        util.update_version(result, version)
        return True
    if wechat:
        version = wechat.group(1)
        util.update_map(result, dataset.get('WeChat'))
        util.update_version(result, version)
        return True
    if google:
        version = google.group(1)
        util.update_map(result, dataset.get('GSA'))
        util.update_version(result, version)
        return True
    if other_in_app:
        app_name = other_in_app.group(1)
        util.update_map(result, dataset.get(app_name))
        util.update_version(result, dataset.VALUE_UNKNOWN)
        return True

def challenge_webview(ua, result):

    # Android(Lollipop and Above)
    if 'Chrome' in ua and 'wv' in ua:
        obj = re.search('Version/([.0-9]+)', ua)
        version = obj.group(1) if obj else dataset.VALUE_UNKNOWN
        util.update_map(result, dataset.get('Webview'))
        util.update_version(result, version)
        return True

    # iOS
    obj = re.search('iP(?:hone;|ad;|od) .*like Mac OS X', ua)
    if not obj or 'Safari/' in ua:
        return False

    obj = re.search(r'Version\/([.0-9]+)', ua)
    version = obj.group(1) if obj else dataset.VALUE_UNKNOWN
    util.update_map(result, dataset.get('Webview'))
    util.update_version(result, version)
    return True


def challenge_sleipnir(ua, result):
    if 'Sleipnir/' not in ua:
        return False
    obj = re.search('Sleipnir/([.0-9]+)', ua)
    version = obj.group(1) if obj else dataset.VALUE_UNKNOWN
    util.update_map(result, dataset.get('Sleipnir'))
    util.update_version(result, version)
    # Sleipnir's user-agent doesn't contain Windows version,
    # so put 'Windows UNKNOWN Ver'.
    # Sleipnir is IE component browser, so for Windows only.
    win = dataset.get('Win')
    util.update_category(result, win[dataset.KEY_CATEGORY])
    util.update_os(result, win[dataset.KEY_NAME])
    return True


def challenge_vivaldi(ua, result):
    if 'Vivaldi/' not in ua:
        return False

    obj = re.search('Vivaldi/([.0-9]+)', ua)
    version = obj.group(1) if obj else dataset.VALUE_UNKNOWN
    util.update_map(result, dataset.get('Vivaldi'))
    util.update_version(result, version)
    return True
