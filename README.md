# What is this?
This is a simple script for obtaining words from a youtube video or .PDF, sorting them by frequency, translate them and getting a sample sentence.
A csv is generated, so you can import it into anki or do whatever you wish with it.
Column meanings:
"Word" Is the word in your target language.
"Frequency" Is the number of times the word appeared in the whole text or subtitles.
"Translation" Is the word in English.
"Context" Is a sample sentence in your target language that comes from the original text.

# Does this works with x language?
This was only tested with German and English.

# Can I use this for a whole novel?
Yes, it will work just fine.

# Requirements
You need to install python.
Then install the required packages with the following command:
`pip install pdfquery youtube_transcript_api deep_translator pandas numpy`
# Use
For youtube videos, go to the video and copy the id at the end of the link.
example:
if the link is https://www.youtube.com/watch?v=G_KIyWSucK4
the id is what comes after v=
In this case you'll have to copy "G_KIyWSucK4"
Then run the script.

For pdf, you have to put the file in the same folder as the script, then run the script.
warning: When the script asks for the name of the file, don't put the extension .pdf, just write the file name.
