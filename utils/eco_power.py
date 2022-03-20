import urllib.request, xmltodict, datetime
import logging as logger


def get_power(datacenter, time_stamp):
    v_max = 30
    maxRadiation = 1000
    total = get_wind(datacenter, time_stamp, v_max) + get_solar(datacenter, time_stamp, maxRadiation)
    return total


def get_wind(datacenter, time_stamp, v_max):
    v = float(get_xml(datacenter, ('windSpeed', '@mps'), time_stamp)) * 1.6
    power = datacenter.wind_max * (v / v_max)**2
    #logger.info(f"Wind Power {round(power)}")
    return power


def get_solar(datacenter, time_stamp, maxRadiation):
    actualRadiation = float(get_xml(datacenter, ('globalRadiation', '@value'), time_stamp))
    power = datacenter.solar_max * (actualRadiation / maxRadiation)
    #logger.info(f"Solar Power {round(power)}")
    return power


def get_xml(datacenter, target: tuple[str], time_stamp):
    lat = datacenter.lat
    long = datacenter.long
    url = "http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast?lat=%s;long=%s" % (str(lat), str(long))
    raw = urllib.request.urlopen(url)
    dict = xmltodict.parse(raw.read().decode("utf8"))
    index = time_stamp_to_index(time_stamp, dict)
    try:
        value = dict['weatherdata']['product']['time'][index]['location'][target[0]][target[1]]
    except:
        value = 50
    return (value)


def time_stamp_to_index(time_stamp, dict):
    time = datetime.datetime.fromtimestamp(time_stamp)
    start_time_raw = dict['weatherdata']['product']['time'][0]['@from']
    # cut away unused shit and convert
    start_time = start_time_raw.replace('T', ' ').replace('Z', '')
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    diff_raw = time - start_time
    return int(diff_raw.total_seconds() // 3600) * 2
