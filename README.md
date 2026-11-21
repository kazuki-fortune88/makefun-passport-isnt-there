[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/kazuki-fortune88/makefun-passport-isnt-there/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/kazuki-fortune88/makefun-passport-isnt-there/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

# The Passport That Isn't There — Republic of Talmara

A program that draws a single 1024×1024 image: an open passport spread
from a country that does not exist — the **Republic of Talmara**, a small
island republic of the Meridian Sea (capital **Port Anselm**, currency the
thaler, languages Talmaric and English).

Left page: data page of holder **Elena Maris Ansel** (born 14 Mar 1994,
Port Anselm), issued 12 May 2023 in Port Anselm, expiring 11 May 2033,
with a PIL-drawn stylised portrait and a valid ICAO MRZ strip that matches
the data. Right page: visa stamps in chronological order, all dated after
the issue date — entry/exit Meridia (Jun 2023), entry Sorvane (11 Oct 2024),
return entry Talmara (25 Oct 2024) — plus the telling detail: a
**"Visa on arrival — 30 days, fee 25 thalers"** stamp.

## Run

```bash
python3 main.py
# writes entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

Deterministic: stdlib + PIL only, no network, no randomness — rebuilding
produces a byte-identical PNG.

Made with [make.fun](https://make.fun) — referral code `4fxhr3y1`.
