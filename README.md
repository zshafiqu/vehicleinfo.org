# vehicleinfo.org
> The Vehicle Information Project aims to make vehicle information public and accessible for anyone who needs it through a public API and web interface.

![Open Source Love](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-pink.svg)

The purpose of this tool is to be a public resource for anyone interested in accessing a specific vehicle's information. The ongoing mission is to continually write robust scripts in order to add support for more vehicles and gather more data about the existing vehicles in the database.

This project is intended to be open source and public, so any and all contributions are always welcome!

![The Vehicle Information Project](/static/img/scrot.jpg)


## Release History
* 2.3.0
    * Add's caching to the routes on the website for 5 minutes at a time, that way if someone is on the site, they get a seamless experience when going to pages they've already visited. Utilized Flask Caching, and did some handling to bypass caching on POST requests in order to avoid errors.
    * [(See pull request)](https://github.com/zshafiqu/vehicleinfo.org/pull/18)
* 2.2.2
    * Fixed an issue where on tall screens, the footer would float with a bunch of whitespace. Spent some time ironing out CSS and JS issues to develop some code that updates the last section on a page if the viewport exceeds the size of real content.
    * [(See pull request)](https://github.com/zshafiqu/vehicleinfo.org/pull/17)
* 2.2.1
    * The data tables on the report now have pages! Instead of getting a list of 100 items, you now see five at a time.  
    * Also fixed a server issue while I was in there. The DB provider [clearDB], has a non-adjustable server timeout configuration. To mitigate dropping connections, we now ping the server between requests. The pull request below has more details, including the link to the stackoverflow post I used.
    * [(See pull request)](https://github.com/zshafiqu/vehicleinfo.org/pull/14)
* 2.2.0
    * Resolves issue where the search form made it difficult to get a report on cars where the name is ambiguous, or not well defined, such as ‘BMW 3-series’ or ‘Lexus ES’. Because of this, the web report interface’s search form was swapped out for a select option.
    * Utilized the fetch() API to grab the updated lists, and they are asynchronously rendered as you change your selections.  
    * [(See pull request)](https://github.com/zshafiqu/vehicleinfo.org/pull/13)
* 2.1.0
    * Trailing slash fix for API. Fixes inconsistent HTTP request paths. [(See pull request)](https://github.com/zshafiqu/vehicleinfo.org/pull/12)
* 2.0.0
    * Designed a whole new UI [(see pull request)](https://github.com/zshafiqu/vehicleinfo.org/pull/2)
    * Significant improvements warranted skipping versions b/w 1.0.1 & 2
* 1.0.0
    * Only slightly a working web app

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
