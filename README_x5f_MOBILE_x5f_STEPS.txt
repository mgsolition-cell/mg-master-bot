
MG MASTER BOT V2 - MOBILE FULL GUIDE
=====================================

FILES LIST:
1. app.py - Main bot + admin + payment
2. dashboard.html - Full admin panel (5 tabs)
3. requirements.txt - Libraries
4. clients.json - Client database
5. .env - API keys

API EDHUKKANUM - STEP BY STEP:

A) META GRAPH API (Insta + FB Auto Post ku) - FREE
--------------------------------------------------
1. developers.facebook.com poi login pannu (FB account)
2. My Apps -> Create App -> Business -> Name: MG Bot
3. Dashboard la -> Products -> Instagram Graph API + Facebook Pages -> Setup
4. Tools -> Graph API Explorer:
   - Select App: MG Bot
   - Permissions add pannu: pages_show_list, pages_read_engagement, instagram_basic, instagram_content_publish, pages_manage_posts
   - Generate Token -> Copy (Long lived token eduthuko)
5. Pages list edukka: /me/accounts nu query pannu -> Page ID + IG ID varum
6. .env file la paste pannu:
   META_ACCESS_TOKEN=EAAG....
   META_PAGE_ID=123456
   META_IG_ID=178414...

NOTE: First ku token venam na manual post pannalam - bot QR + content generate pannum, nee copy paste pannalam.

B) WHATSAPP CLOUD API - FREE (1000 msgs/month)
----------------------------------------------
1. developers.facebook.com -> Same app MG Bot
2. Products -> WhatsApp -> Setup
3. API Setup la Phone Number ID + Token copy pannu
4. .env la:
   WHATSAPP_TOKEN=EAA...
   WHATSAPP_PHONE_ID=123456789

Ithu illa na kooda bot work agum - WhatsApp link manual anuppalam.

C) UPI - ALREADY DONE
----------------------
UPI: 8940498738@ybl - No API needed, direct GPay

DEPLOYMENT - MOBILE LA:
------------------------
Option 1: RENDER (Recommended)
- render.com -> Sign up with GitHub
- New Web Service -> Connect mg-master-bot repo
- Build: pip install -r requirements.txt
- Start: python app.py
- Deploy -> Live!

Option 2: REPLIT (Easiest for mobile)
- replit.com -> Create Repl -> Import GitHub
- Run button -> Live!

FIRST CLIENT ADD:
-----------------
Admin panel -> Add Client -> Shop name, phone, plan 1000 -> Create
Pay link: /pay/1000 -> Client ku share
GPay notification -> Admin la Paid nu mark

POSTING:
--------
/api/post_all nu cron job daily 2 times set pannu (cron-job.org free)
Illana manual: Admin la Post Now button

WALLET:
-------
Client Rs.100 add panna /pay/100 -> Wallet +100
Bot daily check panni ad run pannum (Meta Ads API add panna)

SUPPORT: Any doubt - message pannu
