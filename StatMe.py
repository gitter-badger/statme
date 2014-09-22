#!/usr/bin/env python

__author__ = 'noahlutz'

import tweepy
import sys
import MySQLdb
# import xhtml2pdf

states = {
    'AK': 'ALASKA',
    'AL': 'ALABAMA',
    'AR': 'ARKANSAS',
    'AS': 'AMERICAN SAMOA',
    'AZ': 'ARIZONA',
    'CA': 'CALIFORNIA',
    'CO': 'COLORADO',
    'CT': 'CONNECTICUT',
    'DC': 'DISTRICT OF COLUMBIA',
    'DE': 'DELAWARE',
    'FL': 'FLORIDA',
    'GA': 'GEORGIA',
    'GU': 'GUAM',
    'HI': 'HAWAII',
    'IA': 'IOWA',
    'ID': 'IDAHO',
    'IL': 'ILLINOIS',
    'IN': 'INDIANA',
    'KS': 'KANSAS',
    'KY': 'KENTUCKY',
    'LA': 'LOUISIANA',
    'MA': 'MASSACHUSETTS',
    'MD': 'MARYLAND',
    'ME': 'MAINE',
    'MI': 'MICHIGAN',
    'MN': 'MINNESOTA',
    'MO': 'MISSOURI',
    'MP': 'NORTHERN MARIANA ISLANDS',
    'MS': 'MISSISSIPPI',
    'MT': 'MONTANA',
    'NA': 'NATIONAL',
    'NC': 'NORTH CAROLINA',
    'ND': 'NORTH DAKOTA',
    'NE': 'NEBRASKA',
    'NH': 'NEW HAMPSHIRE',
    'NJ': 'NEW JERSEY',
    'NM': 'NEW MEXICO',
    'NV': 'NEVADA',
    'NY': 'NEW YORK',
    'OH': 'OHIO',
    'OK': 'OKLAHOMA',
    'OR': 'OREGON',
    'PA': 'PENNSYLVANIA',
    'PR': 'PUERTO RICO',
    'RI': 'RHODE ISLAND',
    'SC': 'SOUTH CAROLINA',
    'SD': 'SOUTH DAKOTA',
    'TN': 'TENNESSEE',
    'TX': 'TEXAS',
    'UT': 'UTAH',
    'VA': 'VIRGINIA',
    'VI': 'VIRGIN ISLANDS',
    'VT': 'VERMONT',
    'WA': 'WASHINGTON',
    'WI': 'WISCONSIN',
    'WV': 'WEST VIRGINIA',
    'WY': 'WYOMING'
}

consumer_key = 'TWPsNBca4joN3o3bF5GP8X52J'
consumer_secret = 'k1O9YO267OsDedaErkhR1MTIxJS9FjgIPCnhtcsM0o4IVEnQk0'
access_key = '2199777559-0cnOjV5oBtGl57FIWrtpNI5THdrRjyS9f9O9pQV'
access_secret = 'hSs76D1kxjepVUuXoy0WinWisUyYdXifEbqNkd7IKCJZ2'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


class DBConnector():
    def __init__(self, host, year):
        self.connection = MySQLdb.connect(host=host, port=3306, user='root', passwd='', db='mysql')
        self.year = str(year)

    def findcrimerate(self, city, state):
        cur = self.connection.cursor()
        cur.execute('SELECT crime_activity FROM CrimeData.' + self.year + ' WHERE state = ' + '\'' + states[state] + '\'' + ' AND city = ' + '\'' + city + '\'')
        print "Crime: %s" % cur.fetchone()
        cur.close()


class HashtagListener(tweepy.StreamListener):
    def __init__(self, dbconnector):
        super(HashtagListener, self).__init__()
        self.location = None
        self.mysqldb = dbconnector

    def on_status(self, status):
        for hashtag in status.entities['hashtags']:
            if hashtag['text'] == 'statme':
                print "Someone Tweeted #statme"
                print status.user.screen_name
                try:
                    self.location = status.place.full_name.split(',')
                except:
                    print 'No Location Data. Retry with location services enabled.'
                    return
                # print self.location[0]
                # print self.location[1].strip(' ')
                self.mysqldb.findcrimerate(self.location[0], self.location[1].strip(' '))
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered Error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True


def main():
    mysql_db = DBConnector('localhost', 2012)
    listen = HashtagListener(mysql_db)
    stream = tweepy.Stream(auth, listen)

    #starts listening for tweets @ authenticated user
    print 'Stream Started...'
    stream.userstream()


if __name__ == '__main__':
    main()