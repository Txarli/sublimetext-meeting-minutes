import sublime, sublime_plugin
import os
import re
from subprocess import call
import time
import json

from .mistune import markdown

import gettext

PACKAGE_PATH = os.path.dirname(__file__)
LANG_PATH = PACKAGE_PATH + '/lang'

DEFAULT_LANG_CODE = 'eu'

ASSISTANTS_INPUT_MESSAGE = 'Write the meeting assistant list, separated with commas'
LOGO_INPUT_MESSAGE = 'Write the logo path'
LANGUAGE_INPUT_MESSAGE = 'Write the language code'

ASSISTANTS_FILE_NAME = '/attendees.sublime-meetings'
LOGO_FILE_NAME = '/logo.sublime-meetings'
LANG_FILE_NAME = '/language.sublime-meetings'

HTML_START = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>'
BODY_END = '</body>'
HTML_END = '</html>'

def change_extension(file_name, new_ext):
	f, ext = os.path.splitext(file_name)
	return '%s%s' % (f, new_ext)

def load_file(filename):
	with open(filename) as file_:
		return file_.read()

def write_file(filename, text):
	with open(filename, 'w+') as file_:
		file_.write(text)

def get_configuration_file(markdown_file, file_name):
	assistants_directory = []

	assistants_directory.append(os.path.dirname(markdown_file))
	assistants_directory.append(file_name)

	return ''.join(assistants_directory)


class CreateMinuteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		html_source = []
		html_source.append(HTML_START)

		header_source = self.create_header()
		html_source.append(header_source)

		region = sublime.Region(0, self.view.size())
		md_source = self.view.substr(region)
		md_source.encode(encoding='UTF-8',errors='strict')
		html_source.append(markdown(md_source))
		html_source.append(BODY_END)

		css_file = "/home/txarli/.config/sublime-text-3/Packages/sublimetext-meeting-minutes/style.css"
		css_source = load_file(css_file)
		html_source.append('<style>%s</style>%s' % (css_source, HTML_END))


		file_name = self.view.file_name()
		html_file = change_extension(file_name, ".html")
		html_source_code = ''.join(html_source)
		write_file(html_file, html_source_code)

		self.save_pdf(html_file)

		print('Created minute.')

	def save_pdf(self, html_file):
		pdf_file = change_extension(html_file, ".pdf")
		call(["wkhtmltopdf",html_file,pdf_file])

	def create_header(self):
		markdown_file = self.view.file_name()
		markdown_dir = os.path.dirname(markdown_file)

		language_file = markdown_dir + LANG_FILE_NAME
		if os.path.isfile(language_file):
				lang_code = load_file(language_file)
		else:
			lang_code = DEFAULT_LANG_CODE

		lang = gettext.translation('MeetingMinutes', localedir=LANG_PATH, languages=[lang_code])
		lang.install()

		header_source = []
		header_source.append('<div class="header-parent"><div class="header-left"><h3>')
		header_source.append('%s: ' % _('Date'))
		date_format = _('%d/%m/%Y')
		meeting_date = time.strftime(date_format)
		header_source.append(meeting_date)
		header_source.append('</h3><h4>%s:</h4><ul>' % _('Atendees'))

		assistants_file = markdown_dir + ASSISTANTS_FILE_NAME
		meeting_assistants_list = load_file(assistants_file).splitlines()

		meeting_assistants = []
		for assistant in meeting_assistants_list:
			meeting_assistants.append('<li>%s</li>' % assistant)


		header_source.append(''.join(meeting_assistants))
		header_source.append('</ul></div><div class="header-right">')

		logo_file_path = '%s%s' % (markdown_dir, LOGO_FILE_NAME)

		if os.path.isfile(logo_file_path):
			logo_path = load_file(logo_file_path)
			header_source.append('<img src="%s">' % logo_path)

		header_source.append('</div></div>')

		return ''.join(header_source)


class WriteAssistantsCommand (sublime_plugin.TextCommand):
	def run(self, edit):
		window = self.view.window()

		assistants_file = get_configuration_file(self.view.file_name(), ASSISTANTS_FILE_NAME)
		if os.path.isfile(assistants_file):
			assistants = load_file(assistants_file)
		else:
			assistants = None
			
		if assistants:
			initial_text = re.sub('\n', ', ', assistants)
		else:
			initial_text = ''

		window.show_input_panel(ASSISTANTS_INPUT_MESSAGE, initial_text, self.save_assistants, self.save_assistants, self.cancel_assistants)

	def save_assistants(self, assistants_list):
		assistants = assistants_list.split(',')
		assistants_doc = ''
		for assistant in assistants:
			assistant = re.sub('^(^[\s]*)(\s)', '', assistant)
			if assistant != '':
				assistant += '\n'
				assistants_doc += assistant

		assistants_file = get_configuration_file(self.view.file_name(), ASSISTANTS_FILE_NAME)
		write_file(assistants_file, assistants_doc)

	def cancel_assistants(self):
		pass

class WriteLogoCommand (sublime_plugin.TextCommand):
	def run(self, edit):
		window = self.view.window()

		logo_file = get_configuration_file(self.view.file_name(), LOGO_FILE_NAME)
		if os.path.isfile(logo_file):
			logo_path = load_file(logo_file)
		else:
			logo_path = ''

		window.show_input_panel(LOGO_INPUT_MESSAGE, logo_path, self.save_logo, self.save_logo, self.cancel_assistants)

	def save_logo(self, logo_path):
		logo_file = get_configuration_file(self.view.file_name(), LOGO_FILE_NAME)
		write_file(logo_file, logo_path)

	def cancel_assistants(self):
		pass

class ChangeLanguageCommand(sublime_plugin.TextCommand):
	"""docstring for ChangeLanguageCommand"""
	def run(self, edit):
		window = self.view.window()

		language_file = get_configuration_file(self.view.file_name(), LANG_FILE_NAME)
		if os.path.isfile(language_file):
			lang = load_file(language_file)
		else:
			lang = ''

		window.show_input_panel(LANGUAGE_INPUT_MESSAGE, lang, self.save_language, self.save_language, self.cancel_language)

	def save_language(self, lang):
		language_file = get_configuration_file(self.view.file_name(), LANG_FILE_NAME)
		write_file(language_file, lang)

	def cancel_language(self):
		pass
