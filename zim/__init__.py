# -*- coding: utf8 -*-

# Copyright 2008 Jaap Karssenberg <pardus@cpan.org>

'''FIXME'''

# Bunch of meta data, used at least in the about dialog
__version__ = '0.42-alpha1'
__url__='http://www.zim-wiki.org'
__author__ = 'Jaap Karssenberg <pardus@cpan.org>'
__copyright__ = 'Copyright 2008 Jaap Karssenberg <pardus@cpan.org>'
__license__='''\
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
'''

import os
import logging
import gobject


logger = logging.getLogger('zim')
executable = 'zim'

class NotebookInterface(gobject.GObject):
	'''FIXME

	Subclasses can prove a class attribute "ui_type" to tell plugins what
	interface they support. This can be "gtk" or "html". If "ui_type" is None
	we run without interface (e.g. commandline export).
	'''

	# define signals we want to use - (closure type, return type and arg types)
	__gsignals__ = {
		'open-notebook': (gobject.SIGNAL_RUN_LAST, None, (object,)),
	}

	ui_type = None

	def __init__(self, notebook=None):
		gobject.GObject.__init__(self)
		self.notebook = None
		self.plugins = []

		logger.info('This is zim %s', __version__)
		try:
			from zim._version import version_info
			logger.debug(
				'branch: %(branch_nick)s\n'
				'revision: %(revno)d %(revision_id)s\n'
				'date: %(date)s\n',
				version_info )
		except ImportError:
			logger.debug('No bzr version-info found')

		if not notebook is None:
			self.open_notebook(notebook)

	def load_config(self):
		'''FIXME'''

	def load_plugins(self):
		'''FIXME'''
		plugins = ['spell', 'linkmap', 'printtobrowser'] # FIXME: get from config
		for plugin in plugins:
			self.load_plugin(plugin)

	def load_plugin(self, pluginname):
		'''FIXME'''
		import zim.plugins
		klass = zim.plugins.get_plugin(pluginname)
		plugin = klass(self)
		self.plugins.append(plugin)

	def unload_plugin(self, plugin):
		'''FIXME'''

	def open_notebook(self, notebook):
		'''FIXME'''
		import zim.notebook
		notebook = zim.notebook.get_notebook(notebook)
		self.emit('open-notebook', notebook)

	def do_open_notebook(self, notebook):
		'''FIXME'''
		self.notebook = notebook

	def export(self, format='html', template=None, page=None, output=None):
		'''FIXME'''
		if page is None:
			assert False, 'TODO: export whole notebook'
		if not output is None:
			assert False, 'TODO: output other than stdout'

		if isinstance(page,basestring):
			page = self.notebook.get_page(page)

		if template is None:
			print page.get_text(format=format).encode('utf8')
		else:
			import sys
			if isinstance(template, basestring):
				from zim.templates import get_template
				template = get_template(format, template)
			template.process(page, sys.stdout)

	def spawn(self, *argv):
		'''FIXME'''
		argv = list(argv)
		if argv[0] == 'zim':
			argv[0] = executable
		logger.info('Spawn process: %s', ' '.join(['"%s"' % a for a in argv]))
		try:
			pid = os.spawnvp(os.P_NOWAIT, argv[0], argv)
		except AttributeError:
			# spawnvp is not available on windows
			# TODO path lookup ?
			pid = os.spawnv(os.P_NOWAIT, argv[0], argv)
		logger.debug('New process: %i', pid)


# Need to register classes defining gobject signals
gobject.type_register(NotebookInterface)
