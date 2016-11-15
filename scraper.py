import urllib

padx = "http://www.puzzledragonx.com"

pad_handle = urllib.urlopen(padx)

html = pad_handle.read()

print html
