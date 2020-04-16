## PHEV Electric Vehicle Scraping Library 
[![Build Status](https://travis-ci.com/eneakllomollari/pscraper-lib.svg?branch=master)](https://travis-ci.com/eneakllomollari/pscraper-lib)

#### Sub-modules
* [pscraper.api](#pscraperapi)
* [pscraper.scraper](#pscraperscraper)
* [pscraper.utils](#pscraperutils)

## pscraper.api
#### Classes
##### Class `API`
> `class API(username, password, localhost=False)` 

Provides the APIs to interact with the database
##### Ancestors (in MRO)
* [pscraper.utils.base_api.BaseAPI](#class-baseapi)
##### Methods
###### Method `history_get`
> `def history_get(self, **kwargs)` 
###### Method `history_post`
> `def history_post(self, **kwargs)` 
###### Method `seller_get`
> `def seller_get(self, **kwargs)` 
###### Method `seller_patch`
> `def seller_patch(self, phone_number, **kwargs)` 
###### Method `seller_post`
> `def seller_post(self, **kwargs)` 
###### Method `vehicle_get`
> `def vehicle_get(self, **kwargs)` 
###### Method `vehicle_patch`
> `def vehicle_patch(self, vin, **kwargs)` 
###### Method `vehicle_post`
> `def vehicle_post(self, **kwargs)` 

## pscraper.scraper
* [pscraper.scraper.marketplaces](#pscraperscrapermarketplaces)

## pscraper.scraper.marketplaces
#### Sub-modules
* [pscraper.scraper.marketplaces.autotrader](#pscraperscrapermarketplacesautotrader)
* [pscraper.scraper.marketplaces.carmax](#pscraperscrapermarketplacescarmax)
* [pscraper.scraper.marketplaces.cars](#pscraperscrapermarketplacescars)
* [pscraper.scraper.marketplaces.consts](#pscraperscrapermarketplacesconsts)
* [pscraper.scraper.marketplaces.helpers](#pscraperscrapermarketplaceshelpers)
#### Functions
##### Function `scrape`
> `def scrape(zip_code, search_radius, target_states, api)`

Scrape data about electric vehicles from all supported marketplaces using the specified parameters
###### Args

**```zip_code```** :&ensp; <code>str</code>
:   The zip code to perform the search in

**```search_radius```** :&ensp; <code>int</code>
:   The search radius for the specified zip code

**```target_states```** :&ensp; <code>list</code>
:   The states to search in (i.e. ``` ['CA', 'NV'] ``` )

**```api```** :&ensp; <code>[API](#class-api)</code>
:   Pscraper API to communicate with the database
###### Returns
<code>list</code> of <code>tuples</code>
:   (time, vehicles) per marketplace

## pscraper.scraper.marketplaces.autotrader
#### Sub-modules
* [pscraper.scraper.marketplaces.autotrader.consts](#pscraperscrapermarketplacesautotraderconsts)
#### Functions
##### Function `scrape_autotrader`
> `def scrape_autotrader(zip_code, search_radius, target_states, api)` 

## pscraper.scraper.marketplaces.autotrader.consts

## pscraper.scraper.marketplaces.carmax
#### Sub-modules
* [pscraper.scraper.marketplaces.carmax.consts](#pscraperscrapermarketplacescarmaxconsts)
#### Functions
##### Function `scrape_carmax`
> `def scrape_carmax(zip_code, search_radius, target_states, api)` 

## pscraper.scraper.marketplaces.carmax.consts

## pscraper.scraper.marketplaces.cars
#### Sub-modules
* [pscraper.scraper.marketplaces.cars.consts](#pscraperscrapermarketplacescarsconsts)
* [pscraper.scraper.marketplaces.cars.helpers](#pscraperscrapermarketplacescarshelpers)
#### Functions
##### Function `scrape_cars`
> `def scrape_cars(zip_code, search_radius, target_states, api)` 

Scrape EV data from cars.com filtering with the specified parameters
##### Args
**```zip_code```** :&ensp; <code>str</code>
:   The zip code to perform the search in

**```search_radius```** :&ensp; <code>int</code>
:   The search radius for the specified zip code

**```target_states```** :&ensp; <code>list</code>
:   The states to search in (i.e. ``` ['CA', 'NV'] ``` )

**```api```** :&ensp; <code>[API](#class-api)</code>
:   Pscraper API to communicate with the backend
###### Returns

**```total```** :&ensp; <code>int</code>
:   Total number of cars scraped 

## pscraper.scraper.marketplaces.cars.consts

## pscraper.scraper.marketplaces.cars.helpers
#### Functions
##### Function `get_cars_com_response`
> `def get_cars_com_response(url, session)` 

Scrapes vehicle and page information from <code>url</code>
###### Args

**```url```** :&ensp; <code>str</code>
:   Url to get the response from

**```session```** :&ensp; <code>requests.sessionsSession</code>
:   Session to use for sending requests
###### Returns
<code>dict</code>
:   Parsed information about the url and the vehicles it contains
##### Function `validate_params`
> `def validate_params(search_radius, target_states)` 

Validates that <code>target\_states</code> are eligible states and <code>search\_radius</code> is valid
###### Args

**```search_radius```** :&ensp; <code>int</code>
:   Radius to scrape in

**```target_states```** :&ensp; <code>list</code>
:   States provided by the scraper

## pscraper.scraper.marketplaces.consts

## pscraper.scraper.marketplaces.helpers
#### Functions
##### Function `get_seller_id`
> `def get_seller_id(vehicle, api, session)` 

Returns a seller id (primary_key). Search for existing seller by phone number.
If not found creates a new seller and returns it's id.
Requires seller to have `streetAddress`, `city` and `state`. If any are missing returns -1.
###### Args

**```vehicle```** :&ensp; <code>dict</code>
:   Vehicle whose seller needs to be created/searched

**```api```** :&ensp;  <code>[API](#class-api)</code>
:   Pscraper api, that allows retrieval/creation of marketplaces

**```session```** :&ensp; <code>requests.sessionsSession</code>
:   Google Maps Session to use for geolocating seller
##### Function `update_vehicle`
> `def update_vehicle(vehicle, api, google_maps_session)` 

Updates vehicle's last date and duration if it exists in the database, creates a new vehicle if it doesn't.
Updates vehicle's price/seller if a change is found from the existing price/seller.
###### Args

**```vehicle```** :&ensp; <code>dict</code>
:   vehicle to be created/updated

**```api```** :&ensp; <code>[API](#class-api)</code>
:   Pscraper api, that allows retrieval/creation of marketplaces

**```google_maps_session```** :&ensp; <code>requests.sessionsSession</code>
:   Google Maps Session to use for geolocating seller

## pscraper.utils
#### Sub-modules
* [pscraper.utils.base_api](#pscraperutilsbase_api)
* [pscraper.utils.misc](#pscraperutilsmisc)

## pscraper.utils.base_api
#### Functions
##### Function `request_wrapper`
> `def request_wrapper(method, success_codes)` 
#### Classes
##### Class `BaseAPI`
> `class BaseAPI(base_url, auth)` 
##### Descendants
* [pscraper.api.API](#pscraperapi)
##### Methods
###### Method `get_full_url`
> `def get_full_url(self, url)` 
###### Method `get_request`
> `def get_request(self, url, params)` 
###### Method `patch_request`
> `def patch_request(self, url, data)` 
###### Method `post_request`
> `def post_request(self, url, data)` 

## pscraper.utils.misc
#### Functions
##### Function `get_geolocation`
> `def get_geolocation(address, session)` 

Finds latitude and longitude from a human readable address using Google Maps API.
You need to set the environment variable <code>GCP\_API\_TOKEN</code> to your Google Maps API token
###### Args

**```address```** :&ensp; <code>str</code>
:   Human readable address

**```session```** :&ensp; <code>requests.sessionsSession</code>
:   Session to use for geolocating
###### Returns

**```latitude, longitude```** :&ensp; <code>tuple</code>
:   Lat, Lng found from Google Maps API
##### Function `get_traceback`
> `def get_traceback()` 

Get formatted traceback information after exception
###### Returns
<code>text, longitude (str) Traceback text</code>
:   &nbsp; 
##### Function `measure_time`
> `def measure_time(func)` 

A decorator to call a function and track the time it takes for the function to finish execution
###### Args

**```func```**
:   Function to be decorated
##### Function `send_slack_message`
> `def send_slack_message(**kwargs)` 

Sends a message in Slack. If only one argument is provided (channel) it sends traceback information about
the most recent exception. You need to set the <code>SLACK\_API\_TOKEN</code> environment variable of your slack workspace
 API token
###### Args

**```kwargs```**
:   Keyword arguments to be used as payload for WebClient
##### Function `send_slack_report`
> `def send_slack_report(cars_et, cars_total, at_et, at_total, cm_et, cm_total, states, channel='#daily-job')` 

Post scraping report on slack channel `#daily-job` . Need to set the <code>SLACK\_API\_TOKEN</code> environment variable
to your slack workspace API token. Uses <code>utils.misc.send\_slack\_message</code>.
###### Args

**```cars_et```**
:   Time in seconds it took to scrape cars.com

**```cars_total```**
:   Number of vehicles scraped from cars.com

**```at_total```**
:   Time in seconds it took to scrape autotrader

**```at_et```**
:   Number of vehicles scraped from autotrader

**```cm_total```**
:   Time in seconds it took to scrape carmax

**```cm_et```**
:   Number of vehicles scraped from carmax

**```states```**
:   Scraped states to include in the report

**```channel```**
:   Slack channel to send the report to, default: `#daily-job` 
