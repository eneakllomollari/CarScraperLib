# Vehicle Scraping Project

The goal of the project is to understand how the supply-side of vehicle
availability affects the electric vehicle market. It tracks all vehicles
that are available for sale at dealerships across a number of specified
regions using a web scraper that takes advantage of publicly available data.

## The following is a guide to scrape_and_get_cars_list and store the data for future use

- Guide to the website where you enter three filter terms, a ZIP code,
  leave this as a flexible variable as we will be searching across multiple
  ZIP codes, and the search radius. Electric vehicle search is built-in the
  scraper

- The data should be parsed directly in the following form based on the
  data grab:
  `VIN` `Make` `Model` `Trim` `Body Style` `Year`
  `Price` `Mileage` `Dealer Name` `Dealer Address`
  `Listing Href`

- The main data structure is a dictionary with the VIN being the key.
  To keep track of the availability of a car over time we keep track
  of when the `VIN` first shows up and when it leaves. Therefore,
  two more columns should be added to the above: `firstAvailableDate`
  and `lastAvailableDate` and `lastAvailableDate`.
