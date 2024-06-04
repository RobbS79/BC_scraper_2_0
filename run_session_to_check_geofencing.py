import time
from scraper_functions import ScrapeBusinessCentral

list_of_transportations = []
with open("BEP179_transportations.txt", "r") as f:
    for line in f.readlines():
        list_of_transportations.append(line.split("\n")[0])
    f.close()

set_list_of_transportations = set(list_of_transportations)

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
        #file.write(result[0])
        transport_no_2 = result[0][0][0]
        transport_type_2 = result[0][0][3]
        transport_time_2 = result[0][0][1]
        transport_odometer_2 = result[0][0][2]
        transport_no_1 = result[0][1][0]
        transport_type_1 = result[0][1][3]
        transport_time_1 = result[0][1][1]
        transport_odometer_1 = result[0][1][2]
        print(time.time() - time_0)
        file.write(f"{transport_no_2},{transport_type_2},{transport_time_2},{transport_odometer_2}\n")
        file.write(f"{transport_no_1},{transport_type_1},{transport_time_1},{transport_odometer_1}\n")

