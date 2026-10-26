from station import Station


station_tcr = Station(
    station_id="940GZZLUTCR",
    station_name="Tottenham Court Road Underground Station",
    interchange_lines=[
        {"id": "central"},
        {"id": "northern"},
        {"id": "137"}
    ],
    zones="1",
    lat=51.516426,
    lon=-0.13041
)

station_oc = Station(
    station_id="940GZZLUOXC",
    station_name="Oxford Circus Underground Station",
    interchange_lines=[
        {"id": "victoria"},
        {"id": "central"},
        {"id": "bakerloo"}
    ],
    zones="1",
    lat=51.515224,
    lon=-0.141903
)

print(station_tcr.is_interchange())
