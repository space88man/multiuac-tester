sdp_offer_j2 = """v=0
o=- {{ session_id }} {{ session_ver }} IN {{ address_family|default('IP4') }} {{ contact_ip }}
s=pjmedia
b=AS:117
t=0 0
a=X-nat:0
m=audio {{ rtp_port }} RTP/AVP 96 120
c=IN IP4 {{ contact_ip }}
b=TIAS:96000
a=sendrecv
a=rtpmap:96 speex/16000
a=rtpmap:120 telephone-event/16000
a=fmtp:120 0-16
a=ssrc:520200114 cname:5eb143d3487978cd
a=rtcp:{{ rtcp_port }} IN IP4 {{ contact_ip }}
a=rtcp-mux
m=video 0 RTP/AVP 31
c=IN IP4 127.0.0.1
"""

sdp_answer_j2 = """v=0
o=- {{ session_id }} {{ session_ver }} IN {{ address_family|default('IP4') }} {{ contact_ip }}
s=pjmedia
b=AS:117
t=0 0
a=X-nat:0
m=audio {{ rtp_port }} RTP/AVP 96 120
c=IN IP4 {{ contact_ip }}
b=TIAS:96000
a=ssrc:181184834 cname:67ae2b3c37ece720
a=rtpmap:96 speex/16000
a=rtpmap:120 telephone-event/16000
a=fmtp:120 0-16
a=sendrecv
a=rtcp:{{ rtcp_port }}
a=rtcp-mux
m=video 0 RTP/AVP 31
c=IN IP4 127.0.0.1
"""
