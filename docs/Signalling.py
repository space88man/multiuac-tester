# WebRTC to FreeSWITCH


wss_offer = {
    "callId": "5e7367d2-4bb1-46e4-b79c-7859950cf131",
    "name": "aftershock",
    "sdp": {
        "sdp": "v=0\r\no=mozilla...THIS_IS_SDPARTA-68.0 2393971413639877335 0 IN IP4 0.0.0.0\r\ns=-\r\nt=0 0\r\na=sendrecv\r\na=fingerprint:sha-256 CC:36:DF:9C:6B:29:47:32:6B:D9:DE:86:A9:81:28:EF:91:92:14:07:A3:C6:BD:DB:AE:8E:B7:4B:D6:91:35:F8\r\na=group:BUNDLE 0\r\na=ice-options:trickle\r\na=msid-semantic:WMS *\r\nm=audio 52511 UDP/TLS/RTP/SAVPF 109 9 0 8 101\r\nc=IN IP4 192.168.1.217\r\na=candidate:0 1 UDP 2122187007 192.168.1.217 52511 typ host\r\na=candidate:3 1 UDP 2122121471 192.168.124.1 51589 typ host\r\na=candidate:6 1 UDP 2122055935 10.88.0.1 45044 typ host\r\na=candidate:9 1 UDP 2121990399 192.168.81.6 37749 typ host\r\na=candidate:12 1 UDP 2122252543 2406:3003:2005:244:4ac1:faa5:1124:9fe7 50474 typ host\r\na=candidate:15 1 TCP 2105458943 192.168.1.217 9 typ host tcptype active\r\na=candidate:16 1 TCP 2105393407 192.168.124.1 9 typ host tcptype active\r\na=candidate:17 1 TCP 2105327871 10.88.0.1 9 typ host tcptype active\r\na=candidate:18 1 TCP 2105262335 192.168.81.6 9 typ host tcptype active\r\na=candidate:19 1 TCP 2105524479 2406:3003:2005:244:4ac1:faa5:1124:9fe7 9 typ host tcptype active\r\na=candidate:0 2 UDP 2122187006 192.168.1.217 47797 typ host\r\na=candidate:3 2 UDP 2122121470 192.168.124.1 50182 typ host\r\na=candidate:6 2 UDP 2122055934 10.88.0.1 41639 typ host\r\na=candidate:9 2 UDP 2121990398 192.168.81.6 42373 typ host\r\na=candidate:12 2 UDP 2122252542 2406:3003:2005:244:4ac1:faa5:1124:9fe7 58672 typ host\r\na=candidate:15 2 TCP 2105458942 192.168.1.217 9 typ host tcptype active\r\na=candidate:16 2 TCP 2105393406 192.168.124.1 9 typ host tcptype active\r\na=candidate:17 2 TCP 2105327870 10.88.0.1 9 typ host tcptype active\r\na=candidate:18 2 TCP 2105262334 192.168.81.6 9 typ host tcptype active\r\na=candidate:19 2 TCP 2105524478 2406:3003:2005:244:4ac1:faa5:1124:9fe7 9 typ host tcptype active\r\na=sendrecv\r\na=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level\r\na=extmap:2/recvonly urn:ietf:params:rtp-hdrext:csrc-audio-level\r\na=extmap:3 urn:ietf:params:rtp-hdrext:sdes:mid\r\na=fmtp:109 maxplaybackrate=48000;stereo=1;useinbandfec=1\r\na=fmtp:101 0-15\r\na=ice-pwd:f33756ad90c1fd221cd854e713fc8305\r\na=ice-ufrag:7848ec25\r\na=mid:0\r\na=msid:{57d4cf19-0b61-4e63-a6a9-5f04d39c2759} {21ebe68d-5c58-4026-ba14-21ab01d5e29b}\r\na=rtcp:47797 IN IP4 192.168.1.217\r\na=rtcp-mux\r\na=rtpmap:109 opus/48000/2\r\na=rtpmap:9 G722/8000/1\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:101 telephone-event/8000\r\na=setup:actpass\r\na=ssrc:2570216174 cname:{b84520ee-2443-4f01-a9b1-dcfea71e9c42}\r\n",
        "type": "offer"
    },
    "target": "3500",
    "type": "video-offer"
}

sip_answer = {
    "callId": "5e7367d2-4bb1-46e4-b79c-7859950cf131",
    "name": "3500",
    "sdp": {
        "type": "answer",
        "sdp": "v=0\r\no=FreeSWITCH 1564722855 1564722857 IN IP4 10.88.0.20\r\ns=FreeSWITCH\r\nc=IN IP4 10.13.224.154\r\nt=0 0\r\na=msid-semantic: WMS sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuj\r\nm=audio 23300 UDP/TLS/RTP/SAVPF 109 101\r\na=ssrc:1766175551 cname:fnK0vwawP1bxoWrJ\r\na=ssrc:1766175551 msid:sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuj a0\r\na=ssrc:1766175551 mslabel:sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuj\r\na=ssrc:1766175551 label:sv3BUhVjas1PSwU3vOXFq4omMZnq1Tuja0\r\na=mid:0\r\na=rtpmap:109 opus/48000/2\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:109 useinbandfec=1; stereo=1\r\na=sendrecv\r\na=rtcp:23300\r\na=rtcp-mux\r\na=setup:passive\r\na=fingerprint:sha-1 B8:6C:DE:15:7C:53:49:31:5C:0B:C0:6A:1B:66:F6:C8:35:FE:27:8D\r\na=ptime:20\r\na=ice-ufrag:u3CcfVEK\r\na=ice-pwd:E3V5zSMgvLS8E61o6sqAgUGFUK\r\na=candidate:eYSm6dpGDwCVA5qV 1 UDP 2130706431 10.13.224.154 23300 typ host\r\na=candidate:J4DS0wcsZ3T37rmu 1 UDP 2130706175 10.13.224.154 23316 typ host\r\na=end-of-candidates\r\n"
    },
    "target": "aftershock",
    "type": "video-answer"
}
