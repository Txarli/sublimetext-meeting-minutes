import sublime, sublime_plugin
from .mistune import markdown

class CreateMinuteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		region = sublime.Region(0, self.view.size())
		md_source = self.view.substr(region)
		md_source.encode(encoding='UTF-8',errors='strict')
		html_source = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>' + markdown(md_source) + '</body></html>'
		print(html_source)