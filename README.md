# BC_scraper_2_0
The project is being developed in order to increase time-efficiency of testing 
the implementation of geofencing technology at my current employer's IT ecosystem.

- TMS software responsible for monitoring of production and transportations is built
on MS BusinessCentral (perhaps 2014) and due to the lack of API stack and other
options to access data from it, I decided to develop a webscraper based on selenium
library

1. Create an access folder in project's directory
2. Create a config file which will store credentials to log in to TMS
3. Create a config file which will store urls to access home page,
    or whatever url is needed
4. Install requirements.txt

The result of scraper with demanded data extracted is stored in result folder 
after running scraper_function.py script.
