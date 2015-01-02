# Sublime Text Meeting Minutes

Easily write meeting minutes using markdown in Sublime Text 3. Export it in Github Flavored Markdown style to html and pdf.

## Features:

- Render markdown to html and pdf.
- Add a header with:
    + Date
    + Attendees
    + Logo
- **Nowadays the header is created only in Spanish!** I'll do my best to change it to other languages.

## Instalation:

This plugin has been tested for Linux (Elementary OS) only. To install it:
- Download the [zip](https://github.com/Txarli/sublimetext-meeting-minutes/archive/master.zip).
- Go to your package directory clicking ``Preferences/Browse Packages...``.
- Extract the folder in the packages directory.
- *Optional:* Change its name to ``sublime-meetings``.

### Save to pdf

To save the html as pdf, you must have ``wkhtmltopdf`` installed (you can read more about this package [here](http://wkhtmltopdf.org/)). To install it in Ubuntu/Debian:

    sudo apt-get install wkhtmltopdf

### Markdown in Sublime Text

It's highly recommended to install the [Markdown Preview](https://github.com/revolunet/sublimetext-markdown-preview) plugin for Sublime Text. This is the best way to work with markdown in this text editor.

## Usage:

You can write your markdown minute in a normal text file. With this text written, you can use this commands from the command palette (``ctrl+shift+P``):

- **Sublime Meetings: Write attendees**: Opens a prompt where you can write the attendees list, sepparated with commas. It saves them in a file called ``assistants.sublime-minutes``.
- **Sublime Meetings: Pick logo**: Opens a prompt where you can write the logo file path (it should be an image file). It saves the path in a file called ``logo.sublime-minutes``.
- **Sublime Meetings: Create**: Saves the minute in pdf and html.

Support and collaboration:
- Write your suggestions, bugs, etc. in the [issues](https://github.com/Txarli/sublimetext-meeting-minutes/issues) page.
- Please, do all the forks and pull request submits you want.

**And remember, I'm a starter with this project, so be kind!**

## License:
The code is in github under a MIT License.
