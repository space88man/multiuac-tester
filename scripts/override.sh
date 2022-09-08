#!/bin/bash
SIP_CONTACT="sip:mead1200@192.168.122.15;ob;transport=tls" \
    SIP_REG_PARAM=";+sip.instance=\"<urn:uuid:00000000-0000-0000-0000-000012341234>\"" \
    SIP_REG_PARAM+=";reg-id=7" SIP_VIA_S="SIP/2.0/TLS 192.168.122.15:5061;rport"  \
    python scripts/t_phone.py --novia-hook
