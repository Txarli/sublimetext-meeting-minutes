import sublime, sublime_plugin
import os
import re
from subprocess import call

from .mistune import markdown

HTML_START = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>'
HTML_END = '</body></html>'

class CreateMinuteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		region = sublime.Region(0, self.view.size())
		md_source = self.view.substr(region)
		md_source.encode(encoding='UTF-8',errors='strict')
		html_source = HTML_START + markdown(md_source) + HTML_END
		
		file_name = self.view.file_name()
		html_file = self.change_extension(file_name, ".html")
		with open(html_file, 'w+') as file_:
			file_.write(html_source)

		self.save_pdf(html_file)
		print(file_name)
		print(html_file)

	def change_extension(self,file_name, new_ext):
		f, ext = os.path.splitext(file_name)
		f += new_ext

		return f

	def save_pdf(self, html_file):
		pdf_file = self.change_extension(html_file, ".pdf")
		call(["wkhtmltopdf",html_file,pdf_file])

		
