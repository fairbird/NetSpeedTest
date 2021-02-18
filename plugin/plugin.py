#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from enigma import eConsoleAppContainer
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Pixmap import Pixmap
from Components.Label import Label
from Tools.Directories import resolveFilename, SCOPE_PLUGINS

PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, 'SystemPlugins/NetSpeedTest')


class NetSpeedTestScreen(Screen):
    skin = '  <screen name="NetSpeedTestScreen"  backgroundColor="#380038" position="center,center" size="900,520" title="Net Speed Test" >\n                <ePixmap position="0,0"  size="900,520" pixmap="%s/SystemPlugins/NetSpeedTest/netspeed.jpg"     zPosition="1" transparent="1" alphatest="blend" />\n                <widget name="data" position="155,59" zPosition="4" size="610,243" font="Regular;25" foregroundColor="#76addc" transparent="1" halign="left" valign="top" />\n                <widget name="ping" position="190,29" zPosition="4" size="157,40" font="Regular;25" foregroundColor="white" transparent="1" halign="left" valign="top" />\n                <widget name="host" position="673,453" zPosition="4" size="196,56" font="Regular;25" foregroundColor="white" transparent="1" halign="left" valign="top" />\n                <widget name="ip" position="63,452" zPosition="4" size="204,53" font="Regular;25" foregroundColor="white" transparent="1" halign="left" valign="top" />\n                <widget name="download" position="398,30" zPosition="4" size="156,53" font="Regular;25" foregroundColor="white" transparent="1" halign="left" valign="top" />\n                <widget name="upload" position="597,30" zPosition="4" size="161,53" font="Regular;25" foregroundColor="white" transparent="1" halign="left" valign="top" />\n                                                       \n\t\t</screen>' % resolveFilename(SCOPE_PLUGINS)

    def __init__(self, session):
        Screen.__init__(self, session)
        self.color = '#800080'
        self['data'] = Label('Testing net speed, please wait ...')
        self['ping'] = Label(' ')
        self['host'] = Label(' ')
        self['ip'] = Label(' ')
        self['download'] = Label(' ')
        self['upload'] = Label(' ')
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': self.exit,
         'green': self.testagain}, -1)
        cmd = 'python ' + PLUGIN_PATH + '/speedtest.pyo'
        self.finished = False
        self.data = ''
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.action)
        self.container.dataAvail.append(self.dataAvail)
        self.container.execute(cmd)

    def testagain(self):
        self.container.appClosed.append(self.action)
        self.container.dataAvail.append(self.dataAvail)
        if self.finished == False:
            return
        self['data'].setText('Testing net speed ...')
        self['ping'].setText('')
        self['host'].setText('')
        self['ip'].setText('')
        self['download'].setText('')
        self['upload'].setText('')
        cmd = 'python ' + PLUGIN_PATH + '/lib/speedtest.pyo'
        self.container.execute(cmd)

    def action(self, retval):
        print('retval', retval)
        print('finished test')
        self.finished = True
        self.container_appClosed = None
        self.container_dataAvail = None
        self.container.appClosed.remove(self.action)
        self.container.dataAvail.remove(self.dataAvail)

    def dataAvail(self, rstr):
        if rstr:
            self.data = self.data + rstr
            parts = rstr.split('\n')
            for part in parts:
                if 'Hosted by' in part:
                    try:
                        host = part.split('Hosted by')[1].split('[')[0].strip()
                    except:
                        host = ''

                    self['host'].setText(str(host))
                if 'Testing from' in part:
                    ip = part.split('Testing from')[1].split(')')[0].replace('(', '').strip()
                    self['ip'].setText(str(ip))

            if 'Ping' in rstr:
                try:
                    ping = rstr.split('Ping')[1].split('\n')[0].strip()
                except:
                    ping = ''

                self['ping'].setText(str(ping))
            if 'Download:' in rstr:
                try:
                    download = rstr.split(':')[1].split('\n')[0].strip()
                except:
                    download = ''

                self['download'].setText(str(download))
                self.data = ''
                self.data = 'Testing upload speed....'
            if 'Upload:' in rstr:
                try:
                    upload = rstr.split(':')[1].split('\n')[0].strip()
                except:
                    upload = ''

                self['upload'].setText(str(upload))
                self['data'].setText(' Test completed, to test again press the green button.')
                return
            self['data'].setText(self.data)

    def exit(self):
        self.container = None
        self.close()
        return

    def updateTitle(self):
        self.newtitle = 'Net speed test'
        self.setTitle(self.newtitle)


def netspeedMain(session, iface):
	session.open(NetSpeedTestScreen)


def callFunction(iface):

		return netspeedMain


def Plugins(**kwargs):

 	return PluginDescriptor(name=_("NetSpeedTest"), description=_("Test net speed") + "\n", where=PluginDescriptor.WHERE_NETWORKSETUP, needsRestart=False, fnc={"ifaceSupported": callFunction, "menuEntryName": lambda x: _("NetSpeedTest"), "menuEntryDescription": lambda x: _("Test net speed...") + "\n"})
