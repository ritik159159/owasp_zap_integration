import os
import sys
import time
from zapv2 import ZAPv2

ZAP_ADDRESS = os.getenv("ZAP_ADDRESS", "http://127.0.0.1:8081")
ZAP_API_KEY = os.environ["ZAP_API_KEY"]
TARGET = os.getenv("TARGET", "https://jsonplaceholder.typicode.com")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
ACTIVE_SCAN = os.getenv("ACTIVE_SCAN", "false").lower() == "true"
FAIL_ON = os.getenv("FAIL_ON", "High")   # High | Medium | Low

# In CI the spec path is the one inside the ZAP container
API_SPEC = os.getenv("ZAP_SPEC_PATH")
if not API_SPEC:
    API_SPEC = os.path.abspath("openapi.json")
    if not os.path.isfile(API_SPEC):
        raise FileNotFoundError(f"OpenAPI file not found: {API_SPEC}")

zap = ZAPv2(apikey=ZAP_API_KEY,
            proxies={"http": ZAP_ADDRESS, "https": ZAP_ADDRESS})
print("ZAP version:", zap.core.version)

if AUTH_TOKEN:
    zap.replacer.add_rule(
        description="auth-header", enabled=True, matchtype="REQ_HEADER",
        matchregex=False, matchstring="Authorization",
        replacement=f"Bearer {AUTH_TOKEN}",
    )

zap.openapi.import_file(API_SPEC, target=TARGET)
print("OpenAPI definition imported.")

while int(zap.pscan.records_to_scan) > 0:
    print("Passive scan records remaining:", zap.pscan.records_to_scan)
    time.sleep(2)

if ACTIVE_SCAN:
    scan_id = zap.ascan.scan(url=TARGET, recurse=True)
    while int(zap.ascan.status(scan_id)) < 100:
        print("Active scan progress:", zap.ascan.status(scan_id), "%")
        time.sleep(10)
    while int(zap.pscan.records_to_scan) > 0:
        time.sleep(2)

alerts = zap.core.alerts(baseurl=TARGET)
print("\nAlerts found:", len(alerts))
for a in alerts:
    print(f"[{a['risk']}] {a['alert']} -> {a['method']} {a['url']}")

with open("zap-report.html", "w", encoding="utf-8") as f:
    f.write(zap.core.htmlreport())
with open("zap-report.json", "w", encoding="utf-8") as f:
    f.write(zap.core.jsonreport())
print("Reports saved: zap-report.html, zap-report.json")

order = ["Informational", "Low", "Medium", "High"]
bad = [a for a in alerts if order.index(a["risk"]) >= order.index(FAIL_ON)]
print(f"Alerts at or above {FAIL_ON}: {len(bad)}")
sys.exit(1 if bad else 0)