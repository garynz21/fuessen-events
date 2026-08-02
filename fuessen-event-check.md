You are running the biweekly "Füssen Event Check" for Gary, who lives in Weissensee (Füssen, Ostallgäu, 87629) with his wife and two 7-year-old boys. Your job: research upcoming events, update the event database, and regenerate the subscribed calendar file. Work autonomously, do not ask questions. You are already in the repo root (the folder containing this file).

### Interest profile (what qualifies as a hit)

1. Adventure and expedition talks (Messner-style multivision lectures, mountaineering, exploration), anywhere within about 1 hour of Füssen (Füssen, Oberstdorf, Kempten, Garmisch, Reutte, Kaufbeuren).
2. Classical concerts, especially piano and cello, chamber music: Kaisersaal Kloster St. Mang, Festival vielsaitig, Festspielhaus Neuschwanstein, regional concert halls.
3. Outdoor and open-air concerts and open-air theater (Königswinkel Open Airs, Freilichtbühnen, lake stages, Heimatabende am See).
4. Interesting science talks (Hochschule Kempten public lectures, planetarium/observatory events, DAV lectures, popular science tours).
5. Ice hockey: EV Füssen ONLY special games, not the full home schedule. Special means: season home opener, derbies (SC Riessersee, ESV Kaufbeuren, other Bavarian rivals), pre-playoff and playoff home games, plus any international games or national team fixtures in the region (the Bundesstützpunkt Arena occasionally hosts U-national-team tournaments, always check). A normal Tuesday home game against a mid-table team does NOT qualify. Expect roughly 1-2 EVF entries per month max during the season.
6. Football: NOT FC Augsburg. Only FC Bayern München truly special fixtures (Klassiker, Champions League knockout, finals) and special events at Olympiastadion München. These are rare exceptions, max 1-2 per quarter.
7. English original-version (OV) films at Alpenfilmtheater Füssen (typically Wednesdays, program changes weekly: https://www.alpenfilmtheater.de/programm).
8. Running events and triathlons, local first (Tegelberglauf, Weißenseelauf, Füssener Laufwochenende, Allgäu Triathlon, Hopfensee runs), including kids races (Nachwuchslauf).
9. Kids events for two 7-year-olds: circus performances, children's musicals (Kindermusical, children's music academies), stone discovery / geology adventures, kids white-water or rafting programs, kids sports events (Dorfsportfest, Jugendsportfest).
10. Medieval / Ritter festivals where villages turn medieval (Mittelalterspektakel Eisenberg, Sulzberg Ritterabenteuer, Ritterspiele Türkheim, Kaltenberg, Burgenregion Allgäu-Außerfern events, Castle Days).
11. Füssen town events: Stadtfest, Nacht der Musik (spring), Mittelaltermarkt, Seefest, and everything public in Weissensee and Schwangau (Vereinstermine: Standkonzerte, Feuerwehrfeste, Colomansfest, Herbstmarkt, Weihnachtsmarkt am Kiosk).
12. Live music and special nights in Füssen bars and pubs: the Bayrisch Pub, the wine bar and the cocktail bar in the old town, plus similar venues (live bands, acoustic sessions, jam nights, whisky/wine tastings with music). Check their websites and social media via web search plus the fuessen.de event calendar. Only concrete dated events qualify, not weekly opening hours.

Time horizon: today + 4 months. Language of event descriptions: English with German event names kept as-is. Never use em dashes in any output text.

Description rule for concerts: always name the instruments or genre in the description (e.g. "violin and piano duo recital", "cello", "piano trio", "vocal ensemble", "brass band") so Gary can scan for piano and cello events at a glance. Look up performers' instruments on the event page if the listing does not state them; if you cannot verify the instrument, write "instrument not stated in the listing" rather than guessing.

### Source checklist (search all, fetch where useful)

- https://das-festspielhaus.de/programm/ (Festspielhaus and Königswinkel Open Airs)
- https://www.fuessen.de/en/culture/events/ and the weekly PDF under fuessen.de/service
- https://fuessen-weissensee.de/veranstaltungen/ and the Vereinstermine PDF
- https://festivalvielsaitig.stadt-fuessen.de (chamber music)
- https://evfuessen.de/spielplan/ (confirm exact face-off times)
- https://www.alpenfilmtheater.de/programm (OV films, next 2 weeks only)
- https://www.ac-live.de (Allgäu Concerts open airs)
- https://www.burgenregion.de/erleben/feste-spektakel-ausstellungen (medieval)
- https://www.schwangau.de and TSV Schwangau (Tegelberglauf, Dorfsportfest, Colomansfest)
- runme.de / running.life filtered on Füssen (runs and triathlons)
- eventim.de city page Füssen, meinestadt.de Füssen/Kempten/Marktoberdorf (circus, talks, kids shows)
- Web search for: "Reinhold Messner Vortrag" region, "Mundologia" or multivision lectures Allgäu, "Kindermusical" Füssen/Kempten, "Zirkus" Füssen/Kempten/Marktoberdorf, Hochschule Kempten öffentliche Vorträge, FC Bayern special fixtures, Olympiastadion München events.
- Web search for: "Bayrisch Pub Füssen" events, live music Füssen bar, "Weinbar Füssen" veranstaltung, cocktail bar Füssen live musik.

### Accuracy rules (critical)

- Only add an event if you verified its date on a real web page during this run. Never invent or extrapolate events.
- If a date is confirmed but the time is not published yet, use the placeholder rules below and mark it tentative.
- Record the page you verified it on in the `url` field.

### Update algorithm

1. Read `state/events.json`. Schema per event:
   `{ "uid": "...", "title": "...", "start": ISO8601 with offset, "end": ISO8601, "location": "...", "description": "...", "url": "...", "status": "confirmed|tentative|cancelled", "sequence": 0, "category": "...", "alarm": false, "last_verified": "YYYY-MM-DD" }`
2. Research all categories for the time horizon.
3. For each found event, match against the database by fuzzy title + date:
   - NEW event: add with a stable slug uid (`fuessen-YYYY-short-slug@garylewis`), sequence 0.
   - CHANGED (time firmed up, venue change, price/status change): update fields, increment `sequence` by 1 (this is what makes subscribed calendars pick up the change), set status confirmed if now fixed.
   - CANCELLED: keep the entry, set status cancelled, increment sequence. Do not delete, deletion without an ICS CANCEL confuses subscribers.
   - UNCHANGED: just update `last_verified`.
4. Never remove past events from the JSON (history is useful). The ICS generator script handles which events land in the ICS.
5. Football filter: apply the Ausnahme rule strictly. When in doubt, leave it out.
6. OV films: add only concrete screenings within the next 14 days, uid pattern `fuessen-ov-YYYYMMDD@garylewis`, category `ov-film`.
7. Placeholder times: EV Füssen typically Fri 19:30 / Sun 18:00; Bundesliga windows Sat 15:30 until fixed. Mark such events status tentative and say "time tbc, verify" in the description.
8. Set `"alarm": true` on high-demand ticketed events (the generator adds a reminder 14 days before).

### ICS generation

After updating the JSON, regenerate the calendar by running:

    python3 scripts/generate_ics.py

The script reads `state/events.json` and completely rewrites `fuessen-events.ics` (Europe/Berlin VTIMEZONE, METHOD:PUBLISH, stable UIDs and SEQUENCE from JSON, VALARM for alarm events, proper escaping and 75-octet folding). It only writes events from 7 days ago onward, and OV films only from today onward. It fails loudly on invalid JSON or duplicate UIDs; if it fails, fix the JSON and rerun it. Do not hand-write the ICS.

### Finish the run

1. Write updated `state/events.json`, then run the generator so `fuessen-events.ics` is fresh.
2. `git add -A && git commit -m "event check YYYY-MM-DD: X new, Y updated, Z cancelled" && git push`.
3. Append a short human-readable summary to `run.log`: what is new, what changed, what to book soon (ticket urgency), and anything you could not verify.
