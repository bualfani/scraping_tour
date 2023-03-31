import request
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3


url = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect('data.db')


class Event:
    def scrape(self, url):
        '''scrape the page sorce from url'''

        response = request.get(url)
        source_text = response.text
        return source_text

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
        value = extractor.extract(source)['tours']


def send_email(message):
    host = 'smtp.gmail.com'
    port = 465
    username = 'your_email'
    password = os.getenv("Password")
    receiver = "your_email"
    my_context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=my_context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

def store(extrated):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    Band, City, Date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE Band=? City=? Date=?", (Band, City, Date))
    rows = cursor.fetchall()
    return rows

if __name__ == "__main__":
    while True:
        scraped = scrape(url)
        extracted = extract(scraped)


        if extracted != 'No upcoming tour':
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="New Event was found")
        # check for new event every two sec.
        time.sleep(2)