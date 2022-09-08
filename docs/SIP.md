# SIP Examples

## INVITE with Authentication

```
SIP/2.0 407 Proxy Authentication Required
Via: SIP/2.0/TLS 10.13.20.1:37792;rport=37792;branch=z9hG4bKPjb7666eb1-1fbc-42ee-af22-9d452908283b;alias;received=10.13.20.1
From: sip:u.habots.haalice@v6ha.dev.ontalk.com;tag=8ce520bf-8067-497d-bb1d-7ec5a4c5edea
To: sip:conf-65970373-745e-43c9-8432-266bde62c7d0@v6ha.dev.ontalk.com;tag=9dd61ff61e802d8e2bef5f14621ef3c2.31566a34
Call-ID: d168612f-2937-4371-b2f4-df84e756a7f2
CSeq: 3198 INVITE
Proxy-Authenticate: Digest realm="v6ha.dev.ontalk.com", nonce="XrYLu162Co+Wsu1Clhg65wrLUl170PRI"
Server: OnTalk SIP Server
Content-Length: 0

ACK sip:conf-65970373-745e-43c9-8432-266bde62c7d0@v6ha.dev.ontalk.com SIP/2.0
Via: SIP/2.0/TLS 10.13.20.1:37792;rport;branch=z9hG4bKPjb7666eb1-1fbc-42ee-af22-9d452908283b;alias
Max-Forwards: 70
From: sip:u.habots.haalice@v6ha.dev.ontalk.com;tag=8ce520bf-8067-497d-bb1d-7ec5a4c5edea
To: sip:conf-65970373-745e-43c9-8432-266bde62c7d0@v6ha.dev.ontalk.com;tag=9dd61ff61e802d8e2bef5f14621ef3c2.31566a34
Call-ID: d168612f-2937-4371-b2f4-df84e756a7f2
CSeq: 3198 ACK
Route: <sip:v6ha.dev.ontalk.com;transport=tls;lr>
Content-Length:  0

INVITE sip:conf-65970373-745e-43c9-8432-266bde62c7d0@v6ha.dev.ontalk.com SIP/2.0
Via: SIP/2.0/TLS 10.13.20.1:37792;rport;branch=z9hG4bKPjd4098925-0f2c-4da6-95f6-a68760d28cae;alias
Max-Forwards: 70
From: sip:u.habots.haalice@v6ha.dev.ontalk.com;tag=8ce520bf-8067-497d-bb1d-7ec5a4c5edea
To: sip:conf-65970373-745e-43c9-8432-266bde62c7d0@v6ha.dev.ontalk.com
Contact: <sip:u.habots.haalice@10.13.20.1:37792;transport=TLS;ob>
Call-ID: d168612f-2937-4371-b2f4-df84e756a7f2
CSeq: 3199 INVITE
Route: <sip:v6ha.dev.ontalk.com;transport=tls;lr>
Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS
Supported: replaces, 100rel, timer, norefersub
Session-Expires: 1800
Min-SE: 90
User-Agent: PJSUA v2.10 Linux-5.6.3.44/x86_64/glibc-2.31
Proxy-Authorization: Digest username="u.habots.haalice@v6ha.dev.ontalk.com", realm="v6ha.dev.ontalk.com", ...
Content-Type: application/sdp
Content-Length:   779
```


## WebRTC calling PJSIP

INVITE to PJSIP, uses DTLS-SRTP:
```
INVITE sip:david@192.168.12.42:5070 SIP/2.0
Via: SIP/2.0/UDP 10.13.224.154:5060;rport;branch=z9hG4bK5b06182f7eff01723f1cb9e6eaa15af1
Max-Forwards: 70
From: sip:aftershock@webrtc1.dev.tbs;tag=804bdc7b901c307207345cfda91c9d79
To: sip:david@webrtc1.dev.tbs
Call-ID: 9e4e506cc8ae87e67c4971a96a346981@10.13.224.154
CSeq: 200 INVITE
Contact: Anonymous <sip:aftershock@10.13.224.154:5060>
Expires: 300
User-Agent: Sippy B2BUA (Simple)
cisco-GUID: 600158575-2319724014-4068027205-2215805970
h323-conf-id: 600158575-2319724014-4068027205-2215805970
Content-Type: application/sdp
Content-Length: 1569

v=0
o=mozilla...THIS_IS_SDPARTA-68.0 4589701916981175572 0 IN IP4 0.0.0.0
s=-
t=0 0
a=msid-semantic:WMS *
m=audio 23330 UDP/TLS/RTP/SAVPF 109 9 0 8 101
c=IN IP4 10.13.224.154
a=msid:{ed938127-3bdf-43cd-8e4e-e14d0201e7ce} {a77d45c5-abcb-4271-8cc8-a06cad10d7d1}
a=ssrc:2944310524 cname:{0a196581-29a8-4403-acca-4db7ca3dc30c}
a=mid:0
a=rtpmap:109 opus/48000/2
a=rtpmap:9 G722/8000/1
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:109 maxplaybackrate=48000;stereo=1;useinbandfec=1
a=fmtp:101 0-15
a=sendrecv
a=rtcp:23331
a=rtcp-mux
a=crypto:1 AES_CM_128_HMAC_SHA1_80 inline:2prebNpxb4Np0KyRxJKgAD9IK3rlWKR/MQTtMMH+
a=crypto:2 AES_CM_128_HMAC_SHA1_32 inline:cnr4b1YA2mH/Dzthe7G0qOVIcloWL6hgkT+XjHk9
a=crypto:3 AES_192_CM_HMAC_SHA1_80 inline:lsmDvL8exnj6wwE+L6DkB+lZGXskQE//Qj8VW+/M/H9MgT3Fs8c
a=crypto:4 AES_192_CM_HMAC_SHA1_32 inline:znZRXn6uW9MRSl9EyAxwG40M2/R0Gb6kAoGiN7b1l0G1RMi50EQ
a=crypto:5 AES_256_CM_HMAC_SHA1_80 inline:pVCl8bnkr1d1yXkzHUkDJh76XFtXNadfaT+EsSB1fsSaMdjx6GblIn0/o6/F3g
a=crypto:6 AES_256_CM_HMAC_SHA1_32 inline:gQ2LhUf53KR+VYjcTY+vP/aNKnW0um+PELgm78m/lTgqCBPzQTXWh9QIaCBspQ
a=crypto:7 F8_128_HMAC_SHA1_80 inline:Xs884rBi4SWibNPghdgkOxAcRRNLe8wSyvuhG4B2
a=crypto:8 F8_128_HMAC_SHA1_32 inline:CQkpwFVaKcWJzTV5hVcirVwZd9KeedPVuqsaAkQ9
a=crypto:9 NULL_HMAC_SHA1_80 inline:zKn5EFowZ68vBixvMFStRa1By0J9anqSVU7Yoiqb
a=crypto:10 NULL_HMAC_SHA1_32 inline:iJh5Uxtno41ETwCWy5pDc/LdR6Y2SQ9wlIYwF8Pk
a=setup:actpass
a=fingerprint:sha-1 B8:6C:DE:15:7C:53:49:31:5C:0B:C0:6A:1B:66:F6:C8:35:FE:27:8D
```

ANSWER from PJSIP:
```
SIP/2.0 200 OK
Via: SIP/2.0/UDP 10.13.224.154:5060;rport=5060;received=10.13.224.154;branch=z9hG4bK5b06182f7eff01723f1cb9e6eaa15af1
Call-ID: 9e4e506cc8ae87e67c4971a96a346981@10.13.224.154
From: <sip:aftershock@webrtc1.dev.tbs>;tag=804bdc7b901c307207345cfda91c9d79
To: <sip:david@webrtc1.dev.tbs>;tag=8f9360df-76b1-44b3-a0b3-5f28b52b1987
CSeq: 200 INVITE
Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS
Contact: <sip:david@192.168.12.42:5070;ob>
Supported: replaces, 100rel, timer, norefersub
Content-Type: application/sdp
Content-Length:   476

v=0
o=- 3773731800 3773731801 IN IP4 192.168.12.42
s=pjmedia
b=AS:117
t=0 0
a=X-nat:0
m=audio 4012 UDP/TLS/RTP/SAVPF 109 101
c=IN IP4 192.168.12.42
b=TIAS:96000
a=sendrecv
a=ssrc:799656443 cname:749ca13326e0d748
a=rtcp-mux
a=setup:active
a=fingerprint:SHA-256 B5:0B:13:96:97:64:A1:C9:FF:7A:D8:EF:FF:53:10:21:04:95:CB:4A:34:B8:04:C2:4E:BA:18:D8:A4:1D:66:24
a=rtpmap:109 opus/48000/2
a=fmtp:109 useinbandfec=1
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
```



## WebRTC calling FreeSWITCH

INVITE to FreeSWITCH, uses DTLS-SRTP:

```
INVITE sip:3500@10.88.0.20:5080 SIP/2.0
Via: SIP/2.0/UDP 10.88.0.1:5060;rport;branch=z9hG4bKf67332308b8bfec4ce6fb9064695654c
Max-Forwards: 70
From: sip:aftershock@webrtc1.dev.tbs;tag=39c28bbdd2054c0820f60d834398beac
To: sip:3500@webrtc1.dev.tbs
Call-ID: c1f0cfe2da0412520e1eea3dd2a5010e@10.13.224.154
CSeq: 200 INVITE
Contact: Anonymous <sip:aftershock@10.88.0.1:5060>
Expires: 300
User-Agent: Sippy B2BUA (Simple)
cisco-GUID: 600158575-2319724014-4068027205-2215805970
h323-conf-id: 600158575-2319724014-4068027205-2215805970
Content-Type: application/sdp
Content-Length: 1569

v=0
o=mozilla...THIS_IS_SDPARTA-68.0 2393971413639877335 0 IN IP4 0.0.0.0
s=-
t=0 0
a=msid-semantic:WMS *
m=audio 23266 UDP/TLS/RTP/SAVPF 109 9 0 8 101
c=IN IP4 10.13.224.154
a=msid:{57d4cf19-0b61-4e63-a6a9-5f04d39c2759} {21ebe68d-5c58-4026-ba14-21ab01d5e29b}
a=ssrc:2570216174 cname:{b84520ee-2443-4f01-a9b1-dcfea71e9c42}
a=mid:0
a=rtpmap:109 opus/48000/2
a=rtpmap:9 G722/8000/1
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:109 maxplaybackrate=48000;stereo=1;useinbandfec=1
a=fmtp:101 0-15
a=sendrecv
a=rtcp:23267
a=rtcp-mux
a=crypto:1 AES_CM_128_HMAC_SHA1_80 inline:TYrxAu8gz+4T/DcvNiEDAuAizrUKR8oezA8U4xHQ
a=crypto:2 AES_CM_128_HMAC_SHA1_32 inline:HxsPZeXoGpXslWHHtnxyWO/QA4jEefTMR8qLwDzH
a=crypto:3 AES_192_CM_HMAC_SHA1_80 inline:HV15Z1UqLjCSL/jmtVW7d7GXqMyX5aLku3i30jQ6PpIRNgCDvJA
a=crypto:4 AES_192_CM_HMAC_SHA1_32 inline:3ORKOeygVG1aAUFbRMQpasVrCBkEilQJ2m/Ir/okJ8PZn82dHsw
a=crypto:5 AES_256_CM_HMAC_SHA1_80 inline:wfs4EzHEnOFOqR7UIqbpNdn8QlJsA9eRhjERSxoSlOURaw/cHqmX3oRUN7UMCw
a=crypto:6 AES_256_CM_HMAC_SHA1_32 inline:loBH3jJ+LUQSLLOrDVbfTDfJ390xnmn+4X5Uzpdz1ialcAMsNH5YopUMdWNBTA
a=crypto:7 F8_128_HMAC_SHA1_80 inline:CCoZEiKWPjOEMM5/ZXbRUq0vOorffyPJ3xA7vKqG
a=crypto:8 F8_128_HMAC_SHA1_32 inline:8wQ5x+NcgIpU58Ex8dg8kNkBAiprb6bm2JDIUDg6
a=crypto:9 NULL_HMAC_SHA1_80 inline:mIiS0DNXwok4Hu7rlsZSf4+5knYegiarcDUw4OMi
a=crypto:10 NULL_HMAC_SHA1_32 inline:Ynz5IA9yKTfE5FG+WkD6X6N03UAJkmtlFcr4Cmln
a=setup:actpass
a=fingerprint:sha-1 B8:6C:DE:15:7C:53:49:31:5C:0B:C0:6A:1B:66:F6:C8:35:FE:27:8D
```

ANSWER from FreeSWITCH:
```

SIP/2.0 200 OK
Via: SIP/2.0/UDP 10.88.0.1:5060;rport=5060;branch=z9hG4bKf67332308b8bfec4ce6fb9064695654c
From: <sip:aftershock@webrtc1.dev.tbs>;tag=39c28bbdd2054c0820f60d834398beac
To: <sip:3500@webrtc1.dev.tbs>;tag=H51jm3429egtp
Call-ID: c1f0cfe2da0412520e1eea3dd2a5010e@10.13.224.154
CSeq: 200 INVITE
Contact: <sip:3500@10.88.0.20:5080;transport=udp>
User-Agent: FreeSWITCH-mod_sofia/1.8.7-8-6047ebddfc~64bit
Accept: application/sdp
Allow: INVITE, ACK, BYE, CANCEL, OPTIONS, MESSAGE, INFO, UPDATE, REGISTER, REFER, NOTIFY
Supported: timer, path, replaces
Allow-Events: talk, hold, conference, refer
Content-Type: application/sdp
Content-Disposition: session
Content-Length: 834
Remote-Party-ID: "3500" <sip:3500@webrtc1.dev.tbs>;party=calling;privacy=off;screen=no

v=0
o=FreeSWITCH 1564722855 1564722857 IN IP4 10.88.0.20
s=FreeSWITCH
c=IN IP4 10.88.0.20
t=0 0
a=msid-semantic: WMS sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuj
m=audio 19232 UDP/TLS/RTP/SAVPF 109 101
a=rtpmap:109 opus/48000/2
a=fmtp:109 useinbandfec=1; stereo=1
a=rtpmap:101 telephone-event/8000
a=ptime:20
a=fingerprint:sha-1 7D:4E:B9:D1:FC:B8:2C:81:54:93:C0:4B:89:01:D3:A1:F9:83:2F:75
a=setup:active
a=rtcp-mux
a=rtcp:19232 IN IP4 10.88.0.20
a=ice-ufrag:BfeR9t4Mjh2a1nj7
a=ice-pwd:AUXWhYjWPlk47BDyGIgG1aia
a=candidate:4055827917 1 udp 659136 10.88.0.20 19232 typ host generation 0
a=end-of-candidates
a=ssrc:1766175551 cname:fnK0vwawP1bxoWrJ
a=ssrc:1766175551 msid:sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuj a0
a=ssrc:1766175551 mslabel:sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuj
a=ssrc:1766175551 label:sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuja0
```

SDP rewritten by rtpengine:
```
v=0
o=FreeSWITCH 1564722855 1564722857 IN IP4 10.88.0.20
s=FreeSWITCH
c=IN IP4 10.13.224.154
t=0 0
a=msid-semantic: WMS sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuj
m=audio 23300 UDP/TLS/RTP/SAVPF 109 101
a=ssrc:1766175551 cname:fnK0vwawP1bxoWrJ
a=ssrc:1766175551 msid:sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuj a0
a=ssrc:1766175551 mslabel:sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuj
a=ssrc:1766175551 label:sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuja0
a=mid:0
a=rtpmap:109 opus/48000/2
a=rtpmap:101 telephone-event/8000
a=fmtp:109 useinbandfec=1; stereo=1
a=sendrecv
a=rtcp:23300
a=rtcp-mux
a=setup:passive
a=fingerprint:sha-1 B8:6C:DE:15:7C:53:49:31:5C:0B:C0:6A:1B:66:F6:C8:35:FE:27:8D
a=ptime:20
a=ice-ufrag:u3CcfVEK
a=ice-pwd:E3V5zSMgvLS8E61o6sqAgUGFUK
a=candidate:eYSm6dpGDwCVA5qV 1 UDP 2130706431 10.13.224.154 23300 typ host
a=candidate:J4DS0wcsZ3T37rmu 1 UDP 2130706175 10.13.224.154 23316 typ host
a=end-of-candidates
```
