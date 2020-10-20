# vehicleinfo.org
> The Vehicle Information Project aims to make vehicle information public and accessible for anyone who needs it through a public API and web interface.

![Open Source Love](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-pink.svg)

The purpose of this tool is to be a public resource for anyone interested in accessing a specific vehicle's information. The ongoing mission is to continually write robust scripts in order to add support for more vehicles and gather more data about the existing vehicles in the database.

This project is intended to be open source and public, so any and all contributions are always welcome!

![The Vehicle Information Project](/static/img/scrot.jpg)


## Release History

| Version 	| Description of Changes 	|
|-	|-	|
| 3.1.2 	| - Migrated deployment and database from Heroku and ClearDB to AWS Elastic Beanstalk and AWS RDS. This isn't a functional update but worth noting in the change log as certain configurations were changed in order to operate on AWS standards instead of Heroku.<br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/26) 	|
| 3.1.1 	| - Updated a lot of the web services stuff. Making updates is much easier now and is well documented, with descriptions for everything. See the microservices folder for the details.<br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/25) 	|
| 3.1.0 	| - When getting a report through the web interface, recalls and consumer complaints are no longer mandatory. Two checkboxes have been added to the form, and are selected by default to include recalls and consumer complaints. If the client doesn't want either of these pieces of information, they can choose to omit them.<br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/24) 	|
| 3.0.0 	| - New feature addition! Vehicleinfo.org gets a VIN decoder for the web interface. Simply input your vehicle's VIN number and be presented with various pieces of information about the automobile that was available. Handy tool to verify that a VIN matches the actual vehicle!<br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/23) 	|
| 2.3.1 	| - Add's image toggling on the report interface for the available styles. If there is a car that came as a sedan and coupe, you can toggle images for both styles.<br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/22) 	|
| 04/11/2020 	| - Not a release update, but I refactored the main server code between three files. See server.py, config.py, and api_utils.py for the application business logic breakdown. Also made some updates to the API and Change Log page because I had made some mistakes with bootstrap and flexbox in the styling.<br>- Also in 2.2.2 I fixed the tall screen issue by expanding the last element on the page. I didn't like the way that looked after seeing it on a device, so I now expand the footer instead of the last element. See /static/js/stickyfooter.js for the updates. 	|
| 2.3.0 	| - Add's caching to the routes on the website for 5 minutes at a time, that way if someone is on the site, they get a seamless experience when going to pages they've already visited. Utilized Flask Caching, and did some handling to bypass caching on POST requests in order to avoid errors.<br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/18) 	|
| 2.2.2 	| - Fixed an issue where on tall screens, the footer would float with a bunch of whitespace. Spent some time ironing out CSS and JS issues to develop some code that updates the last section on a page if the viewport exceeds the size of real content.<br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/17) 	|
| 2.2.1 	| - The data tables on the report now have pages! Instead of getting a list of 100 items, you now see five at a time. <br>- Also fixed a server issue while I was in there. The DB provider [clearDB], has a non-adjustable server timeout configuration. To mitigate dropping connections, we now ping the server between requests. The pull request below has more details, including the link to the stackoverflow post I used.<br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/14) 	|
| 2.2.0 	| - Resolves issue where the search form made it difficult to get a report on cars where the name is ambiguous, or not well defined, such as ‘BMW 3-series’ or ‘Lexus ES’. Because of this, the web report interface’s search form was swapped out for a select option.<br>- Utilized the fetch() API to grab the updated lists, and they are asynchronously rendered as you change your selections.  <br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/13) 	|
| 2.1.0 	| - Trailing slash fix for API. Fixes inconsistent HTTP request paths.<br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/12) 	|
| 2.0.0 	| - Designed a whole new UI<br>- Significant improvements warranted skipping versions b/w 1.0.1 & 2 <br>- [See pull request](https://github.com/zshafiqu/vehicleinfo.org/pull/2) 	|
| 1.0.0 	| - Only slightly a working web app 	|                                                                                                                                             |

## About Stuff
See 'requirements.txt' for application dependencies

Zain Shafique – [LinkedIn](https://www.linkedin.com/in/zain-shafique/)

Distributed under the MIT license. See ``LICENSE`` for more information.


## Contributing

1. Fork it (<https://github.com/zshafiqu/vehicleinfo.org/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
