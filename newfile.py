import requests
import time
import re

channel_id = "1437164664776560812"
auth_token = "MTQzNzEwNjMwNjA2MTMwNzk5Nw.GWAUW-.z5rAU5FS0CkozHlcofZu3jKAm-aY-eRgNMZGZo"
target_user_id = "564997004422283294"

reply_texts = [
    "نيكمك", "جلدمك", "حرقمك", "نكحمك", " شطرمك",
    " تشفيرمك", " حفصمك", "نكح كسختك", "طحنمك", "طبخمك",
    "نسفمك", "طيزمك", "رقصمك", "فتحمك", "لكمك",
    "تفجيرمك", "عجنمك", "ركبمك", "طهيمك", "ركلمك",
    "طعنمك", "خبطمك", "لحسمك زب", "فقعمك", "اكلمك",
   "طغيمك", "اخضعمك", "اجلدمك", "انسفمك", "نكحشرفمك",
    "توترمك", "خنقمك", "شويمك", "غسلمك", "حرقمك",
    "ضربمك", "حلبمك", "بيعمك", "طيرانمك لزبي", "نقزمك",
    "تبليلمك", "تحنيطمك", "تخريطمك", "تباهيمك", "تناولمك",
    "تحليمك", "شطحمك", "بقعمك", "شرقمك", "شقمك",
    "تلفمك", "توقفمك", "تشرمطمك", "تقحبنمك", "عرصمك",
    "بعصمك", "تمنيكمك", "لحسكسمك", "بهدلمك", "تفقعمك",
    "تشردمك", "شق حراشفمك", "دعوشمك", "تخورمك", "استعباطمك",
    "شطرمك", "تهرقلمك", "تعقيبمك", "طقعمك", "تفتتمك",
    "توحدمك", "تطوركسمك", "شمكسختك", "سلطنمك", "تبقعمك",
    "كسعمتك", "توسوسمك", "خداعمك", "تفحيطمك", "جنونمك",
    "غضبمك", "حزنكسختك", "مصبزمك", "طلاقمك", "تقزيمك",
    "تفشيمك", "مركلمك", "تفكيكمك", "تحريرمك", "تقليمك",
    "تهويتمك", "تصفيمك", "طرقمك", "وقوعمك", "تلقينمك",
    "تحريفمك", "تغييرمك", "سخونتمك", "تنفسمك", "رعايتمك"
]

handled_ids = set()
reply_index = 0

headers = {
    "authorization": auth_token,
    "Content-Type": "application/json"
}

def clean_text(text):
    text = re.sub(r"[\u064B-\u065F\u0610-\u061A\u06D6-\u06ED]", "", text)
    text = re.sub(r"[^ء-ي]", "", text)
    return text

def is_like_noqt(text):
    cleaned = clean_text(text)
    pattern = r"ن+.ق+.ط+"
    return re.search(pattern, cleaned)

while True:
    try:
        response = requests.get(
            f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=10",
            headers=headers
        )
        messages = response.json()

        if isinstance(messages, list):
            messages = list(reversed(messages))

            for msg in messages:
                msg_id = msg.get("id")
                author = msg.get("author", {})
                author_id = author.get("id")
                content = (msg.get("content") or "").strip()

                if not msg_id or msg_id in handled_ids:
                    continue

                if author_id == target_user_id:
                    cleaned_content = clean_text(content)

                    if is_like_noqt(content):
                        if cleaned_content == "نقط":
                            reply = "."
                        else:
                            reply = f". {reply_texts[reply_index]}"
                            reply_index = (reply_index + 1) % len(reply_texts)
                    else:
                        reply = reply_texts[reply_index]
                        reply_index = (reply_index + 1) % len(reply_texts)

                    payload = {
                        "content": reply,
                        "message_reference": {"message_id": msg_id}
                    }

                    requests.post(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        headers=headers,
                        json=payload
                    )

                    handled_ids.add(msg_id)
                    time.sleep(3)

        time.sleep(3)

    except Exception:
        time.sleep(5)
