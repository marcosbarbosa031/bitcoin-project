import sys
import urllib2

if (len(sys.argv) <= 2):
    if (len(sys.argv[1]) == 34 or len(sys.argv[1]) == 33):
        address = sys.argv[1]
        req = urllib2.Request("https://blockchain.info/pt/q/addressbalance/" + address)
        try:
            response = urllib2.urlopen(req)
            ballance = float(response.read())/100000000
            print str(ballance) + " BTC"
        except urllib2.URLError as e:
            print "Error: " + e.reason
            print "Reason: Invalid Bitcoin Address!"
    else:
        print "Invalid Bitcoin Address!"
else:
    print "Too many arguments. Just pass a valid Bitcoin Address."
