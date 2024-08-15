# General bot settings to use Pro settings you need to download Pro version from: www.automated-bots.com

#PRO FEATURE - browser you want the bot to run ex: ["Chrome"] or ["Firefox"]. Firefox is only supported in Pro feature
browser = ["Chrome"]
# Enter your Linkedin password and username below. Do not commit this file after entering these credentials.
# Linkedin credentials
email = "@gmail.com"
password = "@jJ"

#PRO FEATURE - Optional! run browser in headless mode, no browser screen will be shown it will work in background.
headless = False
#PRO FEATURE - Optional! If you left above credentials fields empty. For Firefox or Chrome enter profile dir to run the bot to prevent logging in your account each time
# get Firefox profile path by typing following url: about:profiles
firefoxProfileRootDir = r""
# get Chrome profile path by typing following url: chrome://version/
chromeProfilePath = r""

# These settings are for running Linkedin job apply bot.
# location you want to search the jobs - ex : ["Poland", "Singapore", "New York City Metropolitan Area", "Monroe County"]
# continent locations:["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa", "Australia"]
location = [ "Hyderabad"]
# keywords related with your job search
keywords = ["DevOps Intern"]
#job experience Level - ex:  ["Internship", "Entry level" , "Associate" , "Mid-Senior level" , "Director" , "Executive"]
experienceLevels = [ "Internship", "Entry level" ]
#job posted date - ex: ["Any Time", "Past Month" , "Past Week" , "Past 24 hours"] - select only one
datePosted = ["Past Week", "Past Month"]
#job type - ex:  ["Full-time", "Part-time" , "Contract" , "Temporary", "Volunteer", "Intership", "Other"]
jobType = ["Full-time", "Part-time" , "Contract"]
#remote  - ex: ["On-site" , "Remote" , "Hybrid"]
remote = ["On-site" , "Remote" , "Hybrid"]
#salary - ex:["$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", "$140,000+", "$160,000+", "$180,000+", "$200,000+" ] - select only one
salary = [ "400000"]
#sort - ex:["Recent"] or ["Relevent"] - select only one
sort = ["Recent"]
#Blacklist companies you dont want to apply - ex: ["Apple","Google"]
blacklistCompanies = []
#Blaclist keywords in title - ex:["manager", ".Net"]
blackListTitles = []
#Follow companies after sucessfull application True - yes, False - no
followCompanies = False



FirstName = "Jason"
LastName = "Sanjay"
Email = "jasonsanjayy21@gmail.com"
LinkedInProfileURL = "www.linkedin.com/in/jasonsanjayy"
Phone = "+91 8248701432" #OPTIONAL
Location = "Chennai" #OPTIONAL
HowDidYouHeard = "LinkedIn" #OPTIONAL
ConsiderMeForFutureOffers = True #true = yes, false = no

 # Testing & Debugging features
displayWarnings = False