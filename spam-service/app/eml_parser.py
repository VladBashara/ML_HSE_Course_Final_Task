import re
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup

def parse_eml_bytes(raw):
    if isinstance(raw,str): raw = raw.encode("utf-8","ignore")
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    plain, html = [], []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_maintype()=="multipart": continue
            if part.get("Content-Disposition","").startswith("attachment"): continue
            try: payload = part.get_content()
            except Exception:
                try: payload = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8","ignore")
                except Exception: continue
            if part.get_content_type()=="text/plain": plain.append(payload)
            elif part.get_content_type()=="text/html": html.append(payload)
    else:
        try: payload = msg.get_content()
        except Exception: payload = msg.get_payload(decode=True).decode("utf-8","ignore")
        (html if msg.get_content_type()=="text/html" else plain).append(payload)
    body = "\n".join(plain) if plain else (BeautifulSoup("\n".join(html),"html.parser").get_text(" ") if html else "")
    subj = str(msg.get("Subject",""))
    text = f"{subj}\n{body}".strip()
    sender = str(msg.get("From","")).lower()
    dom = sender.split("@")[-1].strip("> ") if "@" in sender else ""
    urls = re.findall(r"https?://\S+|www\.\S+", body)
    meta = {"sender_domain":dom,"n_urls":len(urls),"has_url":int(len(urls)>0),
            "n_digits":sum(c.isdigit() for c in body),"n_excl":body.count("!"),
            "n_upper":sum(c.isupper() for c in body),"len":len(body)}
    return text, meta
