import sublime, sublime_plugin
import os
import re
from subprocess import call
import time
import json

from .mistune import markdown

HTML_START = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>'
BODY_END = "</body>"
HTML_END = '</html>'

HEADER_SETTING_NAME = "template"

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
		header_source = '<div class="header-parent"><div class="header-left"><h3>Fecha: '
		meeting_date = time.strftime("%d/%m/%Y")
		header_source += meeting_date + ' </h3><h4>Asistentes</h4><ul>'

		json_file = '/home/txarli/Projects/Tests/markdown/assistants.sublime-meetings'
		with open(json_file) as file_:
			meeting_assistants_list = file_.read().splitlines()

		meeting_assistants = ''
		for assistant in meeting_assistants_list:
			meeting_assistants += '<li>' + assistant + '</li>'

		header_source += meeting_assistants + '</ul></div><div class="header-right"><img src="'
		
		logo_path = '/home/txarli/Projects/Tests/header/img/logo.jpg'
		header_source += logo_path + '" width="100%"></div></div>'

		return header_source

		
