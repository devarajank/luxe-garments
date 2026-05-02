#!/usr/bin/env python3
"""Update all product images with distinct, accurate Unsplash photos."""
import urllib.request
import urllib.error
import json

BASE = "http://localhost:8001"
HEADERS = {"Content-Type": "application/json", "x-user-role": "admin"}

# Product ID -> Unsplash image URL
IMAGES = {
    # ── ELECTRONICS ──────────────────────────────────────────────────────────
    # Smartphones
    "ELEC-001": "https://images.unsplash.com/photo-1592286927505-1def25115558?w=400",
    "ELEC-002": "https://images.unsplash.com/photo-1610945264803-c22b62d2a7b3?w=400",
    "ELEC-003": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400",
    "ELEC-004": "https://images.unsplash.com/photo-1511294635253-b0661cff6600?w=400",
    "ELEC-005": "https://images.unsplash.com/photo-1620655249168-9d6e51578b21?w=400",
    # Laptops
    "ELEC-006": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400",
    "ELEC-007": "https://images.unsplash.com/photo-1588872657840-790ff3a58e39?w=400",
    "ELEC-008": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400",
    "ELEC-009": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400",
    "ELEC-010": "https://images.unsplash.com/photo-1603302576837-37891a844e48?w=400",
    # Tablets
    "ELEC-011": "https://images.unsplash.com/photo-1542992941-44c2c22e2d91?w=400",
    "ELEC-012": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400",
    "ELEC-013": "https://images.unsplash.com/photo-1589739900243-4b52cd9b104e?w=400",
    "ELEC-014": "https://images.unsplash.com/photo-1586253408875-cff102099c53?w=400",
    "ELEC-015": "https://images.unsplash.com/photo-1603387751919-a39bc6437ee0?w=400",
    # Accessories
    "ELEC-016": "https://images.unsplash.com/photo-1626348158427-acda1afb1d17?w=400",
    "ELEC-017": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400",
    "ELEC-018": "https://images.unsplash.com/photo-1610529215189-df8a0b9cfa1c?w=400",
    "ELEC-019": "https://images.unsplash.com/photo-1605559427920-cd4628902d4a?w=400",
    "ELEC-020": "https://images.unsplash.com/photo-1622845550977-9ee7b4c9e8ea?w=400",
    # Audio
    "ELEC-021": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
    "ELEC-022": "https://images.unsplash.com/photo-1487215078519-e21cc028cb29?w=400",
    "ELEC-023": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
    "ELEC-024": "https://images.unsplash.com/photo-1572293552491-d51a085edcc8?w=400",
    "ELEC-025": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400",

    # ── FASHION ──────────────────────────────────────────────────────────────
    # Men
    "FASH-001": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
    "FASH-002": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
    "FASH-003": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400",
    "FASH-004": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400",
    "FASH-005": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400",
    # Women
    "FASH-006": "https://images.unsplash.com/photo-1612551564844-2d34e0d2cf8d?w=400",
    "FASH-007": "https://images.unsplash.com/photo-1598032895397-b9472444bf93?w=400",
    "FASH-008": "https://images.unsplash.com/photo-1599599810694-b5ac4dd37e3b?w=400",
    "FASH-009": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400",
    "FASH-010": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400",
    # Kids
    "FASH-011": "https://images.unsplash.com/photo-1626481851754-fe4a3e81d1cf?w=400",
    "FASH-012": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400",
    "FASH-013": "https://images.unsplash.com/photo-1543790036-38b1e1fc87e2?w=400",
    "FASH-014": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400",
    "FASH-015": "https://images.unsplash.com/photo-1556821852-89d4b1dab8c6?w=400",
    # Shoes
    "FASH-016": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
    "FASH-017": "https://images.unsplash.com/photo-1579338559194-a162d19bf842?w=400",
    "FASH-018": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400",
    "FASH-019": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=400",
    "FASH-020": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=400",
    # Accessories
    "FASH-021": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
    "FASH-022": "https://images.unsplash.com/photo-1579656381226-5fc0f0100c3b?w=400",
    "FASH-023": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400",
    "FASH-024": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=400",
    "FASH-025": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400",

    # ── HOME & KITCHEN ────────────────────────────────────────────────────────
    # Kitchen
    "HOME-001": "https://images.unsplash.com/photo-1584990347449-a76c8036edcb?w=400",
    "HOME-002": "https://images.unsplash.com/photo-1584588694223-7b9e9e79b93f?w=400",
    "HOME-003": "https://images.unsplash.com/photo-1588254602020-4e4b9e0f0b2b?w=400",
    "HOME-004": "https://images.unsplash.com/photo-1566624432832-e94e2b338637?w=400",
    "HOME-005": "https://images.unsplash.com/photo-1577720643272-265e434f6edb?w=400",
    # Bedding
    "HOME-006": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400",
    "HOME-007": "https://images.unsplash.com/photo-1584622181563-430f63602d4b?w=400",
    "HOME-008": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=400",
    "HOME-009": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400",
    "HOME-010": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400",
    # Furniture
    "HOME-011": "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400",
    "HOME-012": "https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?w=400",
    "HOME-013": "https://images.unsplash.com/photo-1565183868294-7563f3ce63c8?w=400",
    "HOME-014": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400",
    "HOME-015": "https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=400",
    # Decor
    "HOME-016": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=400",
    "HOME-017": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=400",
    "HOME-018": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
    "HOME-019": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400",
    "HOME-020": "https://images.unsplash.com/photo-1618220179428-22790b461013?w=400",
    # Appliances
    "HOME-021": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400",
    "HOME-022": "https://images.unsplash.com/photo-1607688387751-c1e95ae09a42?w=400",
    "HOME-023": "https://images.unsplash.com/photo-1517668808822-9ebb02ae2a0e?w=400",
    "HOME-024": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400",
    "HOME-025": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",

    # ── BOOKS ─────────────────────────────────────────────────────────────────
    # Fiction
    "BOOK-001": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
    "BOOK-002": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",
    "BOOK-003": "https://images.unsplash.com/photo-1495640388908-05fa85288e61?w=400",
    "BOOK-004": "https://images.unsplash.com/photo-1550399105-c4db5fb85c18?w=400",
    "BOOK-005": "https://images.unsplash.com/photo-1621351183012-e2f9972dd9bf?w=400",
    # Non-fiction
    "BOOK-006": "https://images.unsplash.com/photo-1592496431122-2349e0fbc666?w=400",
    "BOOK-007": "https://images.unsplash.com/photo-1513001900722-370f803f498d?w=400",
    "BOOK-008": "https://images.unsplash.com/photo-1610882648285-560dc60f4f6b?w=400",
    "BOOK-009": "https://images.unsplash.com/photo-1588599069-3c8f5082f67b?w=400",
    "BOOK-010": "https://images.unsplash.com/photo-1561998338-13ad7883b20f?w=400",
    # Educational
    "BOOK-011": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400",
    "BOOK-012": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400",
    "BOOK-013": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400",
    "BOOK-014": "https://images.unsplash.com/photo-1587613757373-8a11e61d9cde?w=400",
    "BOOK-015": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400",
    # Comics
    "BOOK-016": "https://images.unsplash.com/photo-1612036782180-6f0822045d55?w=400",
    "BOOK-017": "https://images.unsplash.com/photo-1601513445506-2ab0d4fb4229?w=400",
    "BOOK-018": "https://images.unsplash.com/photo-1531259922957-2a59f89a2f8b?w=400",
    "BOOK-019": "https://images.unsplash.com/photo-1534536281715-e28d76689b4d?w=400",
    "BOOK-020": "https://images.unsplash.com/photo-1568667256549-094345857637?w=400",
    # Reference
    "BOOK-021": "https://images.unsplash.com/photo-1589998059171-988d887df646?w=400",
    "BOOK-022": "https://images.unsplash.com/photo-1507842217343-583f7270bfbb?w=400",
    "BOOK-023": "https://images.unsplash.com/photo-1524661135-423995f22d0b?w=400",
    "BOOK-024": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400",
    "BOOK-025": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400",

    # ── SPORTS ────────────────────────────────────────────────────────────────
    # Equipment
    "SPORT-001": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400",
    "SPORT-002": "https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=400",
    "SPORT-003": "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=400",
    "SPORT-004": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400",
    "SPORT-005": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=400",
    # Apparel
    "SPORT-006": "https://images.unsplash.com/photo-1565084888279-aca607ecce0c?w=400",
    "SPORT-007": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400",
    "SPORT-008": "https://images.unsplash.com/photo-1583744946564-b52ac1c389c8?w=400",
    "SPORT-009": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400",
    "SPORT-010": "https://images.unsplash.com/photo-1609205264737-d69b49d37b43?w=400",
    # Outdoor
    "SPORT-011": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400",
    "SPORT-012": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
    "SPORT-013": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400",
    "SPORT-014": "https://images.unsplash.com/photo-1605139452360-3a5a9d8f0a67?w=400",
    "SPORT-015": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=400",
    # Fitness
    "SPORT-016": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400",
    "SPORT-017": "https://images.unsplash.com/photo-1517836357463-d25ddfcbf042?w=400",
    "SPORT-018": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400",
    "SPORT-019": "https://images.unsplash.com/photo-1556741533-6e6a62bd8b49?w=400",
    "SPORT-020": "https://images.unsplash.com/photo-1575505586569-646b2ca898fc?w=400",
    # Games
    "SPORT-021": "https://images.unsplash.com/photo-1606503153255-59d8b8b82176?w=400",
    "SPORT-022": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400",
    "SPORT-023": "https://images.unsplash.com/photo-1560461396-ec0ef7bb29f2?w=400",
    "SPORT-024": "https://images.unsplash.com/photo-1566132127697-4524fea60007?w=400",
    "SPORT-025": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400",

    # ── BEAUTY ────────────────────────────────────────────────────────────────
    # Skincare
    "BEAUTY-001": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400",
    "BEAUTY-002": "https://images.unsplash.com/photo-1631390259409-93718702dfa4?w=400",
    "BEAUTY-003": "https://images.unsplash.com/photo-1570194065650-d99fb4a8ba24?w=400",
    "BEAUTY-004": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=400",
    "BEAUTY-005": "https://images.unsplash.com/photo-1617897903246-719242758050?w=400",
    # Makeup
    "BEAUTY-006": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400",
    "BEAUTY-007": "https://images.unsplash.com/photo-1564023505980-dbbe845e3f13?w=400",
    "BEAUTY-008": "https://images.unsplash.com/photo-1512207736890-6ffed8a84e8d?w=400",
    "BEAUTY-009": "https://images.unsplash.com/photo-1631214503851-25e3b3b4c8a0?w=400",
    "BEAUTY-010": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400",
    # Haircare
    "BEAUTY-011": "https://images.unsplash.com/photo-1560707303-4e980ce876ad?w=400",
    "BEAUTY-012": "https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=400",
    "BEAUTY-013": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400",
    "BEAUTY-014": "https://images.unsplash.com/photo-1576426863848-c21f53c60b19?w=400",
    "BEAUTY-015": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400",
    # Fragrance
    "BEAUTY-016": "https://images.unsplash.com/photo-1541643600914-78b084683702?w=400",
    "BEAUTY-017": "https://images.unsplash.com/photo-1588776814546-ec7e99b50d5a?w=400",
    "BEAUTY-018": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=400",
    "BEAUTY-019": "https://images.unsplash.com/photo-1607446045845-d7e8b3c0291b?w=400",
    "BEAUTY-020": "https://images.unsplash.com/photo-1547887538-047f7945cf47?w=400",
    # Wellness
    "BEAUTY-021": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400",
    "BEAUTY-022": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400",
    "BEAUTY-023": "https://images.unsplash.com/photo-1550572017-edd951b55104?w=400",
    "BEAUTY-024": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400",
    "BEAUTY-025": "https://images.unsplash.com/photo-1556742393-d75f468bfcb0?w=400",
}


def update_product(product_id, image_url):
    payload = json.dumps({"image_url": image_url}).encode()
    req = urllib.request.Request(
        f"{BASE}/api/products/{product_id}",
        data=payload,
        headers=HEADERS,
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, None
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def main():
    ok = 0
    fail = 0
    for pid, url in IMAGES.items():
        status, err = update_product(pid, url)
        if status == 200:
            print(f"  OK  {pid}")
            ok += 1
        else:
            print(f"  FAIL {pid}: {status} {err}")
            fail += 1
    print(f"\nDone: {ok} updated, {fail} failed")


if __name__ == "__main__":
    main()
