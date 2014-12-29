import sublime, sublime_plugin
import os
import re
from subprocess import call

from .mistune import markdown


class CreateMinuteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		region = sublime.Region(0, self.view.size())
		md_source = self.view.substr(region)
		md_source.encode(encoding='UTF-8',errors='strict')
		html_source = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>' + markdown(md_source) + '</body></html>'
		
		file_name = self.view.file_name()
		html_file, extension = os.path.splitext(file_name)
		html_file += ".html"
		with open(html_file, 'w+') as file_:
			file_.write(html_source)

		print(file_name)
		print(html_file)