import socket, struct, time

def probe(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2.5)
        pkt = b"\x1b" + 47 * b"\0"
        t0 = time.time()
        s.sendto(pkt, (host, 123))
        data, _ = s.recvfrom(1024)
        rtt = (time.time() - t0) * 1000
        secs = struct.unpack("!I", data[40:44])[0] - 2208988800
        t = time.strftime("%H:%M:%S", time.gmtime(secs))
        print("  %-22s OK   rtt=%4.0fms   serverUTC=%s" % (host, rtt, t))
    except Exception as e:
        print("  %-22s FAIL (%s)" % (host, type(e).__name__))

for h in ["ntp.aliyun.com", "ntp.tencent.com", "time.windows.com", "cn.pool.ntp.org"]:
    probe(h)

print("  localUTC=" + time.strftime("%H:%M:%S", time.gmtime()))
