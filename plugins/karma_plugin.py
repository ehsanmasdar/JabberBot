#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  karma_plugin.py

#  Initial Copyright © 2013 Rephlexie <rephlex@plutocr.at>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.


def karma_remove_html(text):
  nobold = text.replace('<b>', '').replace('</b>', '')
	nobreaks = nobold.replace('<br>', ' ')
	noescape = nobreaks.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
	return noescape

def karma_search(query):
	try:
		req = urllib2.urlopen('http://www.karmagaming.org/index.php/kunena/recent-topics' % urllib2.quote(query.encode('utf8')))
	except urllib2.HTTPError, e:
		reply(type,source,str(e))
		return
	answ=json.load(req)
	results=answ['responseData']['results']
	if results:
		titleNoFormatting=results[0]['titleNoFormatting']
		content=results[0]['content']
		url=results[0]['unescapedUrl']
		return karma_remove_html(titleNoFormatting+u'\n'+content+u'\n'+url)
	elif answ['responseDetails']:
		return answ['responseDetails']
	else:
		return


def handler_karma_karma(type, source, parameters):
	results = karma_search(parameters)
	if results:
		reply(type, source, results)
	else:
		reply(type, source, u'nothing found')

try:
	import json
	register_command_handler(handler_karma_karma, 'karma', ['fun','all'], 0, 'search in karma.', 'karma <query>', ['search something'])
except ImportError:
	try:
		import simplejson as json
		register_command_handler(handler_karma_karma, 'karma', ['fun','all'], 0, 'search in karma.', 'karma <query>', ['search something'])
	except:
		print '====================================================\nYou need Python 2.6.x or simple_json package installed to use karma_plugin.py!!!\n====================================================\n'

