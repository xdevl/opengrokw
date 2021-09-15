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

	# Initialise or update the workspace when adding new projects
	def init(self):
		initParams = ['--noIndex']
		if os.path.exists(self.configuration):
			self.run(initParams + ['-R', self.configuration])
		else:
			os.makedirs(self.sourcedir, 0o755, True)
			self.run(initParams)

	# Index the opengrok workspace or a list of specific projects if any
	def index(self, projects):
		self.run(['-R', self.configuration] + projects)
	
	def run(self, params):
		opengrokjar = '/usr/share/java/opengrok/opengrok.jar'
		subprocess.check_call(['java', '-jar', opengrokjar,
				'--writeConfig', self.configuration,
				'--source', self.sourcedir,
				'--dataRoot', self.datadir,
				'--projects',
				'--progress',
			] + params)

	# Returns a project path		
	def projectdir(self, project):
		return os.path.join(self.sourcedir, project)
				

# Callback methods
def init(opengrok, args):
	opengrok.deploy(args.webappsdir, args.name)
	opengrok.init()
	
def index(opengrok, args):
	opengrok = OpenGrok(args.opengrokdir)
	opengrok.index(args.project)

def add(opengrok, args):
	project = args.name if args.name else os.path.basename(args.path)
	os.symlink(os.path.abspath(args.path), opengrok.projectdir(project))
	opengrok.init()
	opengrok.index([project])
	
def remove(opengrok, args):
	if not args.project and input('Delete this opengrok repository ? [y/n] ').lower() == 'y':
		shutil.rmtree(opengrok.deploydir)
		shutil.rmtree(opengrok.basedir)
	for project in args.project:
		os.remove(opengrok.projectdir(project))
		opengrok.index([project])
	
def list(opengrok, args):
	for project in os.listdir(opengrok.sourcedir):
		print("%s -> %s"%(project, os.path.realpath(opengrok.projectdir(project))))
		
# Arguments definition
parser = argparse.ArgumentParser(
	description = 'Opengrok workspace manager')
parser.add_argument('--opengrokdir', default = os.getcwd(),
	help = 'Opengrok workspace directory. If none, the working directory will be used.')
subparsers = parser.add_subparsers()

initparser = subparsers.add_parser('init', add_help = True,
	description = 'Initialise and deploy a new opengrok workspace.')
initparser.add_argument('--webappsdir', default = '/var/lib/tomcat10/webapps',
	help = 'Directory into which deploy the webapp associated to the opengrok workspace. If none, %(default)s will be used')
initparser.add_argument('--name',
	help = 'Name used to access the opengrok workspace from the webserver.')
initparser.set_defaults(func = init)

indexparser = subparsers.add_parser('index', add_help = True,
	description = 'Index the opengrok workspace.')
indexparser.add_argument('project', nargs = '*',
	help = 'A list of project to index. If none all projects will be indexed.')
indexparser.set_defaults(func=index)

addparser = subparsers.add_parser('add', add_help = True,
	description = 'Add a new project to the opengrok workspace.')
addparser.add_argument('path',
	help = 'The path of the project sources used for indexing.')
addparser.add_argument('--name',
	help = 'Name of the project. If none, the project sources directory name will be used.')
addparser.set_defaults(func = add)

rmparser = subparsers.add_parser('remove', add_help = True,
	description = 'Remove project(s) from the opengrok workspace.')
rmparser.add_argument('project', nargs = '*',
	help = 'project to remove from the opengrok workspace. If none, the whole workspace will be deleted and undeployed (requires confirmation)')
rmparser.set_defaults(func = remove)

listparser = subparsers.add_parser('list', add_help = True,
	description = 'List the opengrok worspace projects.')
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
