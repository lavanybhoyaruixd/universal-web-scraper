from bs4 import BeautifulSoup
import os
import pandas as pd

d = {'title': [], 'price': [], 'link': []}

for file in os.listdir("data"):
    try:
        with open(f"data/{file}", encoding="utf-8") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')

        # Title + Link
        t = soup.find("h2")
        if t:
            a_tag = t.find("a")
            title = t.get_text(strip=True) if t else ""
            link = "https://www.amazon.in" + a_tag['href'] if a_tag and a_tag.has_attr("href") else ""
        else:
            title, link = "", ""

        # Price
        p = soup.find("span", class_="a-price-whole")
        price = p.get_text(strip=True) if p else ""

        # Store
        if title:
            d['title'].append(title)
            d['price'].append(price)
            d['link'].append(link)

    except Exception as e:
        print(f"⚠️ Error in {file}: {e}")

# Save collected data
df = pd.DataFrame(d)
df.to_csv("data/data.csv", index=False, encoding="utf-8")
print(f"✅ Saved {len(df)} products into data/data.csv")
