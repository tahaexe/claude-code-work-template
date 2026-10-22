# Store and portal record
<!-- Every store and portal fact the next agent needs (PROTOKOL §5): read before store, portal or console work; each event is written when it happens. Texts, forms and answers live in `store/` (last section). Never a secret (key, password, token). Past ~15,000 characters → the oldest log lines to `hafiza/arsiv/magaza.md`. No store or portal yet → a dated line saying so; an empty section → —. -->

## IDs
<!-- Only what isn't secret: package (Android), bundle (iOS), App Store app ID and SKU, Play app ID, developer and team IDs, portal and Steam app IDs, ad unit names (an ID only if the app ships it anyway); Game Center and Play Games IDs, or the file that holds them. -->
- ‹store: ID›

## Listing names
<!-- Per store and language: the title (App Store subtitle too); full texts in `store/`. -->
- ‹store · language: title›

## Store-state log
<!-- Newest first, one line per event: `YYYY-MM-DD · store · version (build) · submitted | approved | rejected (guideline, short reason) | released | removed → decision taken (source)`. -->
- ‹YYYY-MM-DD · store · version · event → decision›

## Products and prices
<!-- In-app products: ID · type · price (base; rows that differ by country) · where in code. -->
- ‹product ID · type · price›

## Where forms and answers live
<!-- The `store/` files: listing texts per language, privacy and data-safety answers, content rating, review notes, the claims ledger `store/facts.md`, announcements `store/duyuru/`; consoles used (names only). -->
- ‹`store/…`: what›
