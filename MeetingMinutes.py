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

ASSISTANTS_INPUT_MESSAGE = 'Write the meeting assistant list, separated with commas'
LOGO_INPUT_MESSAGE = 'Write the logo path'

ASSISTANTS_FILE_NAME = '/attendees.sublime-meetings'
LOGO_FILE_NAME = '/logo.sublime-meetings'

HTML_START = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>'
BODY_END = '</body>'
HTML_END = '</html>'

class CreateMinuteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		html_source = HTML_START

		header_source = self.create_header()
		html_source += header_source

		region = sublime.Region(0, self.view.size())
		md_source = self.view.substr(region)
		md_source.encode(encoding='UTF-8',errors='strict')
		html_source += markdown(md_source) + BODY_END

		css_file = "/home/txarli/.config/sublime-text-3/Packages/sublimetext-meeting-minutes/style.css"
		with open(css_file) as file_:
			css_source = file_.read()
		html_source += '<style>' + css_source + '</style>' + HTML_END


		file_name = self.view.file_name()
		html_file = self.change_extension(file_name, ".html")
		with open(html_file, 'w+') as file_:
			file_.write(html_source)

		self.save_pdf(html_file)

	def change_extension(self,file_name, new_ext):
		f, ext = os.path.splitext(file_name)
		f += new_ext

		return f

	def save_pdf(self, html_file):
		pdf_file = self.change_extension(html_file, ".pdf")
		call(["wkhtmltopdf",html_file,pdf_file])

	def create_header(self):
		lang = gettext.translation('MeetingMinutes', localedir=LANG_PATH, languages=['es'])
		lang.install()

		markdown_file = self.view.file_name()
		markdown_dir = os.path.dirname(markdown_file)

		header_source = '<div class="header-parent"><div class="header-left"><h3>' + _('Date') + ': '
		date_format = _('%d/%m/%Y')
		meeting_date = time.strftime(date_format)
		header_source += meeting_date + ' </h3><h4>' + _('Atendees') + ':</h4><ul>'

		assistants_file = markdown_dir + ASSISTANTS_FILE_NAME
		with open(assistants_file) as file_:
			meeting_assistants_list = file_.read().splitlines()

		meeting_assistants = ''
		for assistant in meeting_assistants_list:
			meeting_assistants += '<li>' + assistant + '</li>'

		header_source += meeting_assistants + '</ul></div><div class="header-right">'

		logo_file_path = markdown_dir + LOGO_FILE_NAME

		if os.path.isfile(logo_file_path):
			with open(logo_file_path) as file_:
				logo_path = file_.read()
			header_source += '<img src="' + logo_path + '" width="100%">'

		header_source += '</div></div>'

		return header_source


class WriteAssistantsCommand (sublime_plugin.TextCommand):
	def run(self, edit):
		window = self.view.window()

		assistants_file = self.get_assistants_file()
		if os.path.isfile(assistants_file):
			with open(assistants_file) as file_:
				assistants = file_.read()
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

		assistants_file = self.get_assistants_file()
		with open(assistants_file, 'w+') as file_:
				file_.write(assistants_doc)

	def cancel_assistants(self):
		pass

	def get_assistants_file(self):
		markdown_file = self.view.file_name()
		assistants_directory = os.path.dirname(markdown_file)
		assistants_file = assistants_directory + ASSISTANTS_FILE_NAME

		return assistants_file

class WriteLogoCommand (sublime_plugin.TextCommand):
	def run(self, edit):
		window = self.view.window()

		logo_file = self.get_logo_file()
		if os.path.isfile(logo_file):
			with open(logo_file) as file_:
				logo_path = file_.read()
		else:
			logo_path = ''

		window.show_input_panel(LOGO_INPUT_MESSAGE, logo_path, self.save_logo, self.save_logo, self.cancel_assistants)

	def save_logo(self, logo_path):
		logo_file = self.get_logo_file()
		with open(logo_file, 'w+') as file_:
				file_.write(logo_path)

	def cancel_assistants(self):
		pass

	def get_logo_file(self):
		markdown_file = self.view.file_name()
		logo_directory = os.path.dirname(markdown_file)
		logo_file = logo_directory + LOGO_FILE_NAME

		return logo_file
