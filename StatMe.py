#!/usr/bin/env python

__author__ = 'noahlutz'

import sys, traceback
import tweepy
import sys
import MySQLdb
from PIL import Image, ImageFont, ImageDraw

#dict of states for easy conversion
states = {'AK': 'ALASKA', 'AL': 'ALABAMA', 'AR': 'ARKANSAS', 'AS': 'AMERICAN SAMOA', 'AZ': 'ARIZONA', 'CA': 'CALIFORNIA',
          'CO': 'COLORADO', 'CT': 'CONNECTICUT', 'DC': 'DISTRICT OF COLUMBIA', 'DE': 'DELAWARE', 'FL': 'FLORIDA',
          'GA': 'GEORGIA', 'GU': 'GUAM', 'HI': 'HAWAII', 'IA': 'IOWA', 'ID': 'IDAHO', 'IL': 'ILLINOIS', 'IN': 'INDIANA',
          'KS': 'KANSAS', 'KY': 'KENTUCKY', 'LA': 'LOUISIANA', 'MA': 'MASSACHUSETTS', 'MD': 'MARYLAND', 'ME': 'MAINE',
          'MI': 'MICHIGAN', 'MN': 'MINNESOTA', 'MO': 'MISSOURI', 'MP': 'NORTHERN MARIANA ISLANDS', 'MS': 'MISSISSIPPI',
          'MT': 'MONTANA', 'NA': 'NATIONAL', 'NC': 'NORTH CAROLINA', 'ND': 'NORTH DAKOTA', 'NE': 'NEBRASKA',
          'NH': 'NEW HAMPSHIRE', 'NJ': 'NEW JERSEY', 'NM': 'NEW MEXICO', 'NV': 'NEVADA', 'NY': 'NEW YORK',
          'OH': 'OHIO', 'OK': 'OKLAHOMA', 'OR': 'OREGON', 'PA': 'PENNSYLVANIA', 'PR': 'PUERTO RICO','RI': 'RHODE ISLAND',
          'SC': 'SOUTH CAROLINA', 'SD': 'SOUTH DAKOTA', 'TN': 'TENNESSEE', 'TX': 'TEXAS', 'UT': 'UTAH', 'VA': 'VIRGINIA',
          'VI': 'VIRGIN ISLANDS', 'VT': 'VERMONT', 'WA': 'WASHINGTON', 'WI': 'WISCONSIN', 'WV': 'WEST VIRGINIA',
          'WY': 'WYOMING'}

NO_LOCATION = ' No Location Data. Please turn location services on in your settings.'
UNEXPECTED_ERROR = ' Sorry, we encountered and unexpected error. Please tweet @NoahL98 with the location you are trying ' \
                   'to tweet from.'


#twitter keys
consumer_key = 'TWPsNBca4joN3o3bF5GP8X52J'
consumer_secret = 'k1O9YO267OsDedaErkhR1MTIxJS9FjgIPCnhtcsM0o4IVEnQk0'
access_key = '2199777559-0cnOjV5oBtGl57FIWrtpNI5THdrRjyS9f9O9pQV'
access_secret = 'hSs76D1kxjepVUuXoy0WinWisUyYdXifEbqNkd7IKCJZ2'

#tweepy authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


class DBConnector():
    def __init__(self, host, year):
        #connect to specified database
        self.connection = MySQLdb.connect(host=host, port=3306, user='root', passwd='', db='mysql')
        self.year = str(year)

    #gets crime score for specified city
    def getcrimescore(self, city, state):
        cur = self.connection.cursor()
        #try to get crime score. return -1 if fail

        #gets num of violent crimes
        cur.execute('SELECT violent_crime FROM CrimeData.{year} WHERE state = \'{state}\' AND city = \'{city}\''.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state, city=MySQLdb.escape_string(city)))
        total_violentcrime = int('%s' % cur.fetchone()) + 0.0

        #gets num of property crimes
        cur.execute('SELECT property_crime FROM CrimeData.{year} WHERE state = \'{state}\' AND city = \'{city}\''.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state, city=MySQLdb.escape_string(city)))
        total_propertycrime = int('%s' % cur.fetchone()) + 0.0

        #gets population
        cur.execute('SELECT population FROM CrimeData.{year} WHERE state = \'{state}\' AND city = \'{city}\''.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state, city=MySQLdb.escape_string(city)))
        population = int('%s' % cur.fetchone()) + 0.0

        #returns the crime score
        return (total_violentcrime + total_propertycrime)/population


    #NEEDS WORK
    def statepercentile(self, state):
        above = []
        violent_crime = 0.0
        property_crime = 0.0
        population = 0.0
        cur = self.connection.cursor()

        cur.execute('SELECT violent_crime FROM CrimeData.{year} WHERE state = \'{state}\' '.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state))
        for violent in cur.fetchall():
            violent_crime += int('%s' % violent)

        cur.execute('SELECT property_crime FROM CrimeData.{year} WHERE state = \'{state}\' '.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state))
        for property in cur.fetchall():
            property_crime += int('%s' % property)

        cur.execute('SELECT population FROM CrimeData.{year} WHERE state = \'{state}\' '.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state))
        for pop in cur.fetchall():
            population += int('%s' % pop)

        current_state_score = (property_crime + violent_crime)/population

        print current_state_score

    #gets the city's percentile based on other cities/towns in state
    def citypercentile(self, city, state):
        above = []
        cur = self.connection.cursor()

        #gets the current cities crime score
        crimescore = self.getcrimescore(city, state)

        #gets all cities in current state
        cur.execute('SELECT city FROM CrimeData.{year} WHERE state = \'{state}\' '.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state))
        total_cities = cur.fetchall()

        #if crime score is higher than current city, add to list
        for ct in total_cities:
            currentcity = '%s' % ct
            if self.getcrimescore(currentcity, state) > crimescore:
                above.append(currentcity)

        #return current city percentile
        return round(((len(above)+0.0)/(len(total_cities)+0.0))*100)

    def victimization(self, city, state):
        cur = self.connection.cursor()

        #gets victimization number from database
        cur.execute('SELECT victimization FROM CrimeData.{year} WHERE state = \'{state}\' AND city = \'{city}\''.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state, city=MySQLdb.escape_string(city)))

        return '%s' % cur.fetchone()

    def violentcrime(self, city, state):
        cur = self.connection.cursor()

        #gets violent crime number from database
        cur.execute('SELECT violent_crimes_per FROM CrimeData.{year} WHERE state = \'{state}\' AND city = \'{city}\''.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state, city=MySQLdb.escape_string(city)))

        return '%s' % cur.fetchone()

    def propertycrime(self, city, state):
        cur = self.connection.cursor()

        #gets property crime number from database
        cur.execute('SELECT property_crimes_per FROM CrimeData.{year} WHERE state = \'{state}\' AND city = \'{city}\''.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state, city=MySQLdb.escape_string(city)))

        return '%s' % cur.fetchone()

    def crimerate(self, city, state):
        cur = self.connection.cursor()

        #gets crime rate number from database
        cur.execute('SELECT crime_activity FROM CrimeData.{year} WHERE state = \'{state}\' AND city = \'{city}\''.format
                    (year=MySQLdb.escape_string(str(self.year)), state=state, city=MySQLdb.escape_string(city)))

        return '%s' % cur.fetchone()



class HashtagListener(tweepy.StreamListener):
    def __init__(self, dbconnector, api, imagelocation):
        super(HashtagListener, self).__init__()
        self.location = None
        self.mysqldb = dbconnector
        self.api = api
        self.imagelocation = imagelocation
        self.font = 'font/HelveNeuUltLig.ttf'

    def on_status(self, status):
        for hashtag in status.entities['hashtags']:
            if hashtag['text'] == 'statme':
                print "Someone Tweeted #statme"
                print status.user.screen_name

                #try to get location. if fail, no location sent with tweet
                try:
                    self.location = status.place.full_name.split(',')
                except:
                    self.replytext(NO_LOCATION, status.user.screen_name)
                    return

                #get city and state from tweet
                city = self.location[0]
                state = states[self.location[1].strip(' ')]


                try:
                    #get info for image generation
                    crimerate = self.mysqldb.crimerate(city, state)
                    citypercentile = int(self.mysqldb.citypercentile(city, state))
                    victimization = self.mysqldb.victimization(city, state)
                    violentcrime = self.mysqldb.violentcrime(city, state)
                    propertycrime = self.mysqldb.propertycrime(city, state)

                    #generates image and replys to user
                    self.generateimage(status, crimerate, victimization, citypercentile, violentcrime, propertycrime)
                    self.reply(crimerate, status.user.screen_name)
                except:
                    #if fail send error to user and print error
                    self.replytext(UNEXPECTED_ERROR, status.user.screen_name)
                    traceback.print_exc(file=sys.stdout)
                    return
                print 'Sent Reply'

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered Error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True

    def reply(self, message, user):
        self.api.update_with_media('Images/statme_test.png', status='@' + user + message)
        print message

    def replytext(self, message, user):
        # self.api.update_status('@' + user + message)
        print message

    def generateimage(self, status, crimerate, victimization, citypercentile, violentcrime, propertycrime):
        #open template
        img = Image.open(self.imagelocation)
        img.load()

        #draw all info on image
        self.drawimage(166, status.place.full_name, img, location=[12, 600])
        self.drawimage(200, crimerate, img, location=[5, 1050])
        self.drawimage(100, '1 in ' + victimization, img,  location=[20, 1450])
        self.drawimage(120, str(citypercentile) + '%', img, location=[-370, 1010])
        self.drawimage(120, str(violentcrime), img, location=[-385, 1520])
        self.drawimage(120, str(propertycrime), img, location=[430, 1520])

        #save image
        img.save('Images/statme_test.png', 'PNG')

    def drawimage(self, fontsize, text, image, location):
        #open image for drawing
        draw = ImageDraw.Draw(image)

        #load font
        font = ImageFont.truetype(self.font, fontsize)

        #calculate center
        fontwidth, fontheight = font.getsize(text)
        x = (image.size[0]-fontwidth)/2

        #draw text on image at specified location(location[0] is offset for x coord)
        draw.text((x + location[0], location[1]), text, (255, 255, 255), font=font)


def main():
    #define image template
    imagelocation = 'Images/statme_template.png'

    #define database
    mysql_db = DBConnector('localhost', 2012)

    #define twitter stream
    listen = HashtagListener(mysql_db, api, imagelocation)
    stream = tweepy.Stream(auth, listen)

    #starts listening for tweets @ the authenticated user
    print 'Stream Started...'
    stream.userstream()


if __name__ == '__main__':
    main()