# PScraper Library

## Main functions
* [pscraper](#module-pscraper)
    *  [scrape](#function-scrape)
* [pscraper.utils](#module-pscraperutils)
    *  [get_master_table](#function-get_master_table)
    *  [save_master_table](#function-save_master_table)
    *  [update_duration_and_history](#function-update_duration_and_history)
    *  [notify](#function-notify)
* [pscraper.classes](#module-pscraperclasses)
    * [Seller](#class-seller)
    * [Vehicle](#class-vehicle)

# Module `pscraper`

## Functions

### Function `scrape`

> `def scrape(zip_code, search_radius, target_states)`

Scrape data about electric vehicles on [`cars.com`](https://www.cars.com) using the specified parameters

###### Args

* **`zip_code`** :&ensp;`str`:   The zip code to perform the search in
* **`search_radius`** :&ensp;`str`: The search radius for the specified zip code
* **`target_states`** :&ensp;`list`:The states to search in (i.e. ```['CA', 'NV']```)

###### Returns

**`list`**: List of scraped vehicle objects

# Module `pscraper.utils`

## Sub-modules

* [pscraper.utils.helpers](#module-pscraperutilshelpers)
* [pscraper.utils.io](#module-pscraperutilsio)
* [pscraper.utils.map](#module-pscraperutilsmap)
* [pscraper.utils.notifications](#module-pscraperutilsnotifications)
* [pscraper.utils.summary](#module-pscraperutilssummary)

# Module `pscraper.utils.helpers`

## Functions

### Function `load_yaml_file`

> `def load_yaml_file(filename)`

Loads a yaml file into a dictionary

###### Args

*  **`filename`** :&ensp;`str`: Path to yaml file

###### Returns

**`dict`**: Dictionary representation of `filename`

### Function `update_duration_and_history`

> `def update_duration_and_history(price_history, seller_history, vehicle, mastertable)`

Updates the first_date, last_date and duration of `vehicle`

###### Args

*  **`price_history`** :&ensp;`str`: Path of the price history .csv file

*  **`seller_history`** :&ensp;`str`: Path of the dealership history .csv file

*  **`vehicle`** :&ensp;`Vehicle`: Vehicle whose duration and dates will be updated

*  **`mastertable`** :&ensp;`dict`: Dictionary containing all data

###### Returns

**`Vehicle`**: The updated vehicle

# Module `pscraper.utils.io`

## Functions

### Function `get_master_table`

> `def get_master_table(mastertable_path, jsonify=False)`

Builds a dictionary by reading `mastertable_path`

###### Args

*  **`mastertable_path`** :&ensp;`str`: Path of the master table excel file
*  **`jsonify`** :&ensp;`bool`: Conditions the format of the return data. If `True` returns a dictionary representation of all the vehicle data, otherwise returns a dictionary with `listingID`s as keys and `Vehicle`s as values

###### Returns

**`dict`**:   `listingID` as keys and values of `Vehicle`s or a dictionary representation of the vehicles

### Function `save_master_table`

> `def save_master_table(mastertable, mastertable_path)`

Saves `master_table` to `master_table_loc`

###### Args

*  **`mastertable_path`** :&ensp;`str`: Path where the master table excel file will be saved
*  **`mastertable`** :&ensp;`dict`: Dictionary with `listingID` keys and `Vehicle` values   

# Module `pscraper.utils.map`

## Functions

### Function `build_map`

> `def build_map(mastertable_path, dealers_geoloc, dealer_map_loc)`

Builds an html geolocation map of current dealers

###### Args

*  **`mastertable_path`** :&ensp;`str`: Path of the master table excel file
*  **`dealers_geoloc`** :&ensp;`str`: Path of the dealer geolocation csv file
*  **`dealer_map_loc`** :&ensp;`str`: Path where the dealer map will be saved

# Module `pscraper.utils.notifications`

## Functions

### Function `notify`

> `def notify(config, message=None, is_failure=False)`

Sends a notification as detailed in configuration. Please check 
[`send_email()`](#function-send_email) and 
[`send_slack_message()`](#function-send_slack_message)
for additional information and requirements.

###### Args

*  **`config`** :&ensp;`dict`: Configuration information for sending the notification
*  **`message`** :&ensp;`str`: Message to send to receivers, defaults to None for traceback information
*  **`is_failure`** :&ensp;`bool`: If set to True receivers get traceback information for debugging

### Function `send_email`

> `def send_email(sender, receivers, message=None)`

Sends an email. If message is `None` it sends traceback information for debugging. Make sure you have
set the `SENDER_EMAIL_PASSWORD` environment variable to sender's password

###### Args

*  **`sender`** :&ensp;`str`: Sender email
*  **`receivers`** :&ensp;`list`: List of emails that will receive the message
* **`message`** :&ensp;`str`: Message to be sent, if `None` message contains debugging information

### Function `send_slack_message`

> `def send_slack_message(sender, receivers, message=None)`

Sends a message in Slack. If message is None it sends traceback information for debugging. Make sure
you have set the `SLACK_API_TOKEN` environment variable to your slack workspace API token

###### Args

*  **`sender`** :&ensp;`str`: Sender name
*  **`receivers`** :&ensp;`list`: List of channels that will receive the message
*  **`message`** :&ensp;`str`: Message to be sent, if None message contains debugging information

# Module `pscraper.utils.summary`

## Functions

### Function `summarize`

> `def summarize(mastertable_path, summary_all, summary_sold)`

Summarizes the data in the master table

###### Args

*  **`mastertable_path`** :&ensp;`str`: Location of the master_table excel file
*  **`summary_all`** :&ensp;`str`: Where to save the summary for all cars
*  **`summary_sold`** :&ensp;`str`: Where the save the summary of sold cars

# Module `pscraper.classes`

## Sub-modules

* [pscraper.classes.seller](#class-seller)
* [pscraper.classes.vehicle](#class-vehicle)

### Class `Seller`

> `class Seller(seller)`

#### Args

*  **`seller`** :&ensp;`dict`: Dictionary containing seller information

#### Attributes

*  **`name`** :&ensp;`str`: Seller name
*  **`phone_number`** :&ensp;`str`: Seller phone number
*  **`rating`** :&ensp;`str`: Seller rating and number of ratings
*  **`address`** :&ensp;`str`: Seller address

#### Instance Variables

##### Variable `json`

### Class `Vehicle`

> `class Vehicle(vehicle)`

#### Args

*  **`vehicle`**: Dictionary containing vehicle information

#### Attributes
*  **`listing_id`** :&ensp;`str` :   Unique listing ID given to the vehicle by the publisher, i.e. [`cars.com`](https://www.cars.com)
*  **`vin`** :&ensp;`str`: Vehicle Identification Number
*  **`make`** :&ensp;`str`: Vehicle make
*  **`model`** :&ensp;`str`: Vehicle model
*  **`trim`** :&ensp;`str`: Vehicle trim
*  **`body_style`** :&ensp;`str`: Vehicle body style
*  **`mileage`** :&ensp;`str`: Vehicle mileage
*  **`year`** :&ensp;`str`: Vehicle year
*  **`seller`** :&ensp;`Seller`: Vehicle seller
*  **`first_date`** :&ensp;`str`: The first date the vehicle was available for purchase
*  **`last_date`** :&ensp;`str`: The last date the vehicle was available for purchase
*  **`duration`** :&ensp;`int`: The duration in days the vehicle was available for

#### Instance variables

##### Variable `json`
