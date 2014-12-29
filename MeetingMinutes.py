import sublime, sublime_plugin

class CreateMinuteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.run_command("markdown_preview_select", {"target":"save"})
