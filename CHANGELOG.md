# Changelog

#### v1.2.1
* Add error reporting in <code>get_cars_com_response</code>

### v1.2.0
* Update `README.md` with documentation on the project
* Rename `post_daily_slack_report` to `send_slack_report` and move to `pscraper.utils.misc`

### v1.1.0
* Post every vehicle's dynamic data into a separate table using the `pscraper/history` endpoint 
* Use requests.session.Session() for persistent connections
* Add `psraper/history/` endpoint for history table in API
* Add logging and update error handling in update table
    - All logs are date-stamped under `logs/` directory
* Update slack daily report format
* Use seller's address to identify it as unique when searching

#### v1.0.4
* Report api errors from base api decorator
* Check google maps api `status_code` before accessing the results
* Don't post message on slack after scraping is complete, let the scraping-tool handle it 
* Update slack report format, add `states`

#### v1.0.3
* Add validation for target_states
* Add validation for radius in cars.com
* Modify cars.com search query to have local only dealers

#### v1.0.2
* Add error handling when seller geolocation can't be found by Google Maps API

#### v1.0.1
* Add filter to skip vehicles whose seller does not have a phone number

### v1.0.0
* Initial Release
