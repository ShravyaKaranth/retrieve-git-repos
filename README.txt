# retrieve-git-repos

This app promots the user to enter GIT User Name.
The user input is checked against user details stored in the DB by quering SQLite using Django models.
If user name exist in DB :
retrieve details of every repository crated by that user, along with all the files
display results in tabular format with all required details

If user name is not found in DB :
connect to GitHub using api
retrieve details of every repository crated by that user, along with all the files
connect to DB 
store all retrieved daetails
display results in tabular format with all required details
