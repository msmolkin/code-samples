tell application "System Events"
	-- Bring OBS window to front if it's minimized to tray
	tell process "OBS"
		click menu bar item 1 of menu bar 2
		
		-- Get the menu of the menu bar item
		set appMenu to menu 1 of menu bar item 1 of menu bar 2
		
		-- Check if the first menu item is "Show" instead of "Hide" to unhide OBS
		set menuItemName to name of menu item 1 of appMenu
		if menuItemName is "Show" then
			click menu item 1 of appMenu
			delay 1 -- required. if OBS is hidden via "Hide" and a fullscreen window is maximized, it can't show obs bc it doesn't leave the full screen window after issuing the "Show" command. e.g. if I'm editing in apple script editor and I have it maximized, and OBS is hidden, it doesn't work. but if it's not hidden, it works. fix? probably just delay a bit after activating.
		else
			click menu bar item 1 of menu bar 2
		end if
	end tell
	
	tell process "OBS"
		set frontmost to true
		try
			-- "try" because it gives error if window is not minimized
			perform action "AXRaise" of (first window)
		on error errMsg
			activate
		end try
	end tell
	--	
	tell process "OBS"
		delay 1
		
		-- Fit source to screen: Ctrl + F
		
		-- Updates that can be made to this script:
		-- Allow it to select the source even if it's not initially selected (see below)
		-- TODO: remaining click on one of the sources and press I need to select all of the sources
		-- then it will continue to run the "delete and undo" sequence that I've already written
		
		-- Delete the source (assuming the source is selected)
		key code 51 -- Press the 'Delete' key
		
		-- Wait for the confirmation dialog to appear
		-- delay 1
		
		-- Press 'Return' to confirm the deletion (assuming "Yes" is the default option)
		key code 36 -- Press the 'Return' key
		
		-- Allow the screen recorder time to reset
		delay 1.1
		
		-- Send an Undo command to undelete the source
		keystroke "z" using command down -- Press 'Cmd + Z'
		
		-- if not recording, click "Start Recording"
		delay 1
		key code 101
	end tell
	
	-- Delay for 2 seconds
	delay 2
	
	-- Minimize the OBS window
	-- TODO: This can be changed to hide the window using the same code as above
	--	tell process "OBS"
	--		-- perform action "AXMinimize" of (first window) -- this line doesn't work. didn't fix: either way, (1) I would prefer to hide than minimize the window, so no need to figure it out and (2) the following line does the same thing (except that it's not consistent with the cmd I used to raise it)
	--		try
	--			-- "try" because the command below gives an error after performing, but it doesn't affect the action and I don't want to deal with the error
	--			perform action "AXPress" of (first button whose subrole is "AXMinimizeButton") of every window --
	--		end try
	--	end tell
	tell process "OBS"
		click menu bar item 1 of menu bar 2
		set appMenu to menu 1 of menu bar item 1 of menu bar 2
		-- No need to check if the first menu item is "Hide" this time
		click menu item 1 of appMenu -- click "Hide"
	end tell
end tell
