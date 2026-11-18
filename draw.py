#!/usr/bin/env python3
"""Draw the news-image-20261118 front page: 'The World in One Day — Wednesday
18 November 2026'. 1024x1024 PNG, drawn entirely in code (Pillow + DejaVu).

Layout: masthead + lead panel (APEC Shenzhen) + 3-column body with 36 stories
in 5 regional sections + footer. Every headline/deck traces to the verified
facts file; no invented numbers or quotes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
GUTTER = 16
COLW = (W - 2 * MARGIN - 2 * GUTTER) // 3  # 313

PAPER = (253, 248, 238)
INK = (17, 17, 17)
RED = (192, 57, 43)
NAVY = (26, 47, 90)
GREY = (110, 108, 100)
LEAD_BG = (255, 243, 224)
RULE = (198, 188, 168)
SKY = (214, 228, 244)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_TITLE = font(True, 58)
F_DATE = font(True, 22)
F_STAND = font(False, 14)
F_KICKER = font(True, 13)
F_LEAD = font(True, 38)
F_SUB = font(True, 19)
F_LEADDECK = font(False, 15)
F_BAR = font(True, 14)
F_HEAD = font(True, 15)
F_DECK = font(False, 12)
F_FOOT = font(True, 13)

# (section, headline, deck) — section label only on the first story of a run.
COLUMNS = [
    [  # Column 1: Asia-Pacific (10) + World & Science (2)
        ("ASIA-PACIFIC", "TRUMP IN MANILA FOR QUAD",
         "The US president praises \u2018friend\u2019 Albanese as Quad leaders announce a new plan."),
        (None, "MODI PUSHES E-VISAS AT ASEAN",
         "India\u2019s PM proposes free e-visas and maritime cooperation in Manila."),
        (None, "CYCLONE AKVAN NEARS INDIA",
         "The storm heads for Andhra Pradesh, with landfall due Friday and gusts to 145 kmph."),
        (None, "DHONI RETIRES FROM THE IPL",
         "The former India captain will become Chennai Super Kings mentor."),
        (None, "JAPAN PITCHES AN ASIAN IEA",
         "Tokyo offers ASEAN nations access to idle oil storage and energy storage for a fee."),
        (None, "CANADA, CHINA EXTEND DEALS",
         "Xi meets PM Carney ahead of APEC as the two countries extend trade deals."),
        (None, "US PRESSES ICAO OVER TAIWAN",
         "Washington protests after Lai\u2019s presidential plane overflight permit is revoked."),
        (None, "AMAZON PLEDGES $7BN FOR INDIA",
         "The $7 billion will go to India\u2019s renewable energy sector, Amazon announces."),
        (None, "INDIA GDP \u2018TO GROW 7.5%\u2019",
         "Growth is expected at 7.5% in the July\u2013September quarter, forecasts show."),
        (None, "AUSTRALIA SANCTIONS SETTLERS",
         "FM Penny Wong targets \u2018illegal\u2019 West Bank settlement expansion."),
        ("WORLD & SCIENCE", "VOYAGER 1 NEARS ONE LIGHT-DAY",
         "The first human object to get there sails on in interstellar space."),
        (None, "SPACEX CATCHES A STARSHIP",
         "SpaceX just caught a falling Starship \u2014 and now asks, \u2018Now what?\u2019"),
    ],
    [  # Column 2: Europe (6) + Middle East & Africa (6)
        ("EUROPE", "UKRAINE HITS CRIMEA BRIDGE",
         "Kyiv strikes a second straight day as Russia pounds Kyiv bridges in return."),
        (None, "BRITAIN SANCTIONS 8 FIRMS",
         "London acts over illegal West Bank settlements, including Tzav 9."),
        (None, "CYBER-ATTACK HITS FREEZERS",
         "Supermarket freezers fail across seven European countries after an attack."),
        (None, "DEUTSCHE BANK IGNORED FLAGS",
         "A leaked-files probe cites Russian oligarchs among risky clients flagged."),
        (None, "STRIKES GRIP SPAIN, FRANCE",
         "Spaniards strike as police clash with protesters; French unions join in."),
        (None, "UEFA BACKS DIALLO FOR FIFA",
         "Europe\u2019s body backs France\u2019s Diallo to stand against Infantino."),
        ("MIDDLE EAST & AFRICA", "IRAN HITS US RADAR IN BAHRAIN",
         "Drones strike a US military radar as Iran and the US trade blows."),
        (None, "GAZA TRUCE \u2018FACES COLLAPSE\u2019",
         "The Board of Peace warns the ceasefire could collapse without action."),
        (None, "GAZA BACK TO KEROSENE STOVES",
         "Families return to kerosene stoves amid a cooking-gas shortage."),
        (None, "KAHANA ELECTED ISRAEL SPEAKER",
         "Parliament elects Matan Kahana, a Gadi Eisenkot ally, as speaker."),
        (None, "TOP IRGC MAN IN IRAQ FOR TALKS",
         "A top commander visits amid Kataib Hezbollah tensions."),
        (None, "CONGO PEACE EFFORTS FAIL",
         "Rival peace efforts fail to halt violence in the east, reports say."),
    ],
    [  # Column 3: Mideast & Africa cont. (2) + Americas (8) + World cont. (2)
        ("MIDEAST & AFRICA (cont.)", "SUDAN FACTORIES STRUGGLE BACK",
         "Factories struggle to recover after wartime destruction."),
        (None, "BABOON MOVE SPARKS PROTESTS",
         "A 44-member troop is relocated as demonstrators block the vehicle."),
        ("AMERICAS", "DOW PLUNGES 1,000+ POINTS",
         "The Dow closes down 848.75 at 50,575.52 as tech sells off."),
        (None, "NVIDIA DOUBLES REVENUE",
         "Revenue hits $115.84bn; the board will not reinstate Jensen Huang."),
        (None, "NVIDIA PROBES SPY CLAIM",
         "Nvidia hires a law firm to probe an alleged CEO link to an alleged Chinese spy."),
        (None, "FUNDS FLEE TECH FOR GOLD",
         "Institutions cut tech sharply and shift to gold and international stocks."),
        (None, "FED: MORE HIKES MAY BE NEEDED",
         "A Fed official warns more rate hikes may be needed before spring 2027."),
        (None, "TRUMP BBC DEADLINE EXTENDED",
         "A judge extends the Trump deposition deadline in the $10bn BBC suit to 22 Jan."),
        (None, "NSA SECRET NETWORK GOES DOWN",
         "The NSA\u2019s classified internal communications network goes down, an official says."),
        (None, "FISHERMEN SUE OVER STRIKE",
         "Ecuadorian fishermen sue the Trump administration over a drone strike."),
        ("WORLD & SCIENCE (cont.)", "DEEP-SEA ROCKS TEEM WITH LIFE",
         "Rocks eyed for deep-sea mining are found teeming with life, scientists say."),
        (None, "GTA 6 VICE CITY COURT REVEALED",
         "The Miami Heat reveal a Vice City NBA court for GTA 6."),
    ],
]

LEAD_KICKER = "APEC SUMMIT  \u00b7  SHENZHEN  \u00b7  18\u201319 NOVEMBER"
LEAD_HEAD = "APEC OPENS IN SHENZHEN"
LEAD_SUB = "FIRST-EVER TRUMP\u2013XI\u2013PUTIN MEETING SET FOR THURSDAY"
LEAD_DECK = ("21 members meet as a first-ever Trump\u2013Xi\u2013Putin trilateral "
             "is set for Thursday on the sidelines.")
STANDFIRST = ("APEC opens in Shenzhen  \u00b7  Dow plunges 1,000+ points  \u00b7  "
              "Voyager 1 nears one light-day")
FOOTER = "18 NOVEMBER 2026  \u00b7  37 STORIES  \u00b7  SIX CONTINENTS  \u00b7  EVERY STORY AS REPORTED ON THE DAY"

HEAD_LH, DECK_LH = 18, 14
BAR_H, BAR_GAP = 24, 4
BASE_GAP = 5


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines (each fits max_w)."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    warnings = []

    # ---- Masthead ----
    d.text((W // 2, 14), "THE WORLD TODAY", font=F_TITLE, fill=INK, anchor="ma")
    d.line([(MARGIN, 86), (W - MARGIN, 86)], fill=RED, width=4)
    d.text((W // 2, 94), "WEDNESDAY 18 NOVEMBER 2026", font=F_DATE, fill=RED, anchor="ma")
    d.text((W // 2, 122), STANDFIRST, font=F_STAND, fill=GREY, anchor="ma")

    # ---- Lead panel ----
    px0, px1, py0, py1 = MARGIN, W - MARGIN, 146, 274
    d.rectangle([px0, py0, px1, py1], fill=LEAD_BG, outline=RED, width=2)
    d.text((px0 + 14, py0 + 8), LEAD_KICKER, font=F_KICKER, fill=RED)
    d.text((px0 + 14, py0 + 26), LEAD_HEAD, font=F_LEAD, fill=INK)
    d.text((px0 + 14, py0 + 70), LEAD_SUB, font=F_SUB, fill=RED)
    d.text((px0 + 14, py0 + 92), LEAD_DECK, font=F_LEADDECK, fill=INK)
    # Skyline strip along the panel bottom: navy towers + red sun.
    sky_y = py1 - 20
    d.rectangle([px0 + 2, sky_y, px1 - 2, py1 - 2], fill=SKY)
    d.ellipse([px1 - 78, sky_y - 22, px1 - 38, sky_y + 18], fill=RED)
    towers = [(0, 16), (52, 12), (104, 18), (158, 10), (206, 15), (258, 12),
              (312, 18), (366, 13), (420, 16), (472, 11), (524, 17), (576, 12),
              (630, 15), (682, 10), (734, 16), (786, 13), (838, 17)]
    for dx, th in towers:
        x = px0 + 8 + dx
        d.rectangle([x, py1 - 2 - th, x + 40, py1 - 2], fill=NAVY)
    d.rectangle([px0, py0, px1, py1], outline=RED, width=2)

    # ---- Body: measure stories, then draw columns justified to the footer ----
    body_top, body_bottom = 286, 984
    col_x = [MARGIN + i * (COLW + GUTTER) for i in range(3)]

    def story_height(story):
        _, _, deck = story
        lines = wrap(d, deck, F_DECK, COLW)
        if len(lines) > 2:
            warnings.append(f"deck needs {len(lines)} lines: {deck[:50]}")
        return HEAD_LH + DECK_LH * len(lines)

    # Pre-check: every headline fits on one line.
    for col in COLUMNS:
        for _, head, _ in col:
            if d.textlength(head, font=F_HEAD) > COLW:
                warnings.append(f"headline too wide ({d.textlength(head, font=F_HEAD):.0f}px): {head}")

    for ci, col in enumerate(COLUMNS):
        x = col_x[ci]
        heights = [story_height(s) for s in col]
        nbars = sum(1 for s in col if s[0])
        content = (sum(heights) + BASE_GAP * (len(col) - 1)
                   + nbars * (BAR_H + BAR_GAP))
        slack = (body_bottom - body_top) - content
        if slack < 0:
            warnings.append(f"column {ci + 1} overflows by {-slack}px")
            slack = 0
        gap = BASE_GAP + slack / max(1, len(col) - 1)
        y = body_top
        for (section, head, deck), hh in zip(col, heights):
            if section:
                d.rectangle([x, y, x + COLW, y + BAR_H], fill=NAVY)
                d.text((x + 8, y + 4), section, font=F_BAR, fill=(255, 255, 255))
                y += BAR_H + BAR_GAP
            d.text((x, y), head, font=F_HEAD, fill=INK)
            y += HEAD_LH
            for line in wrap(d, deck, F_DECK, COLW):
                d.text((x, y), line, font=F_DECK, fill=(51, 51, 51))
                y += DECK_LH
            y += gap
        print(f"column {ci + 1}: {len(col)} stories, content {content}px, "
              f"slack {slack:.0f}px, end y {y - gap:.0f}")

    # ---- Footer ----
    d.line([(MARGIN, 992), (W - MARGIN, 992)], fill=RULE, width=2)
    d.text((W // 2, 998), FOOTER, font=F_FOOT, fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    total = 1 + sum(len(c) for c in COLUMNS)
    print(f"saved {out} ({os.path.getsize(out)} bytes), {total} stories total")
    for wmsg in warnings:
        print("WARNING:", wmsg)
    print("WARNINGS:", len(warnings))


if __name__ == "__main__":
    main()
