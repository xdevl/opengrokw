#!/usr/bin/python3

import argparse
import os
import shutil
import subprocess
import zipfile

# Opengrok workspace
class OpenGrok:
	def __init__(self, opengrokdir):
		self.basedir = os.path.abspath(opengrokdir)
		self.sourcedir = os.path.join(self.basedir, 'src')
		self.datadir = os.path.join(self.basedir, 'data')
		self.configuration = os.path.join(self.basedir, 'configuration.xml')
		self.metadata = os.path.join(self.basedir, 'metadata')
		if os.path.exists(self.metadata):
			with open(self.metadata, 'r') as metadatafile:
				self.name = metadatafile.readline().rstrip()
				self.deploydir = metadatafile.readline().rstrip()
	
	# Deploy the opengrok workspace
	def deploy(self, webappsdir, name = None):
		opengrokwar = '/usr/share/java/opengrok/source.war'
		self.name = name if name else os.path.basename(self.basedir)
		self.deploydir = os.path.join(webappsdir, self.name)

		with open(self.metadata, 'w') as metadatafile:
			metadatafile.write(self.name + os.linesep)
			metadatafile.write(self.deploydir + os.linesep)

		os.makedirs(self.deploydir, 0o755, False)
		with zipfile.ZipFile(opengrokwar, 'r') as warfile:
			warfile.extractall(self.deploydir)
		
		webxml = os.path.join(self.deploydir, 'WEB-INF', 'web.xml')
		content = None
		with open(webxml, 'r') as xmlfile:
			content = xmlfile.read()
			
		content = content.replace('/var/opengrok/etc/configuration.xml', self.configuration)
	
		with open(webxml, 'w') as xmlfile:
			xmlfile.write(content)

	# Index the opengrok workspace or a list of specific modules if any
	def run(self, modules = []):
		opengrokjar = '/usr/share/java/opengrok/opengrok.jar'
		os.makedirs(self.sourcedir, 0o755, True)
		params = ['java',
				'-jar', opengrokjar,
				'--writeConfig', self.configuration,
				'--source', self.sourcedir,
				'--dataRoot', self.datadir,
				'--projects', '--verbose']
				
		for module in modules:	
			params.append('--include')
			params.append(os.path.join(self.sourcedir, module, '*'))
			
		subprocess.check_call(params)
	
	# Returns a module path		
	def moduledir(self, module):
		return os.path.join(self.sourcedir, module)
				

# Callback methods
def init(opengrok, args):
	opengrok.deploy(args.webappsdir, args.name)
	opengrok.run()
	
def index(opengrok, args):
	opengrok = OpenGrok(args.opengrokdir)
	opengrok.run(args.module)

def add(opengrok, args):
	module = args.name if args.name else os.path.basename(args.path)
	os.symlink(os.path.abspath(args.path), opengrok.moduledir(module))
	opengrok.run([module])
	
def remove(opengrok, args):
	if not args.module and input('Delete this opengrok repository ? [y/n] ').lower() == 'y':
		shutil.rmtree(opengrok.deploydir)
		shutil.rmtree(opengrok.basedir)
	for module in args.module:
		os.remove(opengrok.moduledir(module))
		opengrok.run([module])
	
def list(opengrok, args):
	for module in os.listdir(opengrok.sourcedir):
		print("%s -> %s"%(module, os.path.realpath(opengrok.moduledir(module))))
		
# Arguments definition
parser = argparse.ArgumentParser(
	description = 'Opengrok workspace manager')
parser.add_argument('--opengrokdir', default = os.getcwd(),
	help = 'Opengrok workspace directory. If none, the working directory will be used.')
subparsers = parser.add_subparsers()

initparser = subparsers.add_parser('init', add_help = False,
	description = 'Initialise and deploy a new opengrok workspace.')
initparser.add_argument('--webappsdir', default = '/var/lib/tomcat10/webapps',
	help = 'Directory into which deploy the webapp associated to the opengrok workspace.')
initparser.add_argument('--name',
	help = 'Name used to access the opengrok workspace from the webserver.')
initparser.set_defaults(func = init)

indexparser = subparsers.add_parser('index', add_help = False,
	description = 'Index the opengrok workspace.')
indexparser.add_argument('module', nargs = '*',
	help = 'A list of module to index. If none all modules will be indexed.')
indexparser.set_defaults(func=index)

addparser = subparsers.add_parser('add', add_help = False,
	description = 'Add a new module to the opengrok workspace.')
addparser.add_argument('path',
	help = 'The path of the module sources used for indexing.')
addparser.add_argument('--name',
	help = 'Name of the module. If none, the module sources directory name will be used.')
addparser.set_defaults(func = add)

rmparser = subparsers.add_parser('remove', add_help = False,
	description = 'Remove module(s) from the opengrok workspace.')
rmparser.add_argument('module', nargs = '*',
	help = 'Module to remove from the opengrok workspace. If none, the whole workspace will be deleted and undeployed (requires confirmation)')
rmparser.set_defaults(func = remove)

listparser = subparsers.add_parser('list', add_help = False,
	description = 'List the opengrok worspace modules.')
listparser.set_defaults(func = list)
								
# Main
args = parser.parse_args()
if hasattr(args, 'func'):
	args.func(OpenGrok(args.opengrokdir), args)
else:
	parser.print_help()
	print()
	for subparser in [initparser, indexparser, addparser, rmparser, listparser]:
		print('# ', end = '')
		subparser.print_help()
		print()
	print('NOTE: most of those commands will require a web server restart in order to take effect.')
