import os, sys, subprocess, shutil, datetime

#  Used UTC to be unambiguous about timezones, DST, etc.  Also, Windows doesn't like ":" in directory names, so replace with "."
#  This will produce a string of the form "YYYY-MM-DD HH.MM.SS UTC"
newVersionDate = datetime.datetime.utcnow().isoformat(" ",'seconds').replace(":",".") + " UTC"

# Run console command "ver" to get current Windows version.  No need to extract integers - we only care whether new != old
# immediate output of subprocess.Popen().communicate()[0] is a bytes object with leading and trailing line breaks (i.e. b'\r\nOutput from Ver\r\n')
# Strip the line breaks before converting string (or we get backslashes and 'r's and 'n's in the string
# Conversion to str yields prefix b and leading and trailing ' marks (i.e. "b\'Output from ver\'")
newVersion = str(subprocess.Popen("ver", stdout=subprocess.PIPE, shell=True).communicate()[0].strip()).strip("b'")

archivePath = "." #Root directory of system32 archives - same directory where this script is located
#archivePath = "D:/project/archive" # Root directory of system32 archives
oldVersionDate = ""
oldVersion = ""

# Retrieve version and date of last archived version
with open("version.txt","r") as f: oldVersion = f.readline().strip(); oldVersionDate = f.readline().strip()

<<<<<<< HEAD
if oldVersion == newVersion: sys.exit(0) # No update.  Stop here
=======
# if oldVersion == newVersion: sys.exit(0) # No update.  Stop here
>>>>>>> 0f25eb9ba0c96d22f58397e4bdf4f335e6cdba47

# Update version.txt file
with open("version.txt","w") as f: f.write(newVersion + "\r\n" + newVersionDate)

newSys32Path = archivePath + "/" + newVersionDate + "/system32" #Directory where archive of current system32 wiill be stored
oldSys32Path = archivePath + "/" + oldVersionDate + "/system32" #Directory where copy of previous version was stored
binDiffReportPath = newSys32Path + newVersionDate + "/Report" #Bin Diff report directory.  Reports for system32/subdir/file will go in Reports/subdir/file

print("New version detected.  Archiving system32 in " + newSys32Path)
# Copy contens of system32 to archive
shutil.copytree("C:/Windows/system32", newSys32Path, ignore=shutil.ignore_patterns('*.evtx'))

print("Archiving finished.")

# Record version number of current archive version for future reference
with open(archivePath + "/" + newVersionDate + "/version.txt", "x") as f: f.write(newversion + "\r\n" + newVersionDate)

if oldVersion == "": sys.exit(0)

# Scan archived system32 for modified executables and rund bin diff on any found
recursiveScan(newSys32Path, oldSys32Path, reportPath, "system32")

# Iterate over all files in archived system32 and run bin diff if executable and modified
# Calls itself recursively on subdirectories
def recursiveScan(path, date, oldDate, parent, dir):
	with os.scanDir(dir) as it:
		for entry in it:
						
			# if entry is a directory, scan recursively, then skip to next
			if entry.is_dir(): recursiveScan(newPath + "/" + dir, oldPath + "/" + dir, reportPath + "/" + dir, entry.name); continue
			
			if not entry.is_file(): continue # Should probably never happen, but just in case

			# Check if executable (look for prefix) and skip to next file if not
			with open(newPath + "/" + entry.name, 'rb') as f:
				if f.read(2) != b'MZ': continue

			# add check here for change from previous file, if no change then "continue"

			# placeholder for code to generate bin diff
			print("Check for changes and run bin diff on " + entry.path)
