from influxdb import line_protocol

def make_influx_line(measurement, tag_set, field_set, timestamp):
    """Make inputs as an influx line

    https://docs.influxdata.com/influxdb/v1.7/write_protocols/line_protocol_tutorial/

    For exmaple:
    weather,location=us-midwest temperature=82 1465839830100400200
       |    -------------------- --------------  |
       |             |             |             |
       |             |             |             |
    +-----------+--------+-+---------+-+---------+
    |measurement|,tag_set| |field_set| |timestamp|
    +-----------+--------+-+---------+-+---------+

    """
    data = {
        "tags": tag_set,
        "points": [
            {
                "measurement": measurement,
                "fields": field_set,
                "time": timestamp
            }
        ]
    }
    return line_protocol.make_lines(data)
