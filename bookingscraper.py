#Import Statements für Scraper
from playwright.sync_api import sync_playwright
import pandas as pd




def main():
    
    with sync_playwright() as p:

        checkin_date = '2024-05-25'
        checkout_date = '2024-05-26'
        
        base_url = f'https://www.booking.com/searchresults.html?ss=Switzerland&ssne=Switzerland&ssne_untouched=Switzerland&efdco=1&label=gen173nr-1FCAQoggI46wdIMVgEaCyIAQGYATG4ARfIAQzYAQHoAQH4AQOIAgGoAgO4ArGXwa8GwAIB0gIkODRjM2NjNzItZmU3Mi00YmNlLTliMDYtOTViMDJjNDhhMGZi2AIF4AIB&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=204&dest_type=country&checkin={checkin_date}&checkout={checkout_date}&group_adults=1&no_rooms=1&group_children=0'
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        hotels_list = []

        for page_num in range(10):  # 10 Seiten durchgehen mit jeweils 25 Datensätzen
            offset = page_num * 25
            page_url = f"{base_url}&offset={offset}"
            page.goto(page_url, timeout=60000)
            page.wait_for_timeout(10000)
           

        

            hotels = page.locator('//div[@data-testid="property-card"]').all()
        

        
            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
                hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
                hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
                hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
                hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]
                hotel_dict['address'] = hotel.locator('//span[@data-testid="address"]').inner_text()
                hotel_dict["date"] = checkin_date
                
                hotels_list.append(hotel_dict)

            print(f"Page {page_num + 1} processed")

        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False)
        df.to_csv('hotels_list.csv', index=False)

        browser.close()

if __name__ == '__main__':
    main()