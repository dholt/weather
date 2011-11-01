#!/usr/bin/env python

import os, sys, re, urllib2

class yweather:
    def __init__(self, zipcode):
        self.info = {}
        self.zipcode = zipcode
        self.data = ''

        self.getData()
        self.parseData()
    
    def getData(self):
        file = urllib2.urlopen("http://xml.weather.yahoo.com/forecastrss?p=%s&u=f" % self.zipcode)
        self.data = file.readlines()
        file.close()

    def parseData(self):
        for line in self.data:
            if line.find('<yweather:') > -1:
                type = line.split(' ')[0].split(':')[-1]
                args = []
                realArgs = {}
                for arg in line.split(' ')[1:-1]:
                    if arg != "":
                        if arg.find('=') < 0:
                            args[len(args)-1] = "%s %s" % (args[len(args)-1], arg)
                        else:
                            args.append(arg)
                for arg in args:
                    d = arg.split('=')
                    realArgs[d[0]] = d[1].strip('"')
                if type not in self.info:
                    self.info[type] = realArgs
                else:
                    self.info[type] = [self.info[type], realArgs]
        
            if line.find('<geo:') > -1:
                type = line.split('>')[0].split(':')[-1]
                self.info['location'][type] = line.split('>')[1].split('<')[0]
    
    def printData(self):
        for line in self.info:
            print line, self.info[line]

    def isValid(self):
        if len(self.info) == 0:
            return False
        return True

    def getWind(self, dir):
        # Haven't figured this out yet
        return 'UP'

    def __str__(self):
        return 'Weather information for %s' % self.zipcode

    def __getattr__(self, name):
        for type in self.info:
            if type.find(name) > -1:
                return self.info[type]

def report(zipcode):
    w = yweather(zipcode)
    if not w.isValid():
        print "Unknown zipcode %s" % zipcode
        return 1
    
    # examples
    #w.printData()
    #print w
    #print w.condition
    #print w.location['lat']

    #print w.wind['direction'],w.getWind(int(w.wind['direction']))

    print "%s @ %s" % (w.location['city'], w.condition['date'])
    print "%s %s%s\t%s|%s %s" % (w.condition['text'], w.condition['temp'], w.units['temperature'], w.forecast[0]['high'], w.forecast[0]['low'], w.forecast[0]['text'])
    print "humidity:\t%s%%" % w.atmosphere['humidity']
    print "wind:\t\t%s %s %s" % (w.wind['direction'], w.wind['speed'], w.units['distance'])
    print "visibility:\t%s %s" % (w.atmosphere['visibility'], w.units['distance'])
    print "sunrise:\t%s" % w.astronomy['sunrise']
    print "sunset:\t\t%s pm" % w.astronomy['sunset']
    for i in w.forecast[1:]:
        print "%s:\t\t%s|%s %s" % (i['day'], i['high'], i['low'], i['text'])

def temp(zipcode):
    w = yweather(zipcode)
    if not w.isValid():
        return "Unknown zipcode %s" % zipcode
    return '%s %sF' % (w.condition['text'], w.condition['temp'])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: %s [zipcode]' % sys.argv[0]
        sys.exit(1)

    sys.exit(main(sys.argv[1]))

