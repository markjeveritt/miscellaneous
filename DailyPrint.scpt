tell application "Finder"
	set sourceFolder to folder POSIX file "/Users/doctormjeveritt/Desktop/PrintQueue/"
	try
		set theFile to item 1 of (sort files of sourceFolder by creation date) as alias
	on error
		set theFile to missing value
	end try
end tell
if theFile is not missing value then
	set thePrintFile to quoted form of POSIX path of (theFile as text)
	set theShell to ("lpr -P Canon -o media=4x6 -o resolution=600dpi -o media-type=50 -o fit-to-page " & thePrintFile)
	try
		do shell script theShell
	end try
	tell application "Finder"
		try
			move theFile to folder POSIX file "/Users/doctormjeveritt/Desktop/PrintQueue/Printed"
		on error
			display dialog "Cant move" & theFile
		end try
	end tell
end if
