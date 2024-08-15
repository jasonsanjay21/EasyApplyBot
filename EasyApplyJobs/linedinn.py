import time
import math
import random
import os
import pickle
import hashlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import utils
import constants
import config

class Linkedin:
    def __init__(self):
        utils.prYellow("🤖 Thanks for using Easy Apply Jobs bot, for more information you can visit our site - www.automated-bots.com")
        utils.prYellow("🌐 Bot will run in Chrome browser and log in to LinkedIn for you.")
        
        # Initialize the WebDriver
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=utils.chromeBrowserOptions())

        # Initialize cookies path
        self.cookies_path = f"{os.path.join(os.getcwd(), 'cookies')}/{self.getHash(config.email)}.pkl"
        
        # Ensure cookies directory exists
        cookies_dir = os.path.dirname(self.cookies_path)
        if not os.path.exists(cookies_dir):
            os.makedirs(cookies_dir)

        self.driver.get('https://www.linkedin.com')
        self.loadCookies()

        if not self.isLoggedIn():
            self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
            utils.prYellow("🔄 Trying to log in to LinkedIn...")
            try:    
                self.driver.find_element(By.ID, "username").send_keys(config.email)
                time.sleep(2)
                self.driver.find_element(By.ID, "password").send_keys(config.password)
                time.sleep(2)
                self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
                time.sleep(30)
            except:
                utils.prRed("❌ Couldn't log in to LinkedIn using Chrome. Please check your LinkedIn credentials in config files line 7 and 8.")

            self.saveCookies()
        
        # Start application
        self.linkJobApply()

    def getHash(self, string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def loadCookies(self):
        if os.path.exists(self.cookies_path):
            with open(self.cookies_path, "rb") as file:
                cookies = pickle.load(file)
                self.driver.delete_all_cookies()
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

    def saveCookies(self):
        with open(self.cookies_path, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)
    
    def isLoggedIn(self):
        self.driver.get('https://www.linkedin.com/feed')
        try:
            self.driver.find_element(By.XPATH, '//*[@id="ember14"]')
            return True
        except:
            return False 
    
    def login(self):
        self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
        utils.prYellow("🔄 Trying to log in to LinkedIn...")
        try:
            self.driver.find_element(By.ID, "username").send_keys(config.email)
            time.sleep(2)
            self.driver.find_element(By.ID, "password").send_keys(config.password)
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(30)
        except:
            utils.prRed("❌ Couldn't log in to LinkedIn. Please check your LinkedIn credentials in the config file.")

    def generateUrls(self):
        os.makedirs('data', exist_ok=True)
        try: 
            with open('data/urlData.txt', 'w', encoding="utf-8") as file:
                linkedinJobLinks = utils.LinkedinUrlGenerate().generateUrlLinks()
                for url in linkedinJobLinks:
                    file.write(url + "\n")
            utils.prGreen("✅ Apply URLs are created successfully, now the bot will visit those URLs.")
        except:
            utils.prRed("❌ Couldn't generate URLs. Make sure you have edited the config file.")

    def linkJobApply(self):
        self.generateUrls()
        countApplied = 0
        countJobs = 0

        urlData = utils.getUrlDataFile()

        for url in urlData:
            self.driver.get(url)
            time.sleep(random.uniform(1, constants.botSpeed))

            totalJobs = self.driver.find_element(By.XPATH, '//small').text 
            totalPages = utils.jobsToPages(totalJobs)

            urlWords = utils.urlToKeywords(url)
            lineToWrite = f"\n Category: {urlWords[0]}, Location: {urlWords[1]}, Applying {totalJobs} jobs."
            self.displayWriteResults(lineToWrite)

            for page in range(totalPages):
                currentPageJobs = constants.jobsPerPage * page
                url = f"{url}&start={currentPageJobs}"
                self.driver.get(url)
                time.sleep(random.uniform(1, constants.botSpeed))

                offersPerPage = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')
                offerIds = [int(offer.get_attribute("data-occludable-job-id").split(":")[-1]) for offer in offersPerPage]
                time.sleep(random.uniform(1, constants.botSpeed))

                for offer in offersPerPage:
                    if not self.element_exists(offer, By.XPATH, ".//*[contains(text(), 'Applied')]"):
                        offerId = int(offer.get_attribute("data-occludable-job-id").split(":")[-1])
                        offerIds.append(offerId)

                for jobID in offerIds:
                    offerPage = f'https://www.linkedin.com/jobs/view/{jobID}'
                    self.driver.get(offerPage)
                    time.sleep(random.uniform(1, constants.botSpeed))

                    countJobs += 1
                    jobProperties = self.getJobProperties(countJobs)

                    if "blacklisted" in jobProperties:
                        lineToWrite = f"{jobProperties} | * 🤬 Blacklisted Job, skipped!: {offerPage}"
                        self.displayWriteResults(lineToWrite)
                    
                    else:                    
                        easyApplybutton = self.easyApplyButton()

                        if easyApplybutton:
                            easyApplybutton.click()
                            time.sleep(random.uniform(1, constants.botSpeed))
                            
                            try:
                                self.chooseResume()
                                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
                                time.sleep(random.uniform(1, constants.botSpeed))

                                lineToWrite = f"{jobProperties} | * 🥳 Just Applied to this job: {offerPage}"
                                self.displayWriteResults(lineToWrite)
                                countApplied += 1

                            except:
                                try:
                                    self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
                                    time.sleep(random.uniform(1, constants.botSpeed))
                                    self.chooseResume()
                                    comPercentage = self.driver.find_element(By.XPATH, 'html/body/div[3]/div/div/div[2]/div/div/span').text
                                    percenNumber = int(comPercentage.split("%")[0])
                                    result = self.applyProcess(percenNumber, offerPage)
                                    lineToWrite = f"{jobProperties} | {result}"
                                    self.displayWriteResults(lineToWrite)
                                
                                except Exception: 
                                    self.chooseResume()
                                    lineToWrite = f"{jobProperties} | * 🥵 Cannot apply to this Job! {offerPage}"
                                    self.displayWriteResults(lineToWrite)
                        else:
                            lineToWrite = f"{jobProperties} | * 🥳 Already applied! Job: {offerPage}"
                            self.displayWriteResults(lineToWrite)

            utils.prYellow(f"Category: {urlWords[0]}, {urlWords[1]} applied: {countApplied} jobs out of {countJobs}.")
        
        utils.donate(self)

    def chooseResume(self):
        try:
        # Ensure that the resume upload button is present
            self.driver.find_element(By.CLASS_NAME, "jobs-document-upload__title--is-required")
            
            # Find the resume upload input element
            upload_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            
            # Set the path of the resume file
            resume_path = r"C:\Users\JASON\Downloads\JasonLXResume.pdf"
            
            # Upload the resume by sending the file path to the input element
            upload_input.send_keys(resume_path)
            
            utils.prGreen("✅ Resume uploaded successfully.")
            
        except Exception as e:
            utils.prRed(f"❌ Error in choosing resume: {e}")


    def getJobProperties(self, count):
        jobTitle = ""
        jobDetail = ""
        jobLocation = ""

        try:
            jobTitle = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'job-title')]").text.strip()
            if any(blItem.lower() in jobTitle.lower() for blItem in config.blackListTitles):
                jobTitle += "(blacklisted title)"
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"⚠️ Warning in getting jobTitle: {e}")
            jobTitle = ""

        try:
            jobDetail = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs')]//div").text.replace("·", "|")
            if any(blItem.lower() in jobDetail.lower() for blItem in config.blacklistCompanies):
                jobDetail += "(blacklisted company)"
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"⚠️ Warning in getting jobDetail: {e}")
            jobDetail = ""

        try:
            jobWorkStatusSpans = self.driver.find_elements(By.XPATH, "//span[contains(@class,'ui-label ui-label--accent-3 text-body-small')]//span[contains(@aria-hidden,'true')]")
            jobLocation = " | ".join(span.text for span in jobWorkStatusSpans)
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"⚠️ Warning in getting jobLocation: {e}")
            jobLocation = ""

        return f"{count} | {jobTitle} | {jobDetail} {jobLocation}"

    def easyApplyButton(self):
        try:
            time.sleep(random.uniform(1, constants.botSpeed))
            button = self.driver.find_element(By.XPATH, "//div[contains(@class,'jobs-apply-button--top-card')]//button[contains(@class, 'jobs-apply-button')]")
            return button
        except:
            return False

    def applyProcess(self, percentage, offerPage):
        applyPages = math.floor(100 / percentage) - 2
        for _ in range(applyPages):
            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()

        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Review your application']").click()
        time.sleep(random.uniform(1, constants.botSpeed))

        if not config.followCompanies:
            try:
                self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']").click()
            except:
                pass

        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
        time.sleep(random.uniform(1, constants.botSpeed))

        return f"* 🥳 Just Applied to this job: {offerPage}"

    def displayWriteResults(self, lineToWrite: str):
        try:
            print(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            utils.prRed(f"❌ Error in DisplayWriteResults: {e}")

    def element_exists(self, parent, by, selector):
        return len(parent.find_elements(by, selector)) > 0

if __name__ == "__main__":
    start = time.time()
    Linkedin()
    end = time.time()
    utils.prYellow(f"--- Took: {round((end - start) / 60)} minute(s).")
