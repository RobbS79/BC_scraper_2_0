import time
from scraper_functions import ScrapeBusinessCentral

list_of_transportations = []
with open("BEP179_transportations.txt", "r") as f:
    for line in f.readlines():
        list_of_transportations.append(line.split("\n")[0])
    f.close()

set_list_of_transportations = set(list_of_transportations[480:])

route_to_business_central_home_page = ScrapeBusinessCentral()
route_to_business_central_home_page.login_to_business_central()
with open('result_2.txt', 'a') as file:
    json_file = []
    for transportation in set_list_of_transportations:
        time_0 = time.time()
        #print(f"\nTransportation {transportation} start")
        #time.sleep(2)
        route_to_business_central_home_page.filter_by_order_num(transportation)
        #time.sleep(0.5)
        result = route_to_business_central_home_page.locate_transportation_order_rows_DECORATED_2()
        print(transportation,result,"\n",time.time() - time_0)
        file.write(f"{str(result[0])}\n")

