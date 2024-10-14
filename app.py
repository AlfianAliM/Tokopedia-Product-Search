# Import Library
import streamlit as st
import requests
import pandas as pd
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials

# Application Title
st.title("Scrape Product")
st.write("Used to search for products on Tokopedia")

# URL dan Header API
url_target = 'https://gql.tokopedia.com/graphql/SearchProductQueryV4'

header = {'authority': 'gql.tokopedia.com',
   'accept': '*/*',
   'accept-language': 'en-US,en;q=0.9',
   'content-type': 'application/json',
   'cookie': 'bm_sz=1E836F185136E04E74B51EF86E5BDF0D~YAAQrO84F6cvDqSFAQAAqM4nvRJ4T99ecI0m0pa5qvWMwVcejybNmPGjX2S4l5Z8wgiEcYP91OKTzUDvK+imI1QaRyKsW6TXjmoGgZYU7P7P9MkMleJmSDIwtHIEeAi4eYFReuLCvQrXcEqFR6MS4UWVXUQb6etuobmBxWscyeD7xYDiLpfosZlMkMfg73LeeeQq7znLHk9tCw8KK76egznjcMkS/FLZdc7WwFqoCMSKO8k507nJWAzW3NGmBC9uusoisgQ/zqhc9ICWU7gecWUgbXIo/lEccZ8Dtx/FFz6NdvnR5nM=~4473657~3618104; _abck=4BB94791FDA138839DBD53D376980B58~0~YAAQrO84F7AvDqSFAQAAwtEnvQnPuKPW1+x0m7YyBDCuLoTMT61FlSnzyfxR19SiDp5+FQ84es5OIPLlEFU6h6KOYOEbdtfanzvLg8RMvULumin7nVDn1QyA1XsUkWMVi67PsLdxHbUZCUZzol07tUzJjRMgEoM8t8URu/Bh8ZR9aj4gSXKjI1fFZCuaKyErdxbXOzLFJQEwZ12rXHC6WeD/CSnOFXBSr6+TrWjYrrfBMW0D78xtuiD7oZRyplNSiLMXuw2jMvgm1ncrB4KbR9SJaVvYaU1H9baK4tPXh7SXCx6onnhRkD2MD4JmHwhXT2SzxeCdDDe2HGvIHpkeL6cDtaO/U2WLWvkHjjtn7mI+YH3sWI8xLGJM9+5MvyPEZf+vSMH0nqHX28NEBx9eV+JlvFhqesoKS99f~-1~-1~-1; ak_bmsc=4648C9E4EAA900EC69C8B11A4FAC84B8~000000000000000000000000000000~YAAQrO84F8AvDqSFAQAAQtQnvRLJGzy3MBKDPA3YQ7NzeqDunDl+IqNed2me/0iFRtJBRNqJdfuwfgG3oWmruD6l4eFHeuuNu1k5hNbcJ1pCqYV/qZHLQwa/oca6HO1XmcJtTSk0NrE0Lk0+7BF/6HABNneso2UmLUh+LG15oLb+E24WxUmhwleloJuXkJb+ZJHPgyc5+R2l1M/4iPp4sOojHjRvIGHgiZVqKLr/hDtpmOFmPRt4mMgQ/tjiwajHSHIZRKkh35ptoXSWIe7uIBZaxBhcxHB2wr6/Ut8EiETI7ucMfS3T0dQXNhhy41YcRMUXZv1ch/p5ndJREJPot8gtclT9B29fjjDyVhZzeBJc+NwguInrbN5jOm118yJCD9FLsga0r0V133JonKbjUmZCJ8OCdOThXqVeB5+hEGMh5TQfJ+VAkQf0GIaVrWcLjYYqFpFuxt/Z3pLoFIuCJzH6R2eNRKrTwR0OvPDd4YKX/rAp9WoMjjB1r8INrQ==; _gcl_au=1.1.552859224.1673915783; _gid=GA1.2.11588955.1673915783; _SID_Tokopedia_=oo-XU21_oLw66N2meBymK1H_oZlyKWPqicl6z6jitUcjy3nV27xHSym9b-DR0K3rTmKv_BjNgn9q10HwRUyxLcletHybjRIDZ0k3vbXvBbtu1fRe_cuIy_omDYVAMfBy; DID=7f122be4279d38899262d75489d5b6e52a7781afd3577f26db23d9dee321429a73d344239cadaa4562db45ea2341e913; DID_JS=N2YxMjJiZTQyNzlkMzg4OTkyNjJkNzU0ODlkNWI2ZTUyYTc3ODFhZmQzNTc3ZjI2ZGIyM2Q5ZGVlMzIxNDI5YTczZDM0NDIzOWNhZGFhNDU2MmRiNDVlYTIzNDFlOTEz47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; _UUID_NONLOGIN_=6003aca41edf75450ef4ee2ca669b8f6; AMP_TOKEN=%24NOT_FOUND; _UUID_CAS_=5f3cbab6-c66f-4202-a342-d2fbe6845be1; _CASE_=742d6b466b2d353d3d383b232d6e466b2d353f232d636d632d352d456e646e7d7b6e2f5f7a7c6e7b2d232d6c466b2d353e3839232d636061682d352d2d232d636e7b2d352d2d232d7f4c602d352d2d232d78466b2d353e3d3d3e3f3c383a232d7c466b2d353e3e3a3c3f3a383c232d7c5b767f6a2d352d3d672d232d78677c2d352d5474532d786e7d6a67607a7c6a50666b532d353e3d3d3e3f3c383a23532d7c6a7d79666c6a507b767f6a532d35532d3d67532d23532d50507b767f6a616e626a532d35532d586e7d6a67607a7c6a7c532d722374532d786e7d6a67607a7c6a50666b532d353f23532d7c6a7d79666c6a507b767f6a532d35532d3e3a62532d23532d50507b767f6a616e626a532d35532d586e7d6a67607a7c6a7c532d72522d232d635a7f6b2d352d3d3f3d3c223f3e223e385b3f38353c39353d3b243f38353f3f2d72; __asc=e6b7c311185bd27ed2b24af570d; __auc=e6b7c311185bd27ed2b24af570d; _gat_UA-9801603-1=1; _dc_gtm_UA-126956641-6=1; _dc_gtm_UA-9801603-1=1; _ga_70947XW48P=GS1.1.1673915783.1.1.1673916777.50.0.0; _ga=GA1.1.1571217160.1673915783',
   'origin': 'https://www.tokopedia.com',
   'referer': 'https://www.tokopedia.com/search?st=product&q={keyword}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=',
   'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'empty',
   'sec-fetch-mode': 'cors',
   'sec-fetch-site': 'same-site',
   'tkpd-userid': '0',
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
   'x-device': 'desktop-0.0',
   'x-source': 'tokopedia-lite',
   'x-tkpd-lite-service': 'zeus',
   'x-version': '68ba647'}

# User Input
keyword = st.text_input("Masukkan keyword: ")

# Query GraphQL
query = f'[{{"operationName":"SearchProductQueryV4","variables":{{"params":"device=desktop&navsource=&ob=23&page=1&q={keyword}&related=true&rows=250&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&start=0&topads_bucket=true&unique_id=6003aca41edf75450ef4ee2ca669b8f6&user_addressId=&user_cityId=176&user_districtId=2274&user_id=&user_lat=&user_long=&user_postCode=&user_warehouseId=12210375&variants="}},"query":"query SearchProductQueryV4($params: String\u0021) {{\\n  ace_search_product_v4(params: $params) {{\\n    header {{\\n      totalData\\n      totalDataText\\n      processTime\\n      responseCode\\n      errorMessage\\n      additionalParams\\n      keywordProcess\\n      componentId\\n      __typename\\n    }}\\n    data {{\\n      banner {{\\n        position\\n        text\\n        imageUrl\\n        url\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      backendFilters\\n      isQuerySafe\\n      ticker {{\\n        text\\n        query\\n        typeId\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      redirection {{\\n        redirectUrl\\n        departmentId\\n        __typename\\n      }}\\n      related {{\\n        position\\n        trackingOption\\n        relatedKeyword\\n        otherRelated {{\\n          keyword\\n          url\\n          product {{\\n            id\\n            name\\n            price\\n            imageUrl\\n            rating\\n            countReview\\n            url\\n            priceStr\\n            wishlist\\n            shop {{\\n              city\\n              isOfficial\\n              isPowerBadge\\n              __typename\\n            }}\\n            ads {{\\n              adsId: id\\n              productClickUrl\\n              productWishlistUrl\\n              shopClickUrl\\n              productViewUrl\\n              __typename\\n            }}\\n            badges {{\\n              title\\n              imageUrl\\n              show\\n              __typename\\n            }}\\n            ratingAverage\\n            labelGroups {{\\n              position\\n              type\\n              title\\n              url\\n              __typename\\n            }}\\n            componentId\\n            __typename\\n          }}\\n          componentId\\n          __typename\\n        }}\\n        __typename\\n      }}\\n      suggestion {{\\n        currentKeyword\\n        suggestion\\n        suggestionCount\\n        instead\\n        insteadCount\\n        query\\n        text\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      products {{\\n        id\\n        name\\n        ads {{\\n          adsId: id\\n          productClickUrl\\n          productWishlistUrl\\n          productViewUrl\\n          __typename\\n        }}\\n        badges {{\\n          title\\n          imageUrl\\n          show\\n          __typename\\n        }}\\n        category: departmentId\\n        categoryBreadcrumb\\n        categoryId\\n        categoryName\\n        countReview\\n        customVideoURL\\n        discountPercentage\\n        gaKey\\n        imageUrl\\n        labelGroups {{\\n          position\\n          title\\n          type\\n          url\\n          __typename\\n        }}\\n        originalPrice\\n        price\\n        priceRange\\n        rating\\n        ratingAverage\\n        shop {{\\n          shopId: id\\n          name\\n          url\\n          city\\n          isOfficial\\n          isPowerBadge\\n          __typename\\n        }}\\n        url\\n        wishlist\\n        sourceEngine: source_engine\\n        __typename\\n      }}\\n      violation {{\\n        headerText\\n        descriptionText\\n        imageURL\\n        ctaURL\\n        ctaApplink\\n        buttonText\\n        buttonType\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\n"}}]'

response = requests.post(url_target,headers=header,data=query)
products = response.json()[0]['data']['ace_search_product_v4']['data']['products']

df = pd.DataFrame(products)

df = df.fillna("")

# Function to extract the number of sales from 'title'
def extract_sales(label_groups):
    # Find the entry with position 'integrity'
    integrity_entry = next((item for item in label_groups if item['position'] == 'integrity'), None)
    if integrity_entry:
        title = integrity_entry['title']
        # If 'rb' is found, extract the number and multiply by 1000
        if 'rb' in title.lower():  # Ensure 'rb' check is case-insensitive
            match = re.search(r'(\d+)', title)
            if match:
                return int(match.group()) * 1000
        # Extract the number from 'title', ignoring non-digit characters
        match = re.search(r'\d+', title)
        if match:
            return int(match.group())
    return None

# Add the new column 'sales_count' to the DataFrame
df['sales_count'] = df['labelGroups'].apply(extract_sales)

if 'countReview' in df.columns:
    df['countReview'] = pd.to_numeric(df['countReview'], errors='coerce')  # Convert to numeric
    # Sort by countReview
    df = df.sort_values(by='countReview', ascending=False)
else:
    st.warning("The 'countReview' column was not found in the data.")

df = df.astype(str)
print(df)
df.to_csv(f'tokopedia_{keyword}.csv', index=False)
st.write("Search results:")
st.table(df)

# Setting scope and authentication using credentials.json
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('path_file_credentials', scope)
client = gspread.authorize(creds)

spreadsheet_id = '1IWnJnm0-CFeiiEtgSqwfxKhVjv1u29vAS9ZBoIGzLug'

# Opening a Google Spreadsheet with the given ID
try:
    spreadsheet = client.open_by_key(spreadsheet_id)
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"Spreadsheet with ID '{spreadsheet_id}' not found. Please ensure the ID is correct and you have sufficient access.")
    st.stop()

# Checking if a sheet with the keyword name already exists
try:
    sheet = spreadsheet.worksheet(keyword)
    # If the sheet exists, then clear the data inside it
    sheet.clear()
    st.info(f"Sheet '{keyword}' already exists and will be updated.")
except gspread.exceptions.WorksheetNotFound:
    # If the sheet does not exist, create a new sheet
    sheet = spreadsheet.add_worksheet(title=keyword, rows=df.shape[0], cols=df.shape[1])
    st.info(f"Sheet '{keyword}' does not exist yet, creating a new sheet.")

# Send data to Spreadsheet
sheet.update([df.columns.values.tolist()] + df.values.tolist())

st.success("Data successfully sent to Google Spreadsheet with a new sheet name!")
