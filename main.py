import praw
import urllib
import rlogin
from time import gmtime, strftime
from xml.dom import minidom
from operator import itemgetter,attrgetter

# Gather user info from rlogin
userdata = rlogin.userinfo()

# API Data
API_KEY = userdata['api_key']
API_URL = 'http://api.sportsdatallc.org/mlb-t3/standings/2013.xml?api_key=' + API_KEY 
XML_NS = 'http://feed.elasticstats.com/schema/mlb/standings-v3.0.xsd'

url = API_URL
ns = XML_NS
dom = minidom.parse(urllib.urlopen(url))
	
# create an array for our standings
standings = []

# helper function to help calculate the win percentage
def percentage(part, whole):
	if whole == 0:
		return 0
	return 100 * float(part)/float(whole)

# this pulls the standings and formats them
def createStandings():
	s = []
	# loop through the xml results appending each row
	for node in dom.getElementsByTagNameNS(ns, 'team'):
		s.append({
				'teamname': node.getAttribute('name'),
				'division': node.parentNode.parentNode.getAttribute('id') + node.parentNode.getAttribute('id'),
				'wins': node.getAttribute('win'),
				'losses': node.getAttribute('loss'),
				'gamesback': node.getAttribute('games_back'),
				'streak': node.getAttribute('streak'),
				'l10': node.getAttribute('last_10_won') + '-' + node.getAttribute('last_10_lost'),
				'percentage': percentage(int(node.getAttribute('win')),int(node.getAttribute('win'))+int(node.getAttribute('loss')))
			})

	# sort the standings
	n = sorted(s, key=lambda k: k['division'])
	standings = sorted(n, key=lambda q: q['percentage'], reverse=True)

	return standings
	
def createTable():
	
	#create our standings
	standings = createStandings()

	# i suck at sorting stuff so i setup the header rows ahead of time and i'm sorting them below
	# I know this is ugly...
	tablerows = []
	headerrows = []
	alcrows = []
	alcrows.append('|' + '**ALC**' + '|')
	alerows = []
	alerows.append('|' + '**ALE**' + '|')
	alwrows = []
	alwrows.append('|' + '**ALW**' + '|')
	nlcrows = []
	nlcrows.append('|' + '**NLC**' + '|')
	nlerows = []
	nlerows.append('|' + '**NLE**' + '|')
	nlwrows = []
	nlwrows.append('|' + '**NLW**' + '|')

	# Setup the Reddit Table
	headerrows.append(u'**Standings**\n\n| Team | W | L | GB | S | L10 |\n|:-|:-:|:-:|:-:|:-:|:-:|')

	# Print Each Team's Information
	for i in range(len(standings)):
		# sort by league and division
		if standings[i]['division'] == 'ALC':
			alcrows.append('|' + standings[i]['teamname'] + '|' + standings[i]['wins'] + '|' + standings[i]['losses'] + '|' + standings[i]['gamesback'] + '|' + standings[i]['streak'] + '|' + standings[i]['l10'] + '|')
		elif  standings[i]['division'] == 'ALE':
			alerows.append('|' + standings[i]['teamname'] + '|' + standings[i]['wins'] + '|' + standings[i]['losses'] + '|' + standings[i]['gamesback'] + '|' + standings[i]['streak'] + '|' + standings[i]['l10'] + '|')
		elif  standings[i]['division'] == 'ALW':
			alwrows.append('|' + standings[i]['teamname'] + '|' + standings[i]['wins'] + '|' + standings[i]['losses'] + '|' + standings[i]['gamesback'] + '|' + standings[i]['streak'] + '|' + standings[i]['l10'] + '|')
		elif  standings[i]['division'] == 'NLC':
			nlcrows.append('|' + standings[i]['teamname'] + '|' + standings[i]['wins'] + '|' + standings[i]['losses'] + '|' + standings[i]['gamesback'] + '|' + standings[i]['streak'] + '|' + standings[i]['l10'] + '|')
		elif  standings[i]['division'] == 'NLE':
			nlerows.append('|' + standings[i]['teamname'] + '|' + standings[i]['wins'] + '|' + standings[i]['losses'] + '|' + standings[i]['gamesback'] + '|' + standings[i]['streak'] + '|' + standings[i]['l10'] + '|')
		elif  standings[i]['division'] == 'NLW':
			nlwrows.append('|' + standings[i]['teamname'] + '|' + standings[i]['wins'] + '|' + standings[i]['losses'] + '|' + standings[i]['gamesback'] + '|' + standings[i]['streak'] + '|' + standings[i]['l10'] + '|')
	
	# combine all of our lists
	tablerows = headerrows + alcrows + alerows + alwrows + nlcrows + nlerows + nlwrows
	
	# add the footer
	dayupdated = strftime("%a, %d %b %Y %X +0000", gmtime())
	tablerows.append(u'These standings were updated by [u/soxmod](http://www.reddit.com/u/soxmod) a reddit bot. Standings are updated nightly. Standings were last updated on ' + dayupdated)
	
	return tablerows

# store the standings in a string from the previous function
standingsTable = createTable()


### BEGIN REDDIT UPDATE SECION ###

# Reddit user_agent 
user_agent = (userdata['useragent'])

r = praw.Reddit(user_agent=user_agent)

# login
r.login(userdata['username'],userdata['password'])

# Get subreddit settings
settings = r.get_subreddit(userdata['subreddit']).get_settings()

# store the old description
description = settings['description']

# Trim off the old standings
sep = '**Standings**'
trimmed = description.split(sep, 1)[0]

# concatenate the new standings to the description
newdescription = trimmed + '\n'.join(standingsTable)

# encode to utf-8 for reddit tables to format properly
desc = newdescription.encode(encoding='UTF-8',errors='strict')

# Update Description
r.get_subreddit(userdata['subreddit']).update_settings(description=desc)
