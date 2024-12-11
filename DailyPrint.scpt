repeat 50 times
	tell application "Finder"
		set sourceFolder to folder POSIX file "/Users/doctormjeveritt/Desktop/PrintQueue/"
		try
			set theFile to item 1 of (sort files of sourceFolder by creation date) as alias
		on error
			set theFile to missing value
		end try
		
	end tell
	if theFile is not missing value then
		tell application "Preview"
			try
				open theFile
				print document 1 with properties {target printer:"Canon PRO-1000 series 6x4"}
				close document 1
			on error
				display dialog "Cant Print" & theFile
			end try
		end tell
		tell application "Finder"
			try
				move theFile to folder POSIX file "/Users/doctormjeveritt/Desktop/PrintQueue/Printed"
			on error
				display dialog "Cant move" & theFile
			end try
		end tell
	end if
	delay 86400
end repeat
