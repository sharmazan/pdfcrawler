# PDF Crawler
This project aims to search through uploaded PDF files for URLs and save these URLs to the database. 

## How to use
### Upload PDF file
On the main page you could upload any PDF file:
![Main page](https://i.snipboard.io/hRrkgn.jpg)

After file handling, it will redirect you to another page and show "Success" or "Error" message. 
The main reason for an error is a different file format - the program could handle only PDF files. 

### Other URLs
**/files/** returns a set of all the documents that were uploaded: ids, names, and number of URLs that were found for each document, in JSON format. 
![Files output](https://i.snipboard.io/I2Q7FC.jpg)

**/files/<file_id>** returns a set of URLs for a specific document in JSON format.
![Specific file output](https://snipboard.io/Yphr1m.jpg)

**/urls/** returns a set of all URLs found, including the number of documents that contained the URL, in JSON format.
![URLs output](https://snipboard.io/fRqz87.jpg)

## Installation
To install the PDF Crawler application make sure that you have python version 2.7 installed.

### Get source code
`git clone git@github.com:sharmazan/pdfcrawler.git && cd pdfcrawler`

### Prepare virtualenv
`virtualenv crawler && source crawler/bin/activate`

### Install dependencies
`pip install -r requirements.txt`

### Prepare the database
`python manage.py migrate`

### Run server
`python manage.py runserver`

Now you could try http://127.0.0.1:8000 to check how it works. 
