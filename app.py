from flask import Flask, jsonify, request
from playwright.sync_api import Playwright, sync_playwright

app = Flask(__name__)

m_details = []


@app.route('/api', methods=['GET'])
def temp():
    query = str(request.args['Query'])
    opt = int(request.args['num'])
    mg_links = []
    def run(playwright: Playwright) -> None:
        m_details.clear()
        browser = playwright.chromium.launch(headless=True, chromium_sandbox=False,)
        context = browser.new_context()
        page = context.new_page()
        page.goto('https://www.google.com/search?q=' + query + '%201mg')
        links = page.query_selector_all('.yuRUbf > a')
        for i in links:
            mg_link = str(i.get_attribute('href'))
            if mg_link.__contains__("1mg.com/drugs") or mg_link.__contains__("1mg.com/otc"):
                print(mg_link)
                mg_links.append(mg_link)
        var = len(mg_links)
        for i in range(0, var):
            mydict = {}
            print(mg_links[i])
            link = mg_links[i]
            if link.__contains__("/drugs"):
                page1 = context.new_page()
                try:
                    page1.goto(link, wait_until="load",timeout=5000)
                except Exception:
                    print("pageLoad Failed")

                baned = 0
                try:
                    isbanned = str(page1.query_selector('.DrugPriceBox__banned-container___3ngUi div').inner_text())
                    if isbanned.capitalize().__contains__("BANNED"):
                        baned += 1
                        mydict['banned'] = baned
                except:
                    print("::::This Is Not Banned Medicine::::")
                try:
                    name = str(page1.query_selector('.DrugHeader__title-content___2ZaPo').inner_text())
                    mydict['name'] = name
                except:
                    print("e-name")
                if name != '':

                    try:
                        benefits = page1.query_selector('.ShowMoreArray__tile___2mFZk div').inner_text()
                        mydict['benefits'] = benefits
                    except:
                        print("e-benefits")

                    try:
                        manufacturer = page1.query_selector('.DrugHeader__meta___B3BcU:nth-child(1) a').inner_text()
                        mydict['manufacturer'] = manufacturer
                    except:
                        print('e-manufacturer')

                    try:
                        image = page1.query_selector('.style__loaded___22epL').get_attribute("src")
                        mydict['image'] = image
                    except:
                        print('e-image')

                    try:
                        composition = page1.query_selector('.saltInfo a').inner_text()
                        mydict['composition'] = composition
                    except:
                        print('e-composition')

                    try:
                        mrp1 = page1.query_selector('.DrugPriceBox__price___dj2lv').inner_text()
                        mydict['mrp1'] = mrp1
                    except:
                        print("e-mrp1")
                    try:
                        mrp2 = page1.query_selector('.PriceBoxPlanOption__offer-price-cp___2QPU_').inner_text()
                        mydict['mrp2'] = mrp2
                    except:
                        print("e-mrp2")
                    try:
                        storage1 = page1.query_selector(
                            '.DrugHeader__meta___B3BcU:nth-child(4) .DrugHeader__meta-value___vqYM0').inner_text()
                        mydict['storage1'] = storage1

                    except:
                        print("e-storage1")
                    try:
                        storage2 = page1.query_selector(
                            '.DrugHeader__meta___B3BcU~ .DrugHeader__meta___B3BcU+ .DrugHeader__meta___B3BcU .DrugHeader__meta-value___vqYM0 , .PriceBoxPlanOption__offer-price-cp___2QPU_').inner_text()
                        mydict['storage2'] = storage2

                    except:
                        print("e-storage2")
                    try:
                        intro = page1.query_selector('#overview .DrugOverview__content___22ZBX').inner_text()
                        mydict['intro'] = intro
                    except:
                        print("e-intro")
                    try:
                        uses = page1.query_selector('#uses_and_benefits .DrugPane__content___3-yrB').inner_text()
                        mydict['uses'] = uses
                    except:
                        print("e-uses")
                    try:
                        side_effects = page1.query_selector('#side_effects .DrugPane__content___3-yrB').inner_text()
                        mydict['side_effects'] = side_effects
                    except:
                        print("e-side_effects")
                    try:
                        how_to_use = page1.query_selector('#how_to_use .DrugPane__content___3-yrB').inner_text()
                        mydict['how_to_use'] = how_to_use
                    except:
                        print("e-how_to_use")
                    try:
                        how_it_works = page1.query_selector('#how_drug_works .DrugPane__content___3-yrB').inner_text()
                        mydict['how_it_works'] = how_it_works
                    except:
                        print('e-how_it_works')
                    try:
                        se_alcohol = page1.query_selector(
                            '#safety_advice .DrugOverview__content___22ZBX.DrugOverview__content___22ZBX:nth-child(2)').inner_text()
                        mydict['se_alcohol'] = se_alcohol

                        se_pregnancy = page1.query_selector('.DrugOverview__content___22ZBX:nth-child(4)').inner_text()
                        mydict['se_pregnancy'] = se_pregnancy

                        se_breast_feeding = page1.query_selector(
                            '.DrugOverview__content___22ZBX:nth-child(6)').inner_text()
                        mydict['se_breast_feeding'] = se_breast_feeding

                        se_driving = page1.query_selector('.DrugOverview__content___22ZBX:nth-child(8)').inner_text()
                        mydict['se_driving'] = se_driving

                        se_kidney = page1.query_selector('.DrugOverview__content___22ZBX:nth-child(10)').inner_text()
                        mydict['se_kidney'] = se_kidney

                        se_liver = page1.query_selector('.DrugOverview__content___22ZBX:nth-child(12)').inner_text()
                        mydict['se_liver'] = se_liver

                    except:
                        print("e-safty_klp")
                    try:
                        if_forgotten = page1.query_selector('#missed_dose .DrugOverview__content___22ZBX').inner_text()
                        mydict['if_forgotten'] = if_forgotten

                    except:
                        print("e-ifforgot")
                    try:
                        quick_tips = page1.query_selector('.ExpertAdviceItem__content___1Djk2').inner_text()
                        mydict['quick_tips'] = quick_tips

                    except:
                        print("e-quick_tips")
                    try:
                        fact_box = page1.query_selector('.DrugFactBox__black___5cVbb').inner_text()
                        mydict['fact_box'] = fact_box
                    except:
                        print("e-fact")
                    try:
                        faq = page1.query_selector('#faq .DrugPane__content___3-yrB').inner_text()
                        mydict['faq'] = faq
                    except:
                        print("e-faq")
                    m_details.append(mydict)

            elif link.__contains__("/otc"):
                page1 = context.new_page()
                page1.goto(link, wait_until="load",timeout=5000)
                try:
                    name = str(page1.query_selector('.ProductTitle__product-title___3QMYH').inner_text())

                except:
                    print("e-name")
                if name != '':
                    mydict['name'] = name
                    try:
                        image = page1.query_selector('.Thumbnail__thumbnail-image-new___3rsF_').get_attribute("src")
                        mydict['image'] = image
                    except:
                        print("e-image")
                    try:
                        product_highlight = page1.query_selector(
                            '.ProductHighlights__product-highlights___2jAF5').inner_text()
                        mydict['product_highlight'] = product_highlight
                    except:
                        print("e-highlights")
                    try:
                        mrp1 = page1.query_selector('.PriceBoxPlanOption__offer-price-cp___2QPU_').inner_text()
                        mydict['mrp1'] = mrp1

                    except:
                        print("e-mrp1")
                    try:
                        mrp2 = page1.query_selector('.OtcVariants__header___2q6Sa+ div').inner_text()
                        mydict['mrp2'] = mrp2

                    except:
                        print("e-mrp2")
                    try:
                        manufacturer = page1.query_selector('.ProductTitle__manufacturer___sTfon a').inner_text()
                        mydict['manufacturer'] = manufacturer
                    except:
                        print("e-manufacture")
                    try:
                        rating = page1.query_selector('.RatingDisplay__ratings-container___3oUuo').text_content()
                        mydict['rating'] = rating
                    except:
                        print("e-rating")
                    try:
                        intro = page1.query_selector('.ProductDescription__description-content___A_qCZ').inner_text()
                        mydict['intro'] = intro
                    except:
                        print("e-intro")
                    m_details.append(mydict)
            if opt == 0:
                break

        context.close()
        browser.close()
    with sync_playwright() as playwright:
        run(playwright)
    return jsonify(m_details)


if __name__ == '__main__':
    app.run()

