# -*- coding: utf-8 -*-
from __future__ import (division, print_function,
                        absolute_import, unicode_literals)

import re
from . import dataset
from . import util


def challenge_windows(ua, result):
    if 'Windows' not in ua:
        return False

    # Xbox Series
    if 'Xbox' in ua:
        if 'Xbox; Xbox One)' in ua:
            util.update_map(result, dataset.get("XboxOne"))
        else:
            util.update_map(result, dataset.get("Xbox360"))
        # overwrite browser detections as appliance
        return True

    data = dataset.get('Win')
    obj = re.search('Windows ([ .a-zA-Z0-9]+)[;\\)]', ua)
    if not obj:
        # Windows, but version unknown
        util.update_category(result, data[dataset.KEY_CATEGORY])
        util.update_os(result, data[dataset.KEY_NAME])
        return True

    version = obj.group(1)
    winphone_regex = re.compile(r"^Phone(?: OS)? ([.0-9]+)")
    winphone_matched = winphone_regex.search(version)

    if version == 'NT 10.0':
        data = dataset.get('Win10')
    elif version == 'NT 6.3':
        data = dataset.get('Win8.1')
    elif version == 'NT 6.2':
        data = dataset.get('Win8')
    elif version == 'NT 6.1':
        data = dataset.get('Win7')
    elif version == 'NT 6.0':
        data = dataset.get('WinVista')
    elif version == 'NT 5.1':
        data = dataset.get('WinXP')
    elif winphone_matched:
        version = winphone_matched.group(1)
        data = dataset.get('WinPhone')
    elif version == 'NT 5.0':
        data = dataset.get('Win2000')
    elif version == 'NT 4.0':
        data = dataset.get('WinNT4')
    elif version == '98':
        # wow, WinMe is shown as 'Windows 98; Win9x 4.90', fxxxk
        data = dataset.get('Win98')
    elif version == '95':
        data = dataset.get('Win95')
    elif version == 'CE':
        data = dataset.get('WinCE')

    util.update_category(result, data[dataset.KEY_CATEGORY])
    util.update_os(result, data[dataset.KEY_NAME])
    util.update_os_version(result, version)
    return True


def challenge_osx(ua, result):
    if 'Mac OS X' not in ua:
        return False
    data = dataset.get('OSX')
    version = None
    if 'like Mac OS X' in ua:
        if 'iPad;' in ua:
            data = dataset.get('iPad')
        elif 'iPod;' in ua:
            data = dataset.get('iPod')
        elif 'iPhone' in ua:
            data = dataset.get('iPhone')

        regex = re.compile(
            r"; CPU(?: iPhone)? OS (\d+_\d+(?:_\d+)?) like Mac OS X")
        m = regex.search(ua)
        if m:
            version = m.group(1).replace('_', '.')
    else:
        regex = re.compile(r"Mac OS X (10[._]\d+(?:[._]\d+)?)(?:\)|;)")
        m = regex.search(ua)
        if m:
            version = m.group(1).replace('_', '.')

    util.update_category(result, data[dataset.KEY_CATEGORY])
    util.update_os(result, data[dataset.KEY_NAME])
    if version:
        util.update_os_version(result, version)

    return True


def challenge_linux(ua, result):
    if 'Linux' not in ua:
        return False

    data = None
    os_version = None
    tablet_regexes = [
        re.compile(r"android.+;\s(pixel c)[\s)]", flags=re.I),
        re.compile(r"android.+((sch-i[89]0\d|shw-m380s|gt-p\d{4}|gt-n\d+|sgh-t8[56]9|nexus 10))", flags=re.I),
        re.compile(r"android.+(transfo[prime\s]{4,10}\s\w+|eeepc|slider\s\w+|nexus 7|padfone|p00c)", flags=re.I),
        re.compile(r"(kf[A-z]+).+silk\/", flags=re.I),
        re.compile(r"android.+(KS(.+))\s+build", flags=re.I),
        re.compile(r"(nexus\s9)", flags=re.I),
        re.compile(r"((SM-T\w+))", flags=re.I),
        re.compile(r"android.+([vl]k\-?\d{3})\s+build", flags=re.I),
        re.compile(r"android\s3\.[\s\w;-]{10}(lg?)-([06cv9]{3,4})", flags=re.I),
        re.compile(r"(lenovo)\s?(s(?:5000|6000)(?:[\w-]+)|tab(?:[\s\w]+))", flags=re.I),
        re.compile(r"android.+(ideatab[a-z0-9\-\s]+)", flags=re.I),
    ]
    tablet_matches = any(regex.search(ua) for regex in tablet_regexes)
    if tablet_matches:
        data = dataset.get('AndroidTablet')
        regex = re.compile(r"Android[- ](\d+(?:\.\d+(?:\.\d+)?)?)")
        m = regex.search(ua)
        if m:
            os_version = m.group(1)
    elif 'Android' in ua:
        data = dataset.get('Android')
        regex = re.compile(r"Android[- ](\d+(?:\.\d+(?:\.\d+)?)?)")
        m = regex.search(ua)
        if m:
            os_version = m.group(1)
    else:
        data = dataset.get('Linux')
    util.update_category(result, data[dataset.KEY_CATEGORY])
    util.update_os(result, data[dataset.KEY_NAME])
    if os_version:
        util.update_os_version(result, os_version)
    return True


def challenge_smartphone(ua, result):
    data = None
    os_version = None
    if 'iPad' in ua:
        data = dataset.get('iPad')
    elif 'iPod' in ua:
        data = dataset.get('iPod')
    elif 'iPhone' in ua:
        data = dataset.get('iPhone')
    elif 'Android' in ua:
        data = dataset.get('Android')
    elif 'CFNetwork' in ua:
        data = dataset.get('iOS')
    elif 'BB10' in ua:
        data = dataset.get('BlackBerry10')
        regex = re.compile(r"BB10(?:.+)Version\/([.0-9]+)")
        m = regex.search(ua)
        if m:
            os_version = m.group(1)
    elif 'BlackBerry' in ua:
        data = dataset.get('BlackBerry')
        regex = re.compile(r"BlackBerry(?:\d+)\/([.0-9]+) ")
        m = regex.search(ua)
        if m:
            os_version = m.group(1)

    if result.get(dataset.KEY_NAME) ==\
            dataset.get('Firefox')[dataset.KEY_NAME]:

        # Firefox OS specific pattern
        # http://lawrencemandel.com/2012/07/27/decision-made-firefox-os-user-agent-string/
        # https://github.com/woothee/woothee/issues/2
        regex = re.compile(
            r"^Mozilla\/[.0-9]+ \((?:Mobile|Tablet);(?:.*;)?"
            r" rv:([.0-9]+)\) Gecko\/[.0-9]+ Firefox\/[.0-9]+$"
        )
        m = regex.search(ua)
        if m:
            data = dataset.get('FirefoxOS')
            os_version = m.group(1)

    if not data:
        return False

    util.update_category(result, data[dataset.KEY_CATEGORY])
    util.update_os(result, data[dataset.KEY_NAME])
    if os_version:
        util.update_os_version(result, os_version)
    return True


def challenge_mobilephone(ua, result):
    if 'KDDI-' in ua:
        obj = re.search('KDDI-([^- /;()"\']+)', ua)
        if obj:
            term = obj.group(1)
            data = dataset.get('au')
            util.update_category(result, data[dataset.KEY_CATEGORY])
            util.update_os(result, data[dataset.KEY_OS])
            util.update_version(result, term)
            return True
    if 'WILLCOM' in ua or 'DDIPOCKET' in ua:
        obj = re.search('(?:WILLCOM|DDIPOCKET);[^/]+/([^ /;()]+)', ua)
        if obj:
            term = obj.group(1)
            data = dataset.get('willcom')
            util.update_category(result, data[dataset.KEY_CATEGORY])
            util.update_os(result, data[dataset.KEY_OS])
            util.update_version(result, term)
            return True
    if 'SymbianOS' in ua:
        data = dataset.get('SymbianOS')
        util.update_category(result, data[dataset.KEY_CATEGORY])
        util.update_os(result, data[dataset.KEY_OS])
        return True
    if 'Google Wireless Transcoder' in ua:
        util.update_map(result, dataset.get('MobileTranscoder'))
        util.update_version(result, 'Google')
        return True
    if 'Naver Transcoder' in ua:
        util.update_map(result, dataset.get('MobileTranscoder'))
        util.update_version(result, 'Naver')
        return True
    return False


def challenge_appliance(ua, result):
    if 'Nintendo DSi;' in ua:
        data = dataset.get('NintendoDSi')
        util.update_category(result, data[dataset.KEY_CATEGORY])
        util.update_os(result, data[dataset.KEY_OS])
        return True
    if 'Nintendo Wii;' in ua:
        data = dataset.get('NintendoWii')
        util.update_category(result, data[dataset.KEY_CATEGORY])
        util.update_os(result, data[dataset.KEY_OS])
        return True
    return False


def challenge_misc(ua, result):
    data = None
    os_version = None
    if '(Win98;' in ua:
        data = dataset.get('Win98')
        os_version = '98'
    elif 'Macintosh; U; PPC;' in ua:
        data = dataset.get('MacOS')
        regex = re.compile(r"rv:(\d+\.\d+\.\d+)")
        m = regex.search(ua)
        if m:
            os_version = m.group(1)
    elif 'Mac_PowerPC' in ua:
        data = dataset.get('MacOS')
    elif 'X11; FreeBSD ' in ua:
        data = dataset.get('BSD')
        regex = re.compile(r"FreeBSD ([^;\)]+);")
        m = regex.search(ua)
        if m:
            os_version = m.group(1)
    elif 'X11; CrOS ' in ua:
        data = dataset.get('ChromeOS')
        regex = re.compile(r"CrOS ([^\)]+)\)")
        m = regex.search(ua)
        if m:
            os_version = m.group(1)
    else:
        return False
    util.update_category(result, data[dataset.KEY_CATEGORY])
    util.update_os(result, data[dataset.KEY_NAME])
    if os_version:
        util.update_os_version(result, os_version)
    return True
