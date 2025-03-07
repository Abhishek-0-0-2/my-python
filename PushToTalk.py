#Python Appium
import os
import unittest
import multiprocessing
import time
import datetime
import ast
import re

from appium import webdriver
from appium import *
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.common.exceptions import NoSuchElementException  
from time import sleep

###################################################################################################
###################################################################################################
##
##    !#!        !#!   !######    !######      ####     !######    !#     #!
##    !#!        !#!   !#!    #   !#!    #   !#    #!   !#!    #    !#   #!
##    !#!        !#!   !#!    #   !#!    #   !#    #!   !#!    #     !# #!
##    !#!        !#!   !######    !######    !######!   !######       !#!
##    !#!        !#!   !#!    #   !#!  #     !#    #!   !#!  #        !#!
##    !#!!!!!!   !#!   !#!    #   !#!   #    !#    #!   !#!   #       !#!
##    !#######   !#!   !######    !#!    #   !#    #!   !#!    #      !#!
##                                                                                  Version 1.0
###################################################################################################
###################################################################################################

class Android:
		
	def __init__(self,serial,timeout):
		desired_caps = {}
		print("Start of Test")
	   
		desired_caps['platformName'] = 'Android'
		desired_caps['udid'] = serial        
		desired_caps['bundleId']='com.mobilelabsinc.trustbrowser/com.mobilelabsinc.trustbrowser.MainActivity'
		desired_caps['automationName'] = 'Appium'
		desired_caps['newCommandTimeout'] = timeout 
		desired_caps['deviceConnectUsername'] = 'team@automation.com'
		desired_caps['deviceConnectApiKey'] = 'e627dfe3-2a84-4de1-bcb4-0edc35b84b75'
		
		self.driver = webdriver.Remote('http://107.250.171.220/Appium', desired_caps)
		self.actions = TouchAction(self.driver)
		
		# pause a moment, so xml generation can occur
		sleep(2)
				
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		
	def close(self):
		self.driver.quit()

	#================================================================================================================
	# Method Name	     :  open_eptt_app
	#
	# Description        :  This method will open EPTT App.
	#
	# Arguments	         :  
	#
	# Returns	         :  
	#
	# Date Modified      :  Newly Added [21-Sep-2018]
	#================================================================================================================		
		
	def open_eptt_app(self):		 
				
		#Swipe down the notification bar
		size=self.driver.get_window_size()
		start_y = int(size["height"]*0.001)
		end_y   = int(size["height"]*0.40) 
		start_x = int(size["width"]*0.50)
		end_x = int(size["width"]*0.50)
		
		#Swipe the screen
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		print("Device: swiped down the notification bar")
		sleep(5)
		
		#Click on the EPTT App
		self.driver.find_element_by_xpath(".//*[@text='My Status:']").click()
		print("Device: Opened the EPTT App")
		sleep(20)
			
		#Navigate to App Home page if different page is opened
		for i in range (0, 2):
			elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
			if len(elem2) > 0:
				elem2[0].click()
				print("Device: Clicked on Back button")
				sleep(2)
		
		
	#================================================================================================================
	# Method Name	     :  create_contact
	#
	# Description        :  This method will add the contact to EPTT App.
	#
	# Arguments	         :  name,number,avatar='set avatar none',colour='set color none',favorite='FAVORITE',status_flag="0",delete_flag="0"
	#
	# Returns	         :  PASS/FAIL/The phone number entered already exists
	#
	# Date Modified      :  Newly Added [06-July-2018]
	#================================================================================================================

	def create_contact(self,name,number, avatar="none", colour="none", favourite="null", status_flag="0", delete_flag="0"):
		
		"""This keyword will create a new contact.
		
		Arguments are passed as given below.
		
		desired_name,desired_phonenumber,'avatar','colour' and 'favorite',status_falg,delete_flag
		
		colour = none(default),red,blue,green,purple,orange,lightblue
		
		favorite = null(default),FAVORITE
		
		avatar = none(default),construction,driver,front desk,notepad,worker,warehouse,airplane,delivery,envelope,housekeeping,ptt phone,telephone,supervisor,book,desktop pc,field services,laptop pc,room service,tree,car,dispatcher,flower,medical,security,truck
		
		Here avatar, colour ,favorite, status_falg and delete_flag are optional arguments.
		
		"""
		#Initializing the status value	
		status="FAIL"
			
		print("Start of eptt")
		
		if int(delete_flag) == 1:
			#Delete the contact if already present
			self.delete_user(number,dc_flag=1)
			sleep(2)

		#Open eptt app
		self.open_eptt_app()
		
		#Select the Contact tab
		self.driver.find_element_by_id("ext-tab-3").click()
		print("Device: Navigated to the Contact tab")
		sleep(2)
		
		#Click on the Add Contact option
		self.driver.find_element_by_xpath(".//*[@text='Add Contact']").click()
		print("Device: Clicked on the Add Contact option")
		sleep(2)
		
		#Check if network error pop-up
		error=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Data connection')]")
		if len(error) > 0:
			print("Device: Data connection is unavailable error is found")
			
			#Click OK option
			self.driver.find_element_by_xpath(".//*[@text='OK']").click()
			print("Device: Clicked on OK option")
			sleep(2)
		else:
			#Click on New Contact option
			elem=self.driver.find_elements_by_xpath(".//*[@text='New Contact']")
			if len(elem) == 0:
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
				
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			else:
				elem[0].click()
				print("Device: Clicked on New Contact option Button")
				sleep(5)
				
				#self.driver.find_element_by_xpath(".//*[@text='Enter Name']").send_keys(name)
				#self.driver.find_element_by_xpath(".//*[@text='Enter Phone Number']").send_keys(number)
				elem1=self.driver.find_elements_by_class_name("android.widget.EditText")
				if len(elem1) > 0:
					#Input the name
					elem1[0].send_keys(name)
					#self.driver.find_element_by_xpath(".//*[@resource-id='ext-element-4630']").send_keys(name)				
					print("Device: Inserted the name")
					sleep(2)
	
					#Click OK/DONE button
					self.driver.press_keycode(66)
					print("Device: Clicked OK/DONE button")
					sleep(2)
				
					#Input the number
					elem1[1].send_keys(number)
					#self.driver.find_element_by_xpath(".//*[@resource-id='ext-element-4660']").send_keys(number)	
					print("Device: Inserted the number")
					sleep(2)
					
					#Click OK/DONE button
					self.driver.press_keycode(66)
					print("Device: Clicked OK/DONE button")
					sleep(2)
				
				#Select favorite
				if favourite == 'FAVORITE':
					#Set the contact as favorite
					self.driver.find_element_by_xpath(".//*[@text='FAVORITE']").click()
					print("Device: Contact is made as favorite")
					sleep(2)
				
				#Select the colour
				self.driver.find_element_by_xpath(".//*[@text='set color "+colour+"']").click()	
				print("Device: Selected "+colour+" colour")
				sleep(2)
								
				#Select the avatar
				self.driver.find_element_by_xpath(".//*[@text='select avatar']").click()				
				print ("Device: Clicked on avatar options")
				sleep(2)
				
				#Set avatar
				self.driver.find_element_by_xpath(".//*[@text='set avatar "+avatar+"']").click()
				print("Device: Selected "+avatar+" avatar")
				sleep(5)
								
				elem5=self.driver.find_elements_by_xpath(".//*[@text='Save']")
				if len(elem5)>0:
					#Save the contact
					self.driver.find_element_by_xpath(".//*[@text='Save']").click()
					print("Device: Clicked Save button")
						
					for i in range(0, 10):
						elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact created')]")
						elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'The phone number')]")
						if len(elem2) > 0:
							print("Device: Contact saved successfully")
							sleep(2)
							status="PASS"				
							break
						elif len(elem3) > 0:
							print("Devices: The phone number entered is invalid")
							
							#Click on OK
							self.driver.find_element_by_xpath(".//*[@text='OK']").click()
							print("Device: Clicked OK button")
							sleep(2)
							
							#Cancel the contact
							self.driver.find_element_by_xpath(".//*[@text='Cancel']").click()
							print("Device: Clicked Cancel button")
							sleep(2)
							
							#Click on Yes
							self.driver.find_element_by_xpath(".//*[@text='Yes']").click()
							print("Device: Clicked Yes button")
							sleep(2)						
						sleep(1)
				else:
					#Click on Back button
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
					print("Device: Clicked on Back button")
					sleep(2)
				
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2) 
		
		#Check the status is visible after adding a contact
		if status == "PASS" :
			if int(status_flag) == 1:
				p=self._check_status(name)
				return p
			else:		
				return status

	#================================================================================================================
	# Method Name	     :  present_status
	#
	# Description        :  This method will return the present status of the user
	#
	# Arguments	         :  
	#
	# Returns	         :  Available/Do Not Disturb
	#
	# Date Modified      :  Newly Added [24-July-2018]
	#================================================================================================================				
			
	def present_status(self):	
		
		"""This keyword will return the present status of the user

		"""
		#Initializing the status value	
		status=""
					
		#Open eptt app
		self.open_eptt_app()
		
		#Find the present mode
		elem1 = self.driver.find_elements_by_xpath(".//*[@text='Available']")
		elem2 = self.driver.find_elements_by_xpath(".//*[@text='Do Not Disturb']")
		if len(elem1) > 0:
			status = "Available"
		elif len(elem2) > 0:
			status = "Do Not Disturb"				
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return 	status
					
	#================================================================================================================
	# Method Name	     :  change_status
	#
	# Description        :  This method will change the status of the user
	#
	# Arguments	         :  mode
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [06-July-2018]
	#================================================================================================================		
		
			
	def change_status(self,mode):	
		
		"""This keyword will change the status of the user
		
		Arguments are passed as given below.
		
		mode (Available or Do Not Disturb)
		
		"""
		#Initializing the status value	
		status="FAIL"
					
		#Open eptt app
		self.open_eptt_app()
		
		#Find the present mode
		#elem1=driver.find_elements_by_xpath(".//*[@text='Available']")
		#if len(elem1) > 0:
		#	present_mode = "Available"
		#else:
		#	present_mode = "Do Not Disturb"
		#
		#if present_mode == mode:
		#	print("Device: Device is already in the required mode")
		#	status="PASS"
		#	sleep(2)
		#else:
		#Click on the Drop Down Button
		#elem2 = self.driver.find_elements_by_xpath(".//*[@resource-id='ext-element-82']")
		# elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'My Presence')]")		
		# if len(elem2) > 0:
			# elem2[0].click()
			# print("Device: Clicked on the dropdown button")
			# sleep(2)
		
		elem1 = self.driver.find_elements_by_xpath(".//*[@text='Available']")
		elem2 = self.driver.find_elements_by_xpath(".//*[@text='Do Not Disturb']")
		if len(elem1) > 0:
			elem1[0].click()
			sleep(2)
		elif len(elem2) > 0:
			elem2[0].click()
			sleep(2)
		
		#Select the required state
		if mode == "Available" :
			self.driver.find_element_by_xpath(".//*[@text='Available']").click()
			print("Device: Selected Available status")
			sleep(5)
			status="PASS"
		elif mode == "Do Not Disturb" :
			self.driver.find_element_by_xpath(".//*[@text='Do Not Disturb']").click()
			print("Device: Selected Do Not Disturb status")
			sleep(5)
			status="PASS"
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return 	status
		
	#================================================================================================================
	# Method Name	     :  send_IPA
	#
	# Description        :  This method will send an Instant Personal Alert to the user chosen from contact
	#
	# Arguments	         :  name,history
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [10-July-2018]
	#================================================================================================================			

	def send_IPA(self,name, history=0, manual_dial=0, favorite_flag=0):
	
		"""This keyword will send an Instant Personal Alert to the user choosen from contact.
		
		Arguments are passed as given below.
		
		name_1
		
		"""
		#Initializing the status value	
		status="FAIL"
					
		#Open eptt app
		self.open_eptt_app()
		
		if int(history) == 0 and int(manual_dial) == 0:
			if int(favorite_flag) == 0:
				#Select the Contact tab
				self.driver.find_element_by_id("ext-tab-3").click()
				print("Device: Navigated to the Contact tab")
				sleep(2)
				
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
				
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
				
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) == 0:
					#Select the Contact for IPA
					#Select the contact found
					elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
					elem1[0].click()
					print("Device: Clicked on the contact name")
					sleep(5)
					
					#Click on IPA button
					#self.driver.find_element_by_xpath(".//*[@text='Send alert']")
					#elem1=self.driver.find_elements_by_xpath(".//*[@resource-id='ext-button-1095']")	
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Send alert')]").click()	
					print("Device: Clicked on Send Alert option")
		
					for i in range(0, 10):
						elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Alert sent')]")
						if len(elem2) > 0:
							print("Device: Alert sent successfully")
							sleep(2)
							status="PASS"
							break
						sleep(1)
					
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Information')]")
					if len(elem2)>0:
						print("Device: You cannot send an alert while your availability is 'Do Not Disturb'. Please change your status.")
						
						#Click on the Back Button    
						self.driver.press_keycode(4)
						print("Device: Clicked on Back Button")
						sleep(2)
					
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				else:
					print("Device: No contact is found with the given name")
							
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)
			else:
				#Select the Favorite tab
				self.driver.find_element_by_xpath(".//*[@text='Favorite']").click()
				print("Device: Navigated to the Favorite tab")
				sleep(2)
				
				#Click on Favorite Contacts tab
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Favorite Contacts')]").click()
				print("Device: Clicked on Favorite Contacts tab")
				sleep(2)
				
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
				
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
				
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) == 0:
					#Select the Contact for IPA
					#Select the contact found
					elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
					elem1[0].click()
					print("Device: Clicked on the contact name")
					sleep(5)
					
					#Click on IPA button
					#self.driver.find_element_by_xpath(".//*[@text='Send alert']")
					#elem1=self.driver.find_elements_by_xpath(".//*[@resource-id='ext-button-1095']")	
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Send alert')]").click()	
					print("Device: Clicked on Send Alert option")
		
					for i in range(0, 10):
						elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Alert sent')]")
						if len(elem2) > 0:
							print("Device: Alert sent successfully")
							sleep(2)
							status="PASS"
							break
						sleep(1)
					
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Information')]")
					if len(elem2)>0:
						print("Device: You cannot send an alert while your availability is 'Do Not Disturb'. Please change your status.")
						
						#Click on the Back Button    
						self.driver.press_keycode(4)
						print("Device: Clicked on Back Button")
						sleep(2)
					
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				else:
					print("Device: No contact is found with the given name")
							
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)

		elif int(history) == 1:
			#Select the History tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for IPA
				#Select the contact found
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, '"+name+"')]")
				elem1[1].click()
				print("Device: Clicked on the contact name")
				sleep(5)
				
				#Click on IPA button
				#self.driver.find_element_by_xpath(".//*[@text='Send alert']")
				#elem1=self.driver.find_elements_by_xpath(".//*[@resource-id='ext-button-1095']")	
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send alert')]").click()	
				print("Device: Clicked on Send Alert option")
	
				for i in range(0, 10):
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Alert sent')]")
					if len(elem2) > 0:
						print("Device: Alert sent successfully")
						sleep(2)
						status="PASS"
						break
					sleep(1)
				
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Information')]")
				if len(elem2)>0:
					print("Device: You cannot send an alert while your availability is 'Do Not Disturb'. Please change your status.")
					
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
			else:
				print("Device: No history is found with the given name")
						
				#Click on the clear search option
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
				print("Device: Clicked on the clear search option")
				sleep(2)
		elif int(manual_dial) == 1:
			#Select the Menu option
			self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
			print("Device: Navigated to the Menu option")
			sleep(2)
			
			#Select the Manual dial option
			self.driver.find_element_by_xpath(".//*[@text='Manual Dial']").click()
			print("Device: Navigated to the Manual Dial option")
			sleep(2)
			
			elem1=self.driver.find_elements_by_class_name("android.widget.EditText")
			if len(elem1) > 0:
				#Input the number
				name = str(name).replace("-","")
				elem1[0].send_keys(name)
				#self.driver.find_element_by_xpath(".//*[@resource-id='ext-element-4630']").send_keys(name)				
				print("Device: Inserted the number")
				sleep(2)
	
				#Click OK/DONE button
				self.driver.press_keycode(66)
				print("Device: Clicked OK/DONE button")
				sleep(2)
				
				#Select the PTT Call option
				self.driver.find_element_by_xpath(".//*[@text='PTT Call']").click()
				print("Device: Navigated to the PTT Call option")
				sleep(2)
				
				#Click on IPA button
				#self.driver.find_element_by_xpath(".//*[@text='Send alert']")
				#elem1=self.driver.find_elements_by_xpath(".//*[@resource-id='ext-button-1095']")	
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send alert')]").click()	
				print("Device: Clicked on Send Alert option")
	
				for i in range(0, 10):
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Alert sent')]")
					if len(elem2) > 0:
						print("Device: Alert sent successfully")
						sleep(2)
						status="PASS"
						break
					sleep(1)
				
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Information')]")
				if len(elem2)>0:
					print("Device: You cannot send an alert while your availability is 'Do Not Disturb'. Please change your status.")
					
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				
				for i in range (0, 2):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return status	

	#================================================================================================================
	# Method Name	     :  verify_IPA
	#
	# Description        :  This method will verify the received IPA
	#
	# Arguments	         :  option
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [10-July-2018]
	#================================================================================================================			

	def verify_IPA(self,option):
	
		"""This keyword will verify the received IPA
		
		Arguments are passed as given below.
		
		option(Reply or Not now)
		
		"""
		#Initializing the status value	
		status="FAIL"
		
		#Navigate to App Home page if different page is opened
		for i in range (0, 2):
			elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
			if len(elem2) > 0:
				elem2[0].click()
				print("Device: Clicked on Back button")
				sleep(2)
		
		elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Instant')]")
		#elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
		if len(elem1) > 0:
			#Click on the IPA received
			print("Device: Clicked on received IPA")
			status="PASS"
			sleep(2)				
		
			if option == "Reply" :
				#Click on Reply
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Reply')]").click()
				print("Device: Clicked on Reply option")
				sleep(2)
				
				#Click and hold the call button			
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
				if len(elem1) > 0:	
					#Initiate a EPTT call
					self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(20000).release().perform()
					print("Device: Initiated an EPTT call")
					sleep(5)
					
					for i in range (0, 2):
						elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
						if len(elem2) > 0:
							elem2[0].click()
							print("Device: Clicked on Back button")
							sleep(2)
							
			elif option == "Not now" :
				#Click on Not now
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Not now')]").click()
				print("Device: Clicked on Not now option")
				sleep(2)
				
		else:		
			#Open eptt app
			self.open_eptt_app()
	
			#Check for MCA
			for i in range(0, 1000):
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Instant')]")
				#elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
				if len(elem1) > 0:
					#Click on the IPA received
					print("Device: Clicked on received IPA")
					status="PASS"
					sleep(2)				
				
					if option == "Reply" :
						#Click on Reply
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Reply')]").click()
						print("Device: Clicked on Reply option")
						sleep(2)
						
						#Click and hold the call button			
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
						if len(elem1) > 0:	
							#Initiate a EPTT call
							self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(20000).release().perform()
							print("Device: Initiated an EPTT call")
							sleep(5)
							
							for i in range (0, 2):
								elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
								if len(elem2) > 0:
									elem2[0].click()
									print("Device: Clicked on Back button")
									sleep(2)
						
					elif option == "Not now" :
						#Click on Not now
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Not now')]").click()
						print("Device: Clicked on Not now option")
						sleep(2)	
	
				break		
			
		return status	

	#================================================================================================================
	# Method Name	     :  verify_status
	#
	# Description        :  This method will verify the status (Available or Do Not Disturb) of the contact
	#
	# Arguments	         :  name,mode
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [11-July-2018]
	#================================================================================================================			

	def verify_status(self,name,mode):
	
		"""This keyword will verify the other devices state.
		
		Arguments are passed as given below.
		
		name_1,mode(Available or Do Not Disturb)
		
		"""
		#Initializing the status value	
		status="FAIL"
			
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Contact tab
		self.driver.find_element_by_id("ext-tab-3").click()
		print("Device: Navigated to the Contact tab")
		sleep(2)
		
		#Check whether the given name is already avaliable in the contacts
		elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '" + name + "')]")
		if len(elem) > 0:
			#Select the Contact for IPA
			#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
			elem[0].click()
			print("Device: Clicked on the contact name")
			sleep(5)
			
			#Click on Contact Details button
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()	
			print("Device: Clicked on Contact Details option")
			sleep(5)
			
			#elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'presence, " + mode + "')]")
			if mode == "Available" :
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'presence, Available')]")			
				if len(elem1) > 0:
					print("Device: Given device is present in the Available mode")
					status="PASS"
					sleep(2)
				else:
					print("Device: Given device is not present in the Available mode")
					sleep(2)
			elif mode == "Do Not Disturb" :
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'presence, DND')]")			
				if len(elem1) > 0:
					print("Device: Given device is present in the Do Not Disturb mode")
					status="PASS"
					sleep(2)
				else:
					print("Device: Given device is not present in the Do Not Disturb mode")
					sleep(2)
			
			#Click on the Back Option
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
			print("Device: Clicked on Back option")
			sleep(2)
			
			#Click on the Back Button    
			self.driver.press_keycode(4)
			print("Device: Clicked on Back Button")
			sleep(2)
		else:
			print("Device: Given name is not found in the contact")
			status="FAIL"
			sleep(2)
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return status	
			
	#================================================================================================================
	# Method Name	     :  make_private_call
	#
	# Description        :  This method will initiate EPTT call
	#
	# Arguments	         :  name,hold_time_arg
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [11-July-2018]
	#================================================================================================================			

	def make_private_call(self,name,hold_time_arg, manual_dial=0, DND=0, favorite_flag=0):
	
		"""This keyword will Initiate an EPTT call.
		
		Arguments are passed as given below.
		
		name_1,hold_time_arg
		
		Here hold_time_arg is in seconds
		
		"""
		#Initializing the status value
		status="FAIL"		
		
		#Open eptt app
		self.open_eptt_app()
		
		#Convert the hold time from seconds to mili-seconds
		hold_time = int(hold_time_arg)*1000
		print(hold_time)
		
		if int(manual_dial) == 0:	
			if int(favorite_flag) == 0:
				#Select the Contact tab
				self.driver.find_element_by_id("ext-tab-3").click()
				print("Device: Navigated to the Contact tab")
				sleep(2)
				
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
			
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
				
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) == 0 :
					#Select the Contact for IPA
					#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
					elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
					elem1[0].click()
					print("Device: Clicked on the contact name")
					sleep(5)
									
					#Initiate EPTT Call
					#self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
					#sleep(2)
					
					if int(DND) == 0:				
						#Click and hold the call button			
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
						if len(elem1) > 0:	
							#Initiate a EPTT call
							self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(hold_time).release().perform()
							print("Device: Initiated an EPTT call")
							status="PASS"
							sleep(5)
							
							elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
							if len(elem2) > 0:
								elem2[0].click()
								print("Device: Clicked on Back button")
								sleep(2)
					elif int(DND) == 1:
						#Click and hold the call button			
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
						if len(elem1) > 0:	
							#Initiate a EPTT call
							self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
							print("Device: Clicked on the EPTT call")
							sleep(5)
			
							#Check for the information message
							elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Information')]")
							if len(elem2) > 0:
								print("Device: Information:'The Contact you are trying to call is in 'Do Not Disturb' status. Please try again later.'")
								sleep(5)
								#Click on the Back Button    
								self.driver.press_keycode(4)
								print("Device: Clicked on Back Button")
								sleep(2)
								status="PASS"	

								elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
								if len(elem2) > 0:
									elem2[0].click()
									print("Device: Clicked on Back button")
									sleep(2)	
						else:										
							#Click on the Back Option
							self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
							print("Device: Clicked on Back option")
							sleep(2)
				else:
					print("Device: No contact is found with the given name")
						
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)
			else:
				#Select the Favorite tab
				self.driver.find_element_by_xpath(".//*[@text='Favorite']").click()
				print("Device: Navigated to the Favorite tab")
				sleep(2)
				
				#Select the Favorite Contact tab
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Favorite Contacts')]").click()
				print("Device: Clicked on Favorite Contacts tab")
				sleep(2)
				
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
			
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
				
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) == 0 :
					#Select the Contact for IPA
					#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
					elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
					elem1[0].click()
					print("Device: Clicked on the contact name")
					sleep(5)
									
					#Initiate EPTT Call
					#self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
					#sleep(2)
					
					if int(DND) == 0:				
						#Click and hold the call button			
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
						if len(elem1) > 0:	
							#Initiate a EPTT call
							self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(hold_time).release().perform()
							print("Device: Initiated an EPTT call")
							status="PASS"
							sleep(5)
							
							elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
							if len(elem2) > 0:
								elem2[0].click()
								print("Device: Clicked on Back button")
								sleep(2)
					elif int(DND) == 1:
						#Click and hold the call button			
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
						if len(elem1) > 0:	
							#Initiate a EPTT call
							self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
							print("Device: Clicked on the EPTT call")
							sleep(5)
			
							#Check for the information message
							elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Information')]")
							if len(elem2) > 0:
								print("Device: Information:'The Contact you are trying to call is in 'Do Not Disturb' status. Please try again later.'")
								sleep(5)
								#Click on the Back Button    
								self.driver.press_keycode(4)
								print("Device: Clicked on Back Button")
								sleep(2)
								status="PASS"

								elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
								if len(elem2) > 0:
									elem2[0].click()
									print("Device: Clicked on Back button")
									sleep(2)	
						else:										
							#Click on the Back Option
							self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
							print("Device: Clicked on Back option")
							sleep(2)
				else:
					print("Device: No contact is found with the given name")
						
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)
					
		elif int(manual_dial) == 1:	
			#Select the Menu option
			self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
			print("Device: Navigated to the Menu option")
			sleep(2)
			
			#Select the Manual dial option
			self.driver.find_element_by_xpath(".//*[@text='Manual Dial']").click()
			print("Device: Navigated to the Manual Dial option")
			sleep(2)
			
			elem1=self.driver.find_elements_by_class_name("android.widget.EditText")
			if len(elem1) > 0:
				#Input the number
				name = str(name).replace("-","")
				elem1[0].send_keys(name)
				#self.driver.find_element_by_xpath(".//*[@resource-id='ext-element-4630']").send_keys(name)				
				print("Device: Inserted the number")
				sleep(2)
	
				#Click OK/DONE button
				self.driver.press_keycode(66)
				print("Device: Clicked OK/DONE button")
				sleep(2)
				
				#Select the PTT Call option
				self.driver.find_element_by_xpath(".//*[@text='PTT Call']").click()
				print("Device: Navigated to the PTT Call option")
				sleep(2)
				
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'number')]")
				elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
				if len(elem2) > 0:
					print("Devices: The phone number entered is invalid")
					
					#Click on OK
					self.driver.find_element_by_xpath(".//*[@text='OK']").click()
					print("Device: Clicked OK button")
					sleep(2)
					
					#Click on Back
					self.driver.find_element_by_xpath(".//*[@text='Back']").click()
					print("Device: Clicked Back button")
					sleep(2)
				elif len(elem3) > 0:
					if int(DND) == 0:
						#Initiate a EPTT call
						self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(hold_time).release().perform()
						print("Device: Initiated an EPTT call")
						
						elem4=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call cannot complete')]")
						if len(elem4) > 0:
							print("Device: Call cannot complete, not a PTT subscriber.")
							
							#Click on OK
							self.driver.find_element_by_xpath(".//*[@text='OK']").click()
							print("Device: Clicked OK button")
							sleep(2)
						
							#Click on Back
							self.driver.find_element_by_xpath(".//*[@text='Back']").click()
							print("Device: Clicked Back button")
							sleep(2)
						
							#Click on Back
							self.driver.find_element_by_xpath(".//*[@text='Back']").click()
							print("Device: Clicked Back button")
							sleep(2)						
						else:	
							status="PASS"
							
							elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
							if len(elem2) > 0:
								elem2[0].click()
								print("Device: Clicked on Back button")
								sleep(2)
								
								elem2[0].click()
								print("Device: Clicked on Back button")
								sleep(2)
					elif int(DND) ==1:
						#Click and hold the call button			
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
						if len(elem1) > 0:	
							#Initiate a EPTT call
							self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
							print("Device: Clicked on the EPTT call")
							sleep(5)
			
							#Check for the information message
							elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Information')]")								
							if len(elem2) > 0:
								print("Device: Information:'The Contact you are trying to call is in 'Do Not Disturb' status. Please try again later.'")
								sleep(5)
								#Click on the Back Button    
								self.driver.press_keycode(4)
								print("Device: Clicked on Back Button")
								sleep(2)
								status="PASS"

								elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
								if len(elem2) > 0:
									elem2[0].click()
									print("Device: Clicked on Back button")
									sleep(2)

									elem2[0].click()
									print("Device: Clicked on Back button")
									sleep(2)	
						else:										
							#Click on the Back Option
							self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
							print("Device: Clicked on Back option")
							sleep(2)
					
		return status			


	#================================================================================================================
	# Method Name	     :  exchange_floor
	#
	# Description        :  This method will exchange EPTT call
	#
	# Arguments	         :  hold_time_arg
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [19-July-2018]
	#================================================================================================================			

	def exchange_floor(self,hold_time_arg):
	
		"""This keyword will exchange an EPTT call.
		
		Arguments are passed as given below.
		
		hold_time_arg
		
		Here hold_time_arg is in seconds
		
		"""
		#Initializing the status value
		status="FAIL"		
		
		# #Click on the Home Button    
		# self.driver.press_keycode(3)
		# print("Device: Clicked on Home Button")
		# sleep(2)
		
		#Convert the hold time from seconds to mili-seconds
		hold_time = int(hold_time_arg)*1000
		print(hold_time)
		

		#Exchange floor for EPTT call
		for i in range(0, 10000):
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No one')]")
			#elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
			if len(elem1) > 0:
				#sleep(int(hold_time_arg))
				sleep(2)
				self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(hold_time).release().perform()
				#print(elem1)
				#actions.long_press(elem1[0]).wait(hold_time).release().perform()
				status="PASS"
				print("Device: Exchanged floor on EPTT Private call")
				sleep(2)
				break			
						
		return status			
				

	#================================================================================================================
	# Method Name	     :  _check_status
	#
	# Description        :  This method will get the status for the given name in the contact.
	#
	# Arguments	         :  name
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [20-July-2018]
	#================================================================================================================
			
	def _check_status(self,name):
		
		"""This keyword will get the status for the given name in the contact.
		
		Arguments are passed as given below.
		
		 name_1, driver
		
		"""
		#Initializing the status value	
		status="FAIL"
		
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Contact tab
		self.driver.find_element_by_id("ext-tab-3").click()
		print("Device: Navigated to the Contact tab")
		sleep(2)
		
		#Check whether the given name is already available in the contacts
		elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '" + name + "')]")
		if len(elem) > 0:
			#Select the Contact for IPA
			#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
			elem[0].click()
			print("Device: Clicked on the contact name")
			sleep(5)
			
			#Click on Contact Details button
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()	
			print("Device: Clicked on Contact Details option")
			sleep(5)
			
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Status')]")	
			if len(elem1)> 0:
				status="PASS"
				print("Device: Status is found")
				sleep(2)
			else:
				print("Device: Status is not found")
			
			#Click on the Back Option
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
			print("Device: Clicked on Back option")
			sleep(2)
			
			#Click on the Back Button    
			self.driver.press_keycode(4)
			print("Device: Clicked on Back Button")
			sleep(2)
		else:
			print("Device: Given name is not found in the contact")
			status="FAIL"
			sleep(2)
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return status
		
	#================================================================================================================
	# Method Name	     :  airplane_mode_off
	#
	# Description        :  This method performs the airplane mode off activity.
	#
	# Arguments	         : 
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [26-Jul-2018]
	#================================================================================================================

	def airplane_mode_off(self):
		#Initializing the status value
		status="FAIL"
		
		
		#######################################
		##Airplane Mode: OFF : START
		#######################################
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2) 
		
		#Open Settings APP with Airplane Mode activity
		self.driver.start_activity("com.android.settings", "com.android.settings.Settings$AirplaneModeSettingsActivity");
		print("Device: opened the settings APP with Airplane Mode activity")
		sleep(2) 
		
		#Checking whether Airplane Mode is ON or not and if it is ON turn it OFF
		elem = self.driver.find_elements_by_xpath(".//*[@text='ON']")
		if len(elem) > 0:
			elem[0].click()
			print("Airplane mode is OFF Now")
			status="PASS"
		else:
			print("Airplane mode is already OFF")
			status="PASS"
				
		sleep(2)
			 
		print("Device:Airplane mode :'OFF' operations are completed")
		sleep(2) 	
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		 		
		
		#######################################
		##Mobile Airplane Mode: OFF : END
		#######################################    
			
		return status
		
	#================================================================================================================
	# Method Name	     :  airplane_mode_on
	#
	# Description        :  This method performs the airplane mode on activity.
	#
	# Arguments	         :  
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [26-Jul-2018]
	#================================================================================================================

	def airplane_mode_on(self):
		
		#Initializing the status value
		status="FAIL"
				
		#######################################
		##Airplane Mode: ON : START
		####################################### 
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2) 

		#Open Settings APP with Airplane Mode activity
		self.driver.start_activity("com.android.settings", "com.android.settings.Settings$AirplaneModeSettingsActivity");
		print("Device: opened the settings APP with Airplane Mode activity")
		sleep(2) 

		#Checking whether Airplane Mode is OFF or not and if it is OFF turn it ON
		elem = self.driver.find_elements_by_xpath(".//*[@text='OFF']")
		if len(elem) > 0:
			elem[0].click()
			print("Airplane mode is ON Now")
			status="PASS"
		else:
			print("Airplane mode is already ON")
			status="PASS"
				
		sleep(2)
			 
		print("Device:Airplane mode :'ON' operations are completed")
		sleep(2) 	

		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		 	

		#######################################
		##Mobile Airplane Mode: ON : END
		#######################################    

		return status	
	    
	#================================================================================================================
	# Method Name	     :  wifi_mode_on
	#
	# Description        :  This method performs the wifi mode on activity.
	#
	# Arguments	         :  
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [26-Jul-2018]
	#================================================================================================================
	
	def wifi_mode_on(self):
		
		#Initializing the status value
		status="FAIL"
				
		#######################################
		##WiFi Mode: ON : START
		#######################################  
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2) 
				
		#Open Settings APP with WiFi Mode activity
		self.driver.start_activity("com.android.settings", "com.android.settings.Settings$WifiSettingsActivity");
		print("Device: opened the settings APP with WiFi Mode activity")
		sleep(5) 
		
		#Checking whether WiFi Mode is OFF or not and if it is OFF turn it ON
		elem = self.driver.find_elements_by_xpath(".//*[@text='OFF']")
		if len(elem) > 0:
			elem[0].click()
			print("WiFi mode is ON Now")
			status="PASS"
		else:
			print("WiFi mode is already ON")
			status="PASS"
				
		sleep(2)
			 
		print("Device:WiFi mode :'ON' operations are completed")
		sleep(2) 	
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		 	
		
		#######################################
		##Mobile WiFi Mode: ON : END
		#######################################    

		return status	
		
	#================================================================================================================
	# Method Name	     :  wifi_mode_off
	#
	# Description        :  This method performs the wifi mode off activity.
	#
	# Arguments	         :  
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [26-Jul-2018]
	#================================================================================================================	    

	def wifi_mode_off(self):
		
		#Initializing the status value
		status="FAIL"
				
		#######################################
		##WiFi Mode: OFF : START
		#######################################  
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2) 
		

		#Open Settings APP with wifi Mode activity
		self.driver.start_activity("com.android.settings", "com.android.settings.Settings$WifiSettingsActivity");
		print("Device: opened the settings APP with wifi Mode activity")
		sleep(2) 
		
		#Checking whether WiFi Mode is ON or not and if it is ON turn it OFF
		elem = self.driver.find_elements_by_xpath(".//*[@text='ON']")
		if len(elem) > 0:
			elem[0].click()
			print("wifi mode is OFF Now")
			status="PASS"
		else:
			print("wifi mode is already OFF")
			status="PASS"
				
		sleep(2)
			 
		print("Device:Wifi mode :'OFF' operations are completed")
		sleep(2) 	
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
				 			
		#######################################
		##Mobile WiFi Mode: OFF : END
		#######################################    
			
		return status	
			
	#================================================================================================================
	# Method Name	     :  search_contact
	#
	# Description        :  This method will search the for the contact.
	#
	# Arguments	         :  name
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [26-July-2018]
	#================================================================================================================
			
	def search_contact(self,name, contact=0, history=0, group=0):
		
		"""This keyword will search the for the contact.
		
		Arguments are passed as given below.
		
		name_1
		
		"""
		#Initializing the status value	
		status="FAIL"
					
		#Open eptt app
		self.open_eptt_app()
		
		if int(contact) == 1:
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Check if contacts tab is empty or not
			elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add contacts:')]")
			if len(elem2) == 0:		
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
		
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
					
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) > 0:			
					print("Device: No contact is found with the given name")				
					
				elif len(elem) == 0 :
					print("Device: Contact with the given name is available")
					status="PASS"
					
				#Click on the clear search option
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
				print("Device: Clicked on the clear search option")
				sleep(2)	
			else:
				print("Device: No Contacts to search")
		elif int(history) == 1:
			#Select the History tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			
			name = str(name).replace("-","")
			
			#Check if contacts tab is empty or not
			elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No History')]")
			if len(elem2) == 0:		
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
		
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
					
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) > 0:			
					print("Device: No contact is found with the given name")									
				elif len(elem) == 0 :
					print("Device: Contact with the given name is available")
					status="PASS"
					
				#Click on the clear search option
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
				print("Device: Clicked on the clear search option")
				sleep(2)	
			else:
				print("Device: No Contacts to search")
		elif int(group) == 1:
			#Select the Group tab
			#self.driver.find_element_by_xpath(".//*[@text='Group']").click()
			self.driver.find_element_by_id("ext-tab-4").click()
			#self.driver.find_element_by_xpath("//android.view.View[@text='Group']").click()	
			print("Device: Navigated to the Groups tab")
			sleep(2)
			
			#Check if Groups tab is empty or not
			elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add')]")
			if len(elem2) == 0:		
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
		
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
					
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) > 0:			
					print("Device: No group is found with the given name")				
					
				elif len(elem) == 0 :
					print("Device: Group with the given name is available")
					status="PASS"
					
				#Click on the clear search option
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
				print("Device: Clicked on the clear search option")
				sleep(2)	
			else:
				print("Device: No Group to search")
				
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
			
		return status
		
	#================================================================================================================
	# Method Name	     :  duplicate_contact
	#
	# Description        :  This method will try to create a duplicate contact.
	#
	# Arguments	         :  
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [26-July-2018]
	#================================================================================================================
			
	def duplicate_contact(self):
		
		"""This method will try to create a duplicate contact.
				
		"""
		#Initializing the status value	
		status="FAIL"
					
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Contact tab
		self.driver.find_element_by_id("ext-tab-3").click()
		print("Device: Navigated to the Contact tab")
		sleep(2)
		
		#Check if contacts tab is empty or not
		elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add contacts:')]")
		if len(elem2) == 0:		
			#Select the contact
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
			
			#Click on the contact
			elem1[0].click()
			print("Device: Clicked on the contact")
			sleep(2)
			
			#Click on Contact Details button
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()	
			print("Device: Clicked on Contact Details option")
			sleep(5)
			
			#Fetch the name and number of the contact
			elem3=self.driver.find_elements_by_class_name("android.widget.EditText")
			name = elem3[0].get_attribute("text")
			print(name)
			number = elem3[1].get_attribute("text")
			print(number)
			
			#Click on the Back Option
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
			print("Device: Clicked on Back option")
			sleep(2)
			
			#Click on the Back Button    
			self.driver.press_keycode(4)
			print("Device: Clicked on Back Button")
			sleep(2)
			
			#Click on the Add Contact option
			self.driver.find_element_by_xpath(".//*[@text='Add Contact']").click()
			print("Device: Clicked on the Add Contact option")
			sleep(2)
			
			#Click on New Contact option
			self.driver.find_element_by_xpath(".//*[@text='New Contact']").click()
			print("Device: Clicked on New Contact option Button")
			sleep(5)

			elem4=self.driver.find_elements_by_class_name("android.widget.EditText")

			#Input the name
			elem4[0].send_keys(name)
			#self.driver.find_element_by_xpath(".//*[@resource-id='ext-element-4630']").send_keys(name)				
			print("Device: Inserted the name")
			sleep(2)

			#Click OK/DONE button
			self.driver.press_keycode(66)
			print("Device: Clicked OK/DONE button")
			sleep(2)
			
			#Input the number
			elem4[1].send_keys(number)
			#self.driver.find_element_by_xpath(".//*[@resource-id='ext-element-4660']").send_keys(number)	
			print("Device: Inserted the number")
			sleep(2)
			
			#Click OK/DONE button
			self.driver.press_keycode(66)
			print("Device: Clicked OK/DONE button")
			sleep(2)	
				
			#Save the contact
			self.driver.find_element_by_xpath(".//*[@text='Save']").click()
			print("Device: Clicked Save button")
			sleep(5)
			
			#Check if the Information prompt contains duplicate message
			elem5 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'The phone number entered already exists')]")
			if len(elem5) > 0:
				print("Device: 'The phone number entered already exists. Please enter a different number.'Information message is displayed")
				sleep(2)
				
				#Click on OK option
				self.driver.find_element_by_xpath(".//*[@text='OK']").click()
				print("Device: Clicked on OK option")
				sleep(2)
				
				#Click on Cancel option
				self.driver.find_element_by_xpath(".//*[@text='Cancel']").click()
				print("Device: Clicked on Cancel option")
				sleep(2)
				
				#Click on Yes option
				self.driver.find_element_by_xpath(".//*[@text='Yes']").click()
				print("Device: Clicked on Yes option")
				sleep(2)
				
				status="PASS"
				
		else:
			print("Device: No Contacts to search")
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		
		return status
								
	#================================================================================================================
	# Method Name	     :  counter_values
	#
	# Description        :  This method will return the counter values.
	#
	# Arguments	         :  
	#
	# Returns	         :  count
	#
	# Date Modified      :  Newly Added [31-July-2018]
	#================================================================================================================
			
	def counter_values(self):
		
		"""This method will return the counter values.
		
		"""
		#Initializing the counter value	
		count = {'Device_Contacts':None, 'Device_Groups':None, 'Corporate_Contacts':None, 'Corporate_Groups':None, 'Favorite_Contacts':None, 'Favorite_Groups':None}
					
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Menu option
		self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
		print("Device: Navigated to the Menu option")
		sleep(2)
		
		#Select the Settings option
		self.driver.find_element_by_xpath(".//*[@text='Settings']").click()
		print("Device: Navigated to the Settings option")
		sleep(2)
				
		# Identifying the Screen coordinates
		size=self.driver.get_window_size()
		print(size)
		end_y = '700'
		start_y = '1700'
		end_x = '400'
		start_x = '400'

		print(start_x,start_y,end_x,end_y)

		#Scroll down till the Capacity option is found
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		sleep(2)
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		sleep(5)
		
		#Click on Capacity option
		elem = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Capacity')]")
		if len(elem) > 0 :
			elem[0].click()
			print("Device: Clicked on Capacity option")
			sleep(2)
			
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, '/300')]")
			if len(elem1) > 0:
				count['Device_Contacts'] = elem1[0].get_attribute("text")
			
			elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, '/30')]")
			if len(elem2) > 0:			
				count['Device_Groups'] = elem2[1].get_attribute("text")
				
			elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, '/1000')]")
			if len(elem3) > 0:	
				count['Corporate_Contacts'] = elem3[0].get_attribute("text")
				
			elem4=self.driver.find_elements_by_xpath(".//*[contains(@text, '/100')]")
			if len(elem4) > 0:
				count['Corporate_Groups'] = elem4[1].get_attribute("text")
				
			elem5=self.driver.find_elements_by_xpath(".//*[contains(@text, '/300')]")
			if len(elem5) > 0:
				count['Favorite_Contacts'] = elem5[1].get_attribute("text")
			
			elem6=self.driver.find_elements_by_xpath(".//*[contains(@text, '/50')]")
			if len(elem6) > 0:						
				count['Favorite_Groups'] = elem6[0].get_attribute("text")
						
			#Click on BACK
			self.driver.press_keycode(4)
			print("Device: Clicked on BACK button")
			sleep(2)
			print("PASS")
		else:
			print("Device: Capacity option is not seen")
			sleep(2)
			print("FAIL")
			
		#Click on BACK
		self.driver.press_keycode(4)
		print("Device: Clicked on BACK button")
		sleep(2)
		
		#Click on HOME
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		
		return count
		

	#================================================================================================================
	# Method Name	     :  create_group
	#
	# Description        :  This method will add the group to EPTT App.
	#
	# Arguments	         :  group_name,contact_nameLst,avatar='set avatar none',colour='set color none',favorite='FAVORITE'
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [31-July-2018]
	#================================================================================================================

	def create_group(self,group_name,contact_nameLst, avatar="none", colour="none", favourite="null"):
		
		"""This keyword will create a new contact.
		
		Arguments are passed as given below.
		
		desired_name,['contact_1','contact_2',...],'avatar','colour' and 'favorite'
		
		colour = none(default),red,blue,green,purple,orange,lightblue
		
		favorite = null(default),FAVORITE
		
		avatar = none(default),construction,driver,front desk,notepad,worker,warehouse,airplane,delivery,envelope,housekeeping,ptt phone,telephone,supervisor,book,desktop pc,field services,laptop pc,room service,tree,car,dispatcher,flower,medical,security,truck
		
		Here avatar, colour ,favorite are optional arguments.
		
		"""
		#Initializing the status value	
		status="FAIL"				
		user_name = ast.literal_eval(contact_nameLst)

		#Open eptt app
		self.open_eptt_app()
		
		#Select the Groups tab
		#self.driver.find_element_by_xpath(".//*[@text='Group']").click()
		self.driver.find_element_by_id("ext-tab-4").click()
		#self.driver.find_element_by_xpath("//android.view.View[@text='Group']").click()	
		print("Device: Navigated to the Groups tab")
		sleep(2)
		
		#Click on the Add Group option
		self.driver.find_element_by_xpath(".//*[@text='Add Group']").click()
		print("Device: Clicked on the Add Group option")
		sleep(2)
		
		#Check if network error pop-up
		error=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Data connection')]")
		if len(error) > 0:
			print("Device: Data connection is unavailable error is found")
			
			#Click OK option
			self.driver.find_element_by_xpath(".//*[@text='OK']").click()
			print("Device: Clicked on OK option")
			sleep(2)
		else:
			#self.driver.find_element_by_xpath(".//*[@text='Enter Name']").send_keys(name)
			#self.driver.find_element_by_xpath(".//*[@text='Enter Phone Number']").send_keys(number)
			elem1=self.driver.find_elements_by_class_name("android.widget.EditText")
			if len(elem1) > 0:
				#Input the name
				elem1[0].send_keys(group_name)
				#self.driver.find_element_by_xpath(".//*[@resource-id='ext-element-4630']").send_keys(name)				
				print("Device: Inserted the name")
				sleep(2)
	
				#Click OK/DONE button
				self.driver.press_keycode(66)
				print("Device: Clicked OK/DONE button")
				sleep(2)
									
			for i in range (len(user_name)):
				#Click on Add Members
				self.driver.find_element_by_xpath(".//*[@text='Add Members']").click()
				print("Device: Clicked on Add Members button")
				sleep(2)
				
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(user_name[i])
				print("Device: Entered the given name in search bar")
				sleep(2)

				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)

				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) > 0:
					print("Device: No Group is found with the given name")
					
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)
					
					#Click on Back button
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
					print("Device: Clicked on Back button")
					sleep(2)
				else:
					#select the contacts to be added in the group
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Name')]").click()	
					print("Device: Added a member")
					sleep(2)
					
					#Click Save button
					self.driver.find_element_by_xpath(".//*[@text='Save']").click()
					print("Device: Clicked Save button")
					sleep(2)			
			
			#Select favorite
			if favourite == 'FAVORITE':
				#Set the Group as favorite
				self.driver.find_element_by_xpath(".//*[@text='FAVORITE']").click()
				print("Device: Group is made as favorite")
				sleep(2)
			
			#Select the colour
			self.driver.find_element_by_xpath(".//*[@text='set color "+colour+"']").click()	
			print("Device: Selected "+colour+" colour")
			sleep(2)
			
			
			#Select the avatar
			self.driver.find_element_by_xpath(".//*[@text='select avatar']").click()				
			print ("Device: Clicked on avatar options")
			sleep(2)
			
			#Set avatar
			self.driver.find_element_by_xpath(".//*[@text='set avatar "+avatar+"']").click()
			print("Device: Selected "+avatar+" avatar")
			sleep(5)		
			
			elem5=self.driver.find_elements_by_xpath(".//*[@text='Save']")
			if len(elem5)>0:
				#Save the group
				self.driver.find_element_by_xpath(".//*[@text='Save']").click()
				print("Device: Clicked Save button")
	
				for i in range(0, 10):
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Group created')]")
					if len(elem2) > 0:
						print("Device: Group saved successfully")
						sleep(2)
						status="PASS"
						break
					sleep(1)
			else:
				#Click on Back button
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
				print("Device: Clicked on Back button")
				sleep(2)
			
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2) 
				
		return status

	#================================================================================================================
	# Method Name	     :  delete_user
	#
	# Description        :  This method will delete the user.
	#
	# Arguments	         :  name
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [31-July-2018]
	#================================================================================================================
		
	def delete_user(self,name, dc_flag=0, dg_flag=0, fc_flag=0, fg_flag=0, hc_flag=0, del_flag=1):

		"""This keyword will delete the user.
		
		Arguments are passed as given below.
		
		name_1
		
		"""
		#Initializing the status value	
		status="FAIL"
							
		#Open eptt app
		self.open_eptt_app()
		
		if int(dc_flag) == 1 :	
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
	
			#Check if contacts tab is empty or not
			elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add contacts:')]")
			if len(elem2) == 0:		
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
		
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
					
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) > 0:			
					print("Device: No contact is found with the given name")
					
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)				
					status="PASS"
				elif len(elem) == 0 :
					#Select the contact found
					elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
					
					#Long press on the contact found
					self.actions.long_press(elem1[0]).perform()
					print("Device: Long pressed on the contact found")
					sleep(2)
					
					#Click on Delete Contact
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Delete Contact')]").click()
					print("Device: Clicked on Delete Contact option")
					sleep(2)
					
					if int(del_flag) == 1:
						#Click on OK/Yes option
						elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'OK')]")
						elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Yes')]")
						if len(elem2) > 0:
							elem2[0].click()
							print("Device: Clicked on OK option")
						elif len(elem3) > 0:
							elem3[0].click()
							print("Device: Clicked on Yes option")
						
						for i in range(0, 10):
							elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact deleted')]")
							if len(elem) > 0:
								print("Device: Contact deleted successfully")
								sleep(2)
								status="PASS"
								break
							sleep(1)	
					else:					
						#Click on Cancel/No option
						elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Cancel')]")
						elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No')]")
						if len(elem2) > 0:
							elem2[0].click()
							print("Device: Clicked on Cancel option")
						elif len(elem3) > 0:
							elem3[0].click()
							print("Device: Clicked on No option")						
			else:
				print("Device: No Contacts to search and delete")
			
						
		elif int(dg_flag) == 1:	
			#Select the Group tab
			#self.driver.find_element_by_xpath("//android.view.View[@text='Group']").click()
			self.driver.find_element_by_id("ext-tab-4").click()
			print("Device: Navigated to the Group tab")
			sleep(2)
	
			#Check if Group tab is empty or not
			elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add groups:')]")
			if len(elem2) == 0:		
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
		
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
					
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) > 0:			
					print("Device: No Group is found with the given name")
					
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)
					status="PASS"
				elif len(elem) == 0 :
					#Select the Group found
					elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Group Name')]")
					
					#Long press on the Group found
					self.actions.long_press(elem1[0]).perform()
					print("Device: Long pressed on the Group found")
					sleep(2)
					
					#Click on Delete Group
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Delete Group')]").click()
					print("Device: Clicked on Delete Group option")
					sleep(2)
					
					if int(del_flag) == 1:
						#Click on OK/Yes option
						elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'OK')]")
						elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Yes')]")
						if len(elem2) > 0:
							elem2[0].click()
							print("Device: Clicked on OK option")
						elif len(elem3) > 0:
							elem3[0].click()
							print("Device: Clicked on Yes option")
						
						for i in range(0, 10):
							elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Group deleted')]")
							if len(elem) > 0:
								print("Device: Group deleted successfully")
								sleep(2)
								status="PASS"
								break
							sleep(1)	
					else:					
						#Click on Cancel/No option
						elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Cancel')]")
						elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No')]")
						if len(elem2) > 0:
							elem2[0].click()
							print("Device: Clicked on Cancel option")
						elif len(elem3) > 0:
							elem3[0].click()
							print("Device: Clicked on No option")
			else:
				print("Device: No Group to search and delete")
								
		elif int(fc_flag) == 1:	
			#Select the Favorite tab
			self.driver.find_element_by_xpath(".//*[@text='Favorite']").click()
			print("Device: Navigated to the Favorite tab")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Favorite Contacts')]")
			if len(elem) > 0:
				elem[0].click()
				print("Device: Clicked on Favorite Contacts tab")
				sleep(2)
				
				#Check if Favorite Contacts tab is empty or not
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add favorites:')]")
				if len(elem2) == 0:		
					#Input the name into search bar
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
					print("Device: Entered the given name in search bar")
					sleep(2)
			
					#Click Search/Done
					self.driver.press_keycode(66)
					print("Device: Clicked on search button")
					sleep(2)
						
					elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
					print(len(elem))
					if len(elem) > 0:			
						print("Device: No contact is found with the given name")
						
						#Click on the clear search option
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
						print("Device: Clicked on the clear search option")
						sleep(2)
						status="PASS"
					elif len(elem) == 0 :
						#Select the contact found
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, '"+name+"')]")
						
						#Long press on the contact found
						self.actions.long_press(elem1[1]).perform()
						print("Device: Long pressed on the contact found")
						sleep(2)
						
						#Click on Remove Favorite Contact
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Remove Favorite')]").click()
						print("Device: Clicked on Remove Favorite option")
						sleep(2)
				else:
					print("Device: No Contacts to search and delete")
			
			for i in range(0, 10):
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Favorite removed')]")
				if len(elem) > 0:
					print("Device: Favorite contact removed successfully")
					sleep(2)
					status="PASS"
					break
				sleep(1)		
		elif int(fg_flag) == 1:	
			#Select the Favorite tab
			self.driver.find_element_by_xpath(".//*[@text='Favorite']").click()
			print("Device: Navigated to the Favorite tab")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Favorite Groups')]")
			if len(elem) > 0:
				elem[0].click()
				print("Device: Clicked on Favorite Groups tab")
				sleep(2)
	
				#Check if Favorite Groups tab is empty or not
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add favorites:')]")
				if len(elem2) == 0:		
					#Input the name into search bar
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
					print("Device: Entered the given name in search bar")
					sleep(2)
			
					#Click Search/Done
					self.driver.press_keycode(66)
					print("Device: Clicked on search button")
					sleep(2)
						
					elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
					print(len(elem))
					if len(elem) > 0:			
						print("Device: No Group is found with the given name")
						
						#Click on the clear search option
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
						print("Device: Clicked on the clear search option")
						sleep(2)
						status="PASS"
					elif len(elem) == 0 :
						#Select the Group found
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, '"+name+"')]")
						
						#Long press on the Group found
						self.actions.long_press(elem1[1]).perform()
						print("Device: Long pressed on the Group found")
						sleep(2)
						
						#Click on Remove Favorite
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Remove Favorite')]").click()
						print("Device: Clicked on Remove Favorite option")
						sleep(2)
						
				else:
					print("Device: No Group to search and delete")
			
			for i in range(0, 10):
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Favorite removed')]")
				if len(elem) > 0:
					print("Device: Favorite contact removed successfully")
					sleep(2)
					status="PASS"
					break
				sleep(1)
		
		elif int(hc_flag) == 1:
			#Select the History tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			
			#Check whether the given name is already avaliable in the contacts
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
			if len(elem) > 0:
				#Long press on the history found
				self.actions.long_press(elem[0]).perform()
				print("Device: Long pressed on the history found")
				sleep(2)
				
				#Click on Delete History
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Delete')]").click()
				print("Device: Clicked on Delete history option")
				sleep(2)
				
				if int(del_flag) == 1:
					#Click on OK/Yes option
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'OK')]")
					elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Yes')]")
					if len(elem2) > 0:
						elem2[0].click()
						print("Device: Clicked on OK option")
					elif len(elem3) > 0:
						elem3[0].click()
						print("Device: Clicked on Yes option")
					
					for i in range(0, 10):
						elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'deleted')]")
						if len(elem) > 0:
							print("Device: History deleted successfully")
							sleep(2)
							status="PASS"
							break
						sleep(1)	
				else:					
					#Click on Cancel/No option
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Cancel')]")
					elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No')]")
					if len(elem2) > 0:
						elem2[0].click()
						print("Device: Clicked on Cancel option")
					elif len(elem3) > 0:
						elem3[0].click()
						print("Device: Clicked on No option")
					
			else:
				print("Device: No call in private call found to delete")
				sleep(2)
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return status	

	#================================================================================================================
	# Method Name	     :  edit_contact
	#
	# Description        :  This method will edit the contact.
	#
	# Arguments	         :  name
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [01-Aug-2018]
	#================================================================================================================
		
	def edit_contact(self,name, name_flag=0, new_name="User", avatar_flag=0, avatar="none", colour_flag=0, colour="none", favourite="null", save_flag=1):

		"""This keyword will edit the contact.
		
		Arguments are passed as given below.
		
		name_1
		
		"""
		#Initializing the status value	
		status="FAIL"
		
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Contact tab
		self.driver.find_element_by_id("ext-tab-3").click()
		print("Device: Navigated to the Contact tab")
		sleep(2)
	
		#Check if contacts tab is empty or not
		elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add contacts:')]")
		if len(elem2) == 0:		
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
		
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
				
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) > 0:			
				print("Device: No contact is found with the given name")
				
				#Click on the clear search option
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
				print("Device: Clicked on the clear search option")
				sleep(2)
			elif len(elem) == 0 :
				#Select the contact found
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				
				#Long press on the contact found
				self.actions.long_press(elem1[0]).perform()
				print("Device: Long pressed on the contact found")
				sleep(2)
				
				#Click on Contact Details
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()
				print("Device: Clicked on Contact Details option")
				sleep(2)
				
				#Change Name if necessary
				if int(name_flag) == 1:
					elem3=self.driver.find_elements_by_class_name("android.widget.EditText")
					if len(elem3) > 0:
						#Store the name
						elem5=elem3[0].get_attribute("text")
						print(elem5)
					
						if elem5 == new_name :
							print("Device: New name is same as previous name")
							sleep(2)							
						else:	
							#Clear the previous name
							elem3[0].clear()
							print("Device: Cleared the previous name")
							sleep(2)
							
							#Input the new name
							elem3[0].send_keys(new_name)
							print("Device: Inserted the new name")
							sleep(2)
							
							#Click OK/DONE button
							self.driver.press_keycode(66)
							print("Device: Clicked OK/DONE button")
							sleep(2)
				else:
					print("Device: No change in name")
										
				#Change Avatar if necessary
				if int(avatar_flag) == 1:
					#Select the avatar
					self.driver.find_element_by_xpath(".//*[@text='select avatar']").click()
					print ("Device: Clicked on avatar options")
					sleep(2)
					
					#Set avatar
					self.driver.find_element_by_xpath(".//*[@text='set avatar "+avatar+"']").click()
					print("Device: Selected "+avatar+" avatar")
					sleep(5)					
				else:
					print("No change in avatar")
					
				#Change Colour if necessary
				if int(colour_flag) == 1:
					#Select the colour
					self.driver.find_element_by_xpath(".//*[@text='set color "+colour+"']").click()	
					print("Device: Selected "+colour+" colour")
					sleep(2)				
				else:
					print("Device: No change in colour")
				
				#Add/Remove as favorite
				if favourite == "FAVORITE" :
					#Set the contact as favorite
					elem4=self.driver.find_elements_by_xpath(".//*[@text='FAVORITE']")
					if len(elem4) > 0:
						elem4[0].click()
						print("Device: Contact is made as favorite")
						sleep(2)
					else:
						print("Device: Contact is already a favorite")				
				elif favourite == "favorite" :
					#Remove the contact as favorite
					elem4=self.driver.find_elements_by_xpath(".//*[@text='favorite']")
					if len(elem4) > 0:
						elem4[0].click()
						print("Device: Contact is removed from favorite")
						sleep(2)
					else:
						print("Device: Contact is not in favorite")				
				else:
					print("Device: No change in favorite")
				
				if int(save_flag) == 1:					
					#Save the contact
					self.driver.find_element_by_xpath(".//*[@text='Save']").click()
					print("Device: Clicked Save button")
					sleep(1)
						
					#Check if network error pop-up
					error=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Data connection')]")
					if len(error) > 0:
						print("Device: Data connection is unavailable error is found")
						
						#Click OK option
						self.driver.find_element_by_xpath(".//*[@text='OK']").click()
						print("Device: Clicked on OK option")
						sleep(2)
						
						#Click on Cancel option
						self.driver.find_element_by_xpath(".//*[@text='Cancel']").click()
						print("Device: Clicked on Cancel option")
						sleep(2)
						
						#Click on Yes option
						self.driver.find_element_by_xpath(".//*[@text='Yes']").click()
						print("Device: Clicked on Yes option")
						sleep(2)
	
					for i in range(0, 10):
						elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact modified')]")
						if len(elem) > 0:
							print("Device: Contact modified successfully")
							sleep(2)
							status="PASS"
							break
						sleep(1)
				else:
					#Cancel the contact
					self.driver.find_element_by_xpath(".//*[@text='Cancel']").click()
					print("Device: Clicked Cancel button")
					sleep(2)
					
					#Click on Yes
					self.driver.find_element_by_xpath(".//*[@text='Yes']").click()
					print("Device: Clicked Yes button")
					sleep(2)										
		else:
			print("Device: No Contacts to search and modify")

		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return status	
		
	#================================================================================================================
	# Method Name	     :  edit_group
	#
	# Description        :  This method will edit the group.
	#
	# Arguments	         :  name
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [01-Aug-2018]
	#================================================================================================================
		
	def edit_group(self,name, name_flag=0, new_name="User", avatar_flag=0, avatar="none", colour_flag=0, colour="none", favourite="null",add_flag="0", add_members="['']", remove_flag="0", remove_members="['']", save_flag=1):

		"""This keyword will edit the group.
		
		Arguments are passed as given below.
		
		name_1
		
		"""
		#Initializing the status value	
		status="FAIL"
		
		add_members = ast.literal_eval(add_members)
		remove_members = ast.literal_eval(remove_members)

		#Open eptt app
		self.open_eptt_app()
		
		#Select the Group tab
		#self.driver.find_element_by_xpath("//android.view.View[@text='Group']").click()
		self.driver.find_element_by_id("ext-tab-4").click()
		print("Device: Navigated to the Groups tab")
		sleep(2)
	
		#Check if groups tab is empty or not
		elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add groups:')]")
		if len(elem2) == 0:		
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
		
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
				
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) > 0:			
				print("Device: No contact is found with the given name")
				
				#Click on the clear search option
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
				print("Device: Clicked on the clear search option")
				sleep(2)
			elif len(elem) == 0 :
				#Select the group found
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Group Name')]")
				
				#Long press on the group found
				self.actions.long_press(elem1[0]).perform()
				print("Device: Long pressed on the group_name found")
				sleep(2)
				
				#Click on Group Details
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Group details')]").click()
				print("Device: Clicked on Group Details option")
				sleep(2)
				
				#Change Name if necessary
				if int(name_flag) == 1:
					elem3=self.driver.find_elements_by_class_name("android.widget.EditText")
					if len(elem3) > 0:
						#Store the name
						elem5=elem3[0].get_attribute("text")
						print(elem5)
					
						if elem5 == new_name :
							print("Device: New name is same as previous name")
							sleep(2)							
						else:	
							#Clear the previous name
							elem3[0].clear()
							print("Device: Cleared the previous name")
							sleep(2)
							
							#Input the new name
							elem3[0].send_keys(new_name)
							print("Device: Inserted the new name")
							sleep(2)
							
							#Click OK/DONE button
							self.driver.press_keycode(66)
							print("Device: Clicked OK/DONE button")
							sleep(2)
				else:
					print("Device: No change in name")
										
				#Change Avatar if necessary
				if int(avatar_flag) == 1:
					#Select the avatar
					self.driver.find_element_by_xpath(".//*[@text='select avatar']").click()
					print ("Device: Clicked on avatar options")
					sleep(2)
					
					self.driver.find_element_by_xpath(".//*[@text='set avatar "+avatar+"']").click()
					print("Device: Selected "+avatar+" avatar")
					sleep(5)					
				else:
					print("No change in avatar")
					
				#Change Colour if necessary
				if int(colour_flag) == 1:
					#Select the colour
					self.driver.find_element_by_xpath(".//*[@text='set color "+colour+"']").click()	
					print("Device: Selected "+colour+" colour")
					sleep(2)						
				else:
					print("Device: No change in colour")
				
				#Add/Remove as favorite
				if favourite == "FAVORITE" :
					#Set the group as favorite
					elem4=self.driver.find_elements_by_xpath(".//*[@text='FAVORITE']")
					if len(elem4) > 0:
						elem4[0].click()
						print("Device: Group is made as favorite")
						sleep(2)
					else:
						print("Device: Group is already a favorite")				
				elif favourite == "favorite" :
					#Remove the group as favorite
					elem4=self.driver.find_elements_by_xpath(".//*[@text='favorite']")
					if len(elem4) > 0:
						elem4[0].click()
						print("Device: Group is removed from favorite")
						sleep(2)
					else:
						print("Device: Group is not in favorite")				
				else:
					print("Device: No change in favorite")
				
				#Add/Remove group members
				if int(add_flag) == 1:
					for i in range (len(add_members)):
						#Click on Add Members
						self.driver.find_element_by_xpath(".//*[@text='Add Members']").click()
						print("Device: Clicked on Add Members button")
						sleep(2)
						
						#Input the name into search bar
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(add_members[i])
						print("Device: Entered the given name in search bar")
						sleep(2)
		
						#Click Search/Done
						self.driver.press_keycode(66)
						print("Device: Clicked on search button")
						sleep(2)
		
						elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
						print(len(elem))
						if len(elem) > 0:
							print("Device: No Contact is found with the given name")
							
							#Click on the clear search option
							self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
							print("Device: Clicked on the clear search option")
							sleep(2)
						else:
							#select the contacts to be added in the group
							self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Name')]").click()	
							print("Device: Added a member")
							sleep(2)
							
							#Click Save button
							self.driver.find_element_by_xpath(".//*[@text='Save']").click()
							print("Device: Clicked Save button")
							sleep(2)
				elif int(remove_flag) == 1:
					#Remove the members
					for i in range (len(remove_members)):
						#select the contact to be removed from the group
						name=self.driver.find_elements_by_xpath(".//*[contains(@text, '"+remove_members[i]+"')]")	
						
						#Long press on the contact found
						self.actions.long_press(name[0]).perform()
						print("Device: Long pressed on the contact")
						sleep(2)
						
						#Click Remove Member button
						self.driver.find_element_by_xpath(".//*[@text='Remove Member']").click()
						print("Device: Clicked Remove Member button")
						sleep(2)
				
						#Click Yes option
						self.driver.find_element_by_xpath(".//*[@text='Yes']").click()
						print("Device: Clicked Yes option")
						sleep(2)
				
				elem6=self.driver.find_elements_by_xpath(".//*[@text='Back']")
				if len(elem6) > 0:
					#Click on Back option
					elem6[0].click()
					print("Device: Clicked on Back option")
					status="PASS"
					sleep(2)
				else:
					if int(save_flag) == 1:					
						#Save the contact
						self.driver.find_element_by_xpath(".//*[@text='Save']").click()
						print("Device: Clicked Save button")
						sleep(1)
							
						#Check if network error pop-up
						error=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Data connection')]")
						if len(error) > 0:
							print("Device: Data connection is unavailable error is found")
							
							#Click OK option
							self.driver.find_element_by_xpath(".//*[@text='OK']").click()
							print("Device: Clicked on OK option")
							sleep(2)
							
							#Click on Cancel option
							self.driver.find_element_by_xpath(".//*[@text='Cancel']").click()
							print("Device: Clicked on Cancel option")
							sleep(2)
							
							#Click on Yes option
							self.driver.find_element_by_xpath(".//*[@text='Yes']").click()
							print("Device: Clicked on Yes option")
							sleep(2)
		
						for i in range(0, 10):
							elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Group updated')]")
							if len(elem) > 0:
								print("Device: Group updated successfully")
								sleep(2)
								status="PASS"
								break
							sleep(1)
					else:
						#Cancel the contact
						self.driver.find_element_by_xpath(".//*[@text='Cancel']").click()
						print("Device: Clicked Cancel button")
						sleep(2)
						
						#Click on Yes
						self.driver.find_element_by_xpath(".//*[@text='Yes']").click()
						print("Device: Clicked Yes button")
						sleep(2)					
		else:
			print("Device: No Group to search and modify")
	
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return status	
		
	#================================================================================================================
	# Method Name	     :  add_favorite
	#
	# Description        :  This method will add group/contact as favorite.
	#
	# Arguments	         :  name
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [01-Aug-2018]
	#================================================================================================================
		
	def add_favorite(self,name, fc_flag=0, fg_flag=0):

		"""This keyword will add group/contact as favorite.
		
		Arguments are passed as given below.
		
		name_1
		
		"""
		#Initializing the status value	
		status="FAIL"
		
		nameLst=ast.literal_eval(name)
					
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Favorite tab
		self.driver.find_element_by_xpath(".//*[@text='Favorite']").click()
		print("Device: Navigated to the Favorite tab")
		sleep(2)
		
		if int(fc_flag) == 1:	
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Favorite Contacts')]")
			if len(elem) > 0:
				elem[0].click()
				print("Device: Clicked on Favorite Contacts tab")
				sleep(2)
				
				#Click on Add Contact option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Add Contact')]").click()
				print("Device: Clicked on Add Contact option")
				sleep(2)
				
				for i in range (len(nameLst)):								
					#Input the name into search bar
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(nameLst[i])
					print("Device: Entered the given name in search bar")
					sleep(2)
	
					#Click Search/Done
					self.driver.press_keycode(66)
					print("Device: Clicked on search button")
					sleep(2)
	
					elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
					print(len(elem))
					if len(elem) > 0:
						print("Device: No Group is found with the given name")
						
						#Click on the clear search option
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
						print("Device: Clicked on the clear search option")
						sleep(2)
						
						#Click on Back button
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
						print("Device: Clicked on Back button")
						sleep(2)
					else:
						#select the contacts to be added in the group
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Name')]").click()	
						print("Device: Added a member")
						sleep(2)
						
						#Click on the clear search option
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
						print("Device: Clicked on the clear search option")
						sleep(2)
						
				#Click Save button
				self.driver.find_element_by_xpath(".//*[@text='Save']").click()
				print("Device: Clicked Save button")
				sleep(2)
				
				for i in range(0, 10):
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Favorite saved')]")
					if len(elem2) > 0:
						print("Device: Favorite saved successfully")
						sleep(2)
						status="PASS"
						break
					sleep(1)
		elif int(fg_flag) == 1:
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Favorite Groups')]")
			if len(elem) > 0:
				elem[0].click()
				print("Device: Clicked on Favorite Groups tab")
				sleep(2)
				
				#Click on Add Group option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Add Group')]").click()
				print("Device: Clicked on Add Group option")
				sleep(2)
				
				for i in range (len(nameLst)):								
					#Input the name into search bar
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(nameLst[i])
					print("Device: Entered the given name in search bar")
					sleep(2)
	
					#Click Search/Done
					self.driver.press_keycode(66)
					print("Device: Clicked on search button")
					sleep(2)
	
					elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
					print(len(elem))
					if len(elem) > 0:
						print("Device: No Group is found with the given name")
						
						#Click on the clear search option
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
						print("Device: Clicked on the clear search option")
						sleep(2)
						
						#Click on Back button
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
						print("Device: Clicked on Back button")
						sleep(2)
					else:
						#select the contacts to be added in the group
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Name')]").click()	
						print("Device: Added a member")
						sleep(2)
						
						#Click on the clear search option
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
						print("Device: Clicked on the clear search option")
						sleep(2)
						
				#Click Save button
				self.driver.find_element_by_xpath(".//*[@text='Save']").click()
				print("Device: Clicked Save button")
				sleep(2)
				
				for i in range(0, 10):
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Favorite saved')]")
					if len(elem2) > 0:
						print("Device: Favorite saved successfully")
						sleep(2)
						status="PASS"
						break
					sleep(1)
				
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return status				
				
	#================================================================================================================
	# Method Name	     :  verify_favorite
	#
	# Description        :  This method will verifygroup/contact as favorite.
	#
	# Arguments	         :  nameLst
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [03-Aug-2018]
	#================================================================================================================
		
	def verify_favorite(self,nameLst, fc_flag=0, fg_flag=0):

		"""This keyword will verify group/contact as favorite.
		
		Arguments are passed as given below.
		
		['name_1','name_2',...]
		
		"""
		#Initializing the status value	
		status="FAIL"

		name = ast.literal_eval(nameLst)
		
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Favorite tab
		self.driver.find_element_by_xpath(".//*[@text='Favorite']").click()
		print("Device: Navigated to the Favorite tab")
		sleep(2)
		
		if int(fc_flag) == 1:	
			#Click on Favorite Contacts tab
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Favorite Contacts')]").click()
			print("Device: Clicked on Favorite Contacts tab")
			sleep(2)
		elif int(fg_flag) == 1:	
			#Click on Favorite Groups tab
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Favorite Groups')]").click()
			print("Device: Clicked on Favorite Groups tab")
			sleep(2)			

		elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add favorites')]")
		if len(elem) > 0:
			print("Device: No Contact is available to search")
		else:
			for i in range (len(name)):			
				#Search the contact	
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name[i])
				print("Device: Entered the given name in search bar")
				sleep(2)
				
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)				
				
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				if len(elem1) > 0:			
					print("Device: No contact is found with the given name")
					
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)
					temp="false"
					break
				elif len(elem1) == 0 :
					print("Device: Contact is found with the given name")
					
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)
					temp="true"
					
			if temp == "true":
				status="PASS"
			elif temp == "false":
				status="FAIL"
												
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		return status				

	#================================================================================================================
	# Method Name	     :  group_call
	#
	# Description        :  This method will initiate EPTT group call
	#
	# Arguments	         :  name,hold_time_arg
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [03-Aug-2018]
	#================================================================================================================			

	def group_call(self,name,hold_time_arg, favorite_flag=0):
	
		"""This keyword will Initiate an EPTT call.
		
		Arguments are passed as given below.
		
		name_1,hold_time_arg
		
		Here hold_time_arg is in seconds
		
		"""
		#Initializing the status value
		status="FAIL"			
		
		#Open eptt app
		self.open_eptt_app()
		
		if int(favorite_flag) == 0:
			#Select the Group tab
			#self.driver.find_element_by_xpath("//android.view.View[@text='Group']").click()
			self.driver.find_element_by_id("ext-tab-4").click()
			print("Device: Navigated to the Groups tab")
			sleep(2)
			
			#Check whether the given name is already available in the group
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '" + name + "')]")
			if len(elem) > 0:
				#Select the group for call
				#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
				elem[0].click()
				print("Device: Clicked on the group name")
				sleep(5)
									
				#Convert the hold time from seconds to mili-seconds
				hold_time = int(hold_time_arg)*1000
				print(hold_time)
				
				#Initiate EPTT Call
				#self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
				#sleep(2)
				
				#Click and hold the call button			
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
				if len(elem1) > 0:	
					#Initiate a EPTT call
					self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(hold_time).release().perform()
					print("Device: Initiated an EPTT group call")
					status="PASS"
					sleep(5)

					elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
					if len(elem2) > 0:
						elem2[0].click()
						print("Device: Clicked on Back button")
						sleep(2)	
													
			else:
				print("Device: Given name is not found in the group tab")
				status="FAIL"
				sleep(2)
		else:
			#Select the Favorite tab
			self.driver.find_element_by_xpath(".//*[@text='Favorite']").click()
			print("Device: Navigated to the Favorite tab")
			sleep(2)
			
			#Click on Favorite Groups tab
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Favorite Groups')]").click()
			print("Device: Clicked on Favorite Groups tab")
			sleep(2)
			
			#Check whether the given name is already available in the group
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '" + name + "')]")
			if len(elem) > 0:
				#Select the group for call
				#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
				elem[0].click()
				print("Device: Clicked on the group name")
				sleep(5)
									
				#Convert the hold time from seconds to mili-seconds
				hold_time = int(hold_time_arg)*1000
				print(hold_time)
				
				#Initiate EPTT Call
				#self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
				#sleep(2)
				
				#Click and hold the call button			
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
				if len(elem1) > 0:	
					#Initiate a EPTT call
					self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(hold_time).release().perform()
					print("Device: Initiated an EPTT group call")
					status="PASS"
					sleep(5)

					elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
					if len(elem2) > 0:
						elem2[0].click()
						print("Device: Clicked on Back button")
						sleep(2)	
													
			else:
				print("Device: Given name is not found in the group tab")
				status="FAIL"
				sleep(2)
			

		
		return status			
		
	#================================================================================================================
	# Method Name	     :  end_call
	#
	# Description        :  This method will terminate the call
	#
	# Arguments	         :  end_call_flag
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [03-Aug-2018]
	#================================================================================================================

	def end_call(self, end_call_flag=1):
	
		"""
		This keyword will terminate the call.				
		"""
		#Initializing the status value
		status="FAIL"

		if int(end_call_flag) == 1:	
			for i in range(0, 10000):
				sleep(5)
				elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No one')]")
				if len(elem3) > 0:
					#driver.find_element_by_xpath(".//*[contains(@text, 'END')]")
					#self.driver.tap([(250, 1500), ], None)
					self.driver.find_element_by_xpath(".//*[contains(@text, 'call end')]").click()
					sleep(2)
					print("Device: Successfully terminated the call")
					status="PASS"
					break
		else:
			#Wait for the call to be dropped
			timer=0
			for i in range(0, 10000):
				elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call ended')]")
				timer += 1
				if len(elem3) > 0:
					#print "Device: Call ended after {} seconds as the floor was kept idle.".format(int(timer-hold_time_arg))
					print("Device: Call is dropped after 10 seconds as there was no floor exchange")
					sleep(2)
					status="PASS"
					break
				sleep(1)

		#Wait for Back button to be visible
		for i in range(0, 500):
			elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
			if len(elem2) > 0:
				#Click on the Back Option
				elem2[0].click()
				print("Device: Clicked on Back option")
				sleep(2)
				break	

		#Click on the Back Button    
		self.driver.press_keycode(4)
		print("Device: Clicked on Back Button")
		sleep(2)			
				
		return status

	#================================================================================================================
	# Method Name	     :  history_call
	#
	# Description        :  This method will initiate EPTT call from history tab
	#
	# Arguments	         :  hold_time_arg
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [11-July-2018]
	#================================================================================================================			

	def history_call(self,hold_time_arg):
	
		"""This keyword will Initiate an EPTT call from history tab.
		
		Arguments are passed as given below.
		
		hold_time_arg
		
		Here hold_time_arg is in seconds
		
		"""
		#Initializing the status value
		status="FAIL"		
		
		#Open eptt app
		self.open_eptt_app()	
		
		#Select the History tab
		self.driver.find_element_by_id("ext-tab-1").click()
		print("Device: Navigated to the History tab")
		sleep(2)
		
		#Check whether the given name is already avaliable in the contacts
		elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
		if len(elem) > 0:
			#Select the Contact for IPA
			#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
			elem[0].click()
			print("Device: Clicked on the last private call")
			sleep(5)
									
			#Convert the hold time from seconds to mili-seconds
			hold_time = int(hold_time_arg)*1000
			print(hold_time)
			
			#Initiate EPTT Call
			#self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
			#sleep(2)
			
			#Click and hold the call button			
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
			if len(elem1) > 0:	
				#Initiate a EPTT call
				self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(hold_time).release().perform()
				print("Device: Initiated an EPTT call")
				status="PASS"
				sleep(5)								
		else:
			print("Device: No call in private call found")
			sleep(2)

		return status			
	
	#================================================================================================================
	# Method Name	     :  check_login
	#
	# Description        :  This method will check the login to ePTT app.
	#
	# Arguments	         :  
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [03-Aug-2018]
	#================================================================================================================

	def check_login(self):
	
		"""
		This keyword will check the login to ePTT app.				
		"""
		#Initializing the status value
		status="FAIL"
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		#Swipe down the notification bar
		size=self.driver.get_window_size()
		start_y = int(size["height"]*0.001)
		end_y   = int(size["height"]*0.40) 
		start_x = int(size["width"]*0.50)
		end_x = int(size["width"]*0.50)
		
		#Swipe the screen
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		print("Device: swiped down the notification bar")
		sleep(5)
		
		#Check the login status
		elem=self.driver.find_elements_by_xpath(".//*[@text='My Status:']")
		if len(elem) > 0:
			print("Device: ePTT client is logged in")
			sleep(2)
			status="PASS"
		else:
			print("Device: ePTT client is not logged in")
			sleep(2)
			status="FAIL"
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		
		return status

	#================================================================================================================
	# Method Name	     :  history_contact
	#
	# Description        :  This method will add the contact to EPTT App via history tab.
	#
	# Arguments	         :  name,avatar='set avatar none',colour='set color none',favorite='FAVORITE'
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [04-Aug-2018]
	#================================================================================================================

	def history_contact(self,name, avatar="none", colour="none", favourite="null"):
		
		"""This keyword will create a new contact.
		
		Arguments are passed as given below.
		
		desired_name,'avatar','colour' and 'favorite'
		
		colour = none(default),red,blue,green,purple,orange,lightblue
		
		favorite = null(default),FAVORITE
		
		avatar = none(default),construction,driver,front desk,notepad,worker,warehouse,airplane,delivery,envelope,housekeeping,ptt phone,telephone,supervisor,book,desktop pc,field services,laptop pc,room service,tree,car,dispatcher,flower,medical,security,truck
		
		Here avatar, colour ,favorite, status_falg and delete_flag are optional arguments.
		
		"""
		#Initializing the status value	
		status="FAIL"

		#Open eptt app
		self.open_eptt_app()
		
		#Select the History tab
		self.driver.find_element_by_id("ext-tab-1").click()
		print("Device: Navigated to the History tab")
		sleep(2)
		
		#Select the latest private call entry
		elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Private Call')]")
		if len(elem) > 0:
			#Select the Contact for IPA			
			elem[0].click()
			print("Device: Clicked on the last private call")
			sleep(5)
			
			#Click on Contact Details button
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()	
			print("Device: Clicked on Contact Details option")
			sleep(5)
			
			#Click on Add to contact option
			#self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'ext-element-698')]").click()
			self.driver.tap([(100, 2000), ], None)
			print("Device: Clicked on Add contacts option")
			sleep(5)
			
			elem1=self.driver.find_elements_by_class_name("android.widget.EditText")
			if len(elem1) > 0:
			
				#Clear the old name
				elem1[0].clear()
				print("Device: Cleared the old name")
				sleep(2)
				
				#Input the name
				elem1[0].send_keys(name)
				#self.driver.find_element_by_xpath(".//*[@resource-id='ext-element-4630']").send_keys(name)				
				print("Device: Inserted the name")
				sleep(2)
	
				#Click OK/DONE button
				self.driver.press_keycode(66)
				print("Device: Clicked OK/DONE button")
				sleep(2)
			
				#Select favorite
				if favourite == 'FAVORITE':
					#Set the contact as favorite
					self.driver.find_element_by_xpath(".//*[@text='unfavorite']").click()
					print("Device: Contact is made as favorite")
					sleep(2)
				
				#Select the colour
				self.driver.find_element_by_xpath(".//*[@text='set color "+colour+"']").click()	
				print("Device: Selected "+colour+" colour")
				sleep(2)
								
				#Select the avatar
				self.driver.find_element_by_xpath(".//*[@text='select avatar']").click()				
				print ("Device: Clicked on avatar options")
				sleep(2)
				
				#Set avatar
				self.driver.find_element_by_xpath(".//*[@text='set avatar "+avatar+"']").click()
				print("Device: Selected "+avatar+" avatar")
				sleep(5)
								
				#Save the contact
				self.driver.find_element_by_xpath(".//*[@text='Save']").click()
				print("Device: Clicked Save button")
					
				for i in range(0, 10):
					elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact created')]")
					elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'The phone number is invalid')]")
					if len(elem2) > 0:
						print("Device: Contact saved successfully")
						sleep(2)
						status="PASS"
					elif len(elem3) > 0:
						print("Devices: The phone number entered is invalid")
						
						#Click on OK
						self.driver.find_element_by_xpath(".//*[@text='OK']").click()
						print("Device: Clicked OK button")
						sleep(2)
						
						#Cancel the contact
						self.driver.find_element_by_xpath(".//*[@text='Cancel']").click()
						print("Device: Clicked Cancel button")
						sleep(2)
						
						#Click on Yes
						self.driver.find_element_by_xpath(".//*[@text='Yes']").click()
						print("Device: Clicked Yes button")
						sleep(2)						
					sleep(1)
				
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
				
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
				
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
				
		else:
			print("Device: No call in private call found")
			sleep(2)

		return status
		
	#================================================================================================================
	# Method Name	     :  cellular_call
	#
	# Description        :  This method will initiate EPTT call
	#
	# Arguments	         :  name,history_flag
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [13-Sep-2018]
	#================================================================================================================			

	def cellular_call(self,name, history_flag=0):
	
		"""This keyword will Initiate an cellular call from ePTT app.
		
		Arguments are passed as given below.
		
		name_1

		"""
		#Initializing the status value
		status="FAIL"		
		
		#Open eptt app
		self.open_eptt_app()
		
		if int(history_flag) == 0:	
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Check if contacts tab is empty or not
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'To add contacts:')]")
			if len(elem1) == 0:		
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
			
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
					
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem2))
				if len(elem2) > 0:			
					print("Device: No contact is found with the given name")
					
					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)
				elif len(elem2) == 0 :
					#Select the contact found
					elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
					
					#Long press on the contact found
					self.actions.long_press(elem3[0]).perform()
					print("Device: Long pressed on the contact found")
					sleep(2)
					
					#Click on Contact Details
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()
					print("Device: Clicked on Contact Details option")
					sleep(2)
					
					#Click on the Phone option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Phone')]").click()
					print("Device: Clicked on Phone option")
					sleep(5)
					
					#Click on the Audio Call button Button		
					self.driver.find_element_by_xpath(".//*[@content-desc='Call button']").click()
					print("Device: Clicked on Audio Call button Button")
					sleep(1)
					elem4 = self.driver.find_elements_by_xpath(".//*[contains(@text,'Dialing')]")
					if len(elem4)>0:
						print("Device: Audio Call initiated") 
						status="PASS"
					else:
						print("Device: Failed to initiate Audio Call")
		elif int(history_flag) == 1:
			#Select the History tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			
			#Check whether the given name is already avaliable in the contacts
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
			if len(elem1) > 0:
				#Select the Contact for IPA
				#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
				elem1[0].click()
				print("Device: Clicked on the last private call")
				sleep(5)
					
				#Click on Contact Details button
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()	
				print("Device: Clicked on Contact Details option")
				sleep(5)
				
				#Click on the Phone option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Phone')]").click()
				print("Device: Clicked on Phone option")
				sleep(5)
				
				#Click on the Audio Call button Button		
				self.driver.find_element_by_xpath(".//*[@content-desc='Call button']").click()
				print("Device: Clicked on Audio Call button Button")
				sleep(1)
				elem4 = self.driver.find_elements_by_xpath(".//*[contains(@text,'Dialing')]")
				if len(elem4)>0:
					print("Device: Audio Call initiated") 
					status="PASS"
				else:
					print("Device: Failed to initiate Audio Call")
				
				
		return status			

	#================================================================================================================
	# Method Name	     :  terminate_call
	#
	# Description        :  This method will terminate a call.
	#
	# Arguments	         :  serial
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [13-Sep-2018]
	#================================================================================================================
		
	def terminate_call(self):

		"""This Keyword will terminate the established call on the device.
		
		Make sure the serial  passed in the way mentioned below.
		
		serial_1
		"""	
		
		#Initializing the status value
		status="FAIL"
		
		#Terminate the call
		self.driver.press_keycode(6)
		print("Successfully terminated the call")
		sleep(2)
		status="PASS"
		
		return status 
		
	#================================================================================================================
	# Method Name	     :  receive_call
	#
	# Description        :  This method will receive a call.
	#
	# Arguments	         :  serial
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [13-Sep-2018]
	#================================================================================================================
					
	def receive_call(self):

		#Initializing the status value
		status="FAIL"
		#Check for the incoming call
		
		for i in range(0, 500):
			elem1 = self.driver.find_elements_by_xpath(".//*[contains(@content-desc,'Incoming')]")
			if len(elem1)>0:				
				#Received the incoming call
				size=self.driver.get_window_size()
				start_y = int(size["height"] * 0.80)
				end_y   = int(size["height"]* 0.80)
				start_x = int(size["width"]* 0.20)
				end_x = int(size["width"]* 0.60)
				self.driver.swipe(start_x, start_y, end_x, end_y, None)
				sleep(2)
				print("Device: Received the incoming call")
				print("Call is being received")
				status="PASS"
				break
			else:
				print("Device: Checking for the incoming call")
			sleep(5)
			
		sleep(5)
		return status 

	#================================================================================================================
	# Method Name	     :  verify_MCA
	#
	# Description        :  This method will verify the received MCA
	#
	# Arguments	         :  option
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [13-Sep-2018]
	#================================================================================================================			

	def verify_MCA(self,option):
	
		"""This keyword will verify the received MCA
		
		Arguments are passed as given below.
		
		option(Reply or Not now)
		
		"""
		#Initializing the status value	
		status="FAIL"
					
		#Open eptt app
		self.open_eptt_app()

		#Check for MCA
		for i in range(0, 10000):
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Missed Call')]")
			#elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
			if len(elem1) > 0:
				#Click on the IPA received
				print("Device: Clicked on received MCA")
				status="PASS"
				sleep(2)
							
				if option == "Reply" :
					#Click on Reply
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Reply')]").click()
					print("Device: Clicked on Reply option")
					sleep(2)
					
					#Click and hold the call button			
					elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
					if len(elem1) > 0:	
						#Initiate a EPTT call
						self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(20000).release().perform()
						print("Device: Initiated an EPTT call")
						sleep(5)
						
						for i in range (0, 2):
							elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
							if len(elem2) > 0:
								elem2[0].click()
								print("Device: Clicked on Back button")
								sleep(2)
					
				elif option == "Not now" :
					#Click on Not now
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Not now')]").click()
					print("Device: Clicked on Not now option")
					sleep(2)					
			
			break			
	
		return status	

	#================================================================================================================
	# Method Name	     :  eptt_about
	#
	# Description        :  This method will return the about details of the eptt app.
	#
	# Arguments	         :  
	#
	# Returns	         :  
	#
	# Date Modified      :  Newly Added [14-Sep-2018]
	#================================================================================================================			

	def eptt_about(self):
	
		"""This keyword will return the about details of the eptt app.
				
		"""
		#Initializing the status value	
		status="FAIL"
					
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Menu option
		self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
		print("Device: Navigated to the Menu option")
		sleep(5)
		
		#Select the About option
		self.driver.find_element_by_xpath(".//*[@text='About']").click()
		#self.driver.find_element_by_id("ext-element-617").click()
		#self.driver.find_element_by_xpath(".//*[contains(@text, 'About')]").click()
		#self.driver.find_element_by_id("ext-element-636").click()		
		print("Device: Navigated to the About option")
		sleep(2)
		
		#Store the about details
		status = self.driver.find_element_by_xpath(".//*[contains(@text, 'PTT ')]").get_attribute("text")
		
		#Click Back option
		self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
		print("Device: Clicked on Back button")
		sleep(2)
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
			
		return str(status)

	#================================================================================================================
	# Method Name	     :  eptt_number
	#
	# Description        :  This method will return the eptt number.
	#
	# Arguments	         :  
	#
	# Returns	         :  number
	#
	# Date Modified      :  Newly Added [14-Sep-2018]
	#================================================================================================================
			
	def eptt_number(self):
		
		"""This method will return the eptt number.
		
		"""
		#Initializing the counter value	
		status = "FAIL"
					
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Menu option
		self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
		print("Device: Navigated to the Menu option")
		sleep(5)
		
		#Select the Settings option
		self.driver.find_element_by_xpath(".//*[@text='Settings']").click()
		print("Device: Navigated to the Settings option")
		sleep(2)
				
		# Identifying the Screen coordinates
		size=self.driver.get_window_size()
		print(size)
		end_y = '700'
		start_y = '1700'
		end_x = '400'
		start_x = '400'

		print(start_x,start_y,end_x,end_y)

		#Scroll down till the Capacity option is found
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		sleep(2)
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		sleep(2)
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		sleep(5)
		
		status = self.driver.find_element_by_xpath(".//*[contains(@text, '-')]").get_attribute("text")
			
		#Click on BACK
		self.driver.press_keycode(4)
		print("Device: Clicked on BACK button")
		sleep(2)
		
		#Click on HOME
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		
		return str(status)

	#================================================================================================================
	# Method Name	     :  eptt_sorting
	#
	# Description        :  This method will sort the entry.
	#
	# Arguments	         :  history,contact,option
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [14-Sep-2018]
	#================================================================================================================
			
	def eptt_sorting(self, history=0, contact=0, availability=0, option=1):
		
		"""This method will sort the entry.
		
		"""
		#Initializing the counter value	
		status = "FAIL"
					
		#Open eptt app
		self.open_eptt_app()
		
		if int(availability) == 0:
			#Select the Menu option
			self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
			print("Device: Navigated to the Menu option")
			sleep(5)
			
			#Select the Settings option
			self.driver.find_element_by_xpath(".//*[@text='Settings']").click()
			print("Device: Navigated to the Settings option")
			sleep(2)
					
			# Identifying the Screen coordinates
			size=self.driver.get_window_size()
			print(size)
			end_y = '700'
			start_y = '1700'
			end_x = '400'
			start_x = '400'
	
			print(start_x,start_y,end_x,end_y)
	
			#Scroll down till the Capacity option is found
			self.driver.swipe(start_x, start_y, end_x, end_y, None)
			sleep(2)
			self.driver.swipe(start_x, start_y, end_x, end_y, None)
			sleep(2)
			self.driver.swipe(start_x, start_y, end_x, end_y, None)
			sleep(5)
				
			if int(contact) == 1:
				#Click on Contact Sorting option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Sorting')]").click()
				print("Device: Clicked on Contact Sorting option")
				sleep(5)
				
				if int(option) == 1:
					#Click on sort by availability option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Availability')]").click()
					print("Device: Clicked on sort by Availability option")
					sleep(2)
				elif int(option) == 2:
					#Click on sort by Alphabetical option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Alphabetical')]").click()
					print("Device: Clicked on sort by Alphabetical option")
					sleep(2)
				
				#Click on OK option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'OK')]").click()
				print("Device: Clicked on sort by OK option")
				sleep(2)
				status="PASS"
			elif int(history) == 1:
				#Click on History Sorting option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'History Sorting')]").click()
				print("Device: Clicked on History Sorting option")
				sleep(5)
				
				if int(option) == 1:
					#Click on sort by newest on top option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'top')]").click()
					print("Device: Clicked on sort by newest on top option")
					sleep(2)
				elif int(option) == 2:
					#Click on sort by newest on bottom option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'bottom')]").click()
					print("Device: Clicked on sort by newest on bottom option")
					sleep(2)
				
				#Click on OK option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'OK')]").click()
				print("Device: Clicked on sort by OK option")
				sleep(2)
				status="PASS"
		elif int(availability) == 1:
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			if int(option) == 1:
				elem = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Hide offline Contacts')]")
				
				#Hide offline Contacts
				if len(elem) > 0:
					elem[0].click()
					print("Device: Clicked on Hide offline Contacts option")
					sleep(2)
					status="PASS"
				else:
					print("Device: Already the offline contacts have been hidden")
					sleep(2)
					status="PASS"
			elif int(option) == 2:
				elem = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Show offline Contacts')]")
				
				#Show offline Contacts
				if len(elem) > 0:
					elem[0].click()
					print("Device: Clicked on Hide Show Contacts option")
					sleep(2)
					status="PASS"
				else:
					print("Device: Already the offline contacts are not hidden")
					sleep(2)
					status="PASS"			
		
		#Click on BACK
		self.driver.press_keycode(4)
		print("Device: Clicked on BACK button")
		sleep(2)
		
		#Click on HOME
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		
		return status
		
	#================================================================================================================
	# Method Name	     :  eptt_setting
	#
	# Description        :  This method will do few settings.
	#
	# Arguments	         :  default,logout,login,option
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [14-Sep-2018]
	#================================================================================================================
			
	def eptt_setting(self,option, default=0, logout=0, login=0):
		
		"""This method will do few settings.
		
		"""
		#Initializing the counter value	
		status = "FAIL"
		
		if int(login) == 0:
			
			#Open eptt app
			self.open_eptt_app()
			
			#Select the Menu option
			self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
			print("Device: Navigated to the Menu option")
			sleep(5)
			
			#Select the Settings option
			self.driver.find_element_by_xpath(".//*[@text='Settings']").click()
			print("Device: Navigated to the Settings option")
			sleep(2)
					
			# Identifying the Screen coordinates
			size=self.driver.get_window_size()
			print(size)
			end_y = '700'
			start_y = '1700'
			end_x = '400'
			start_x = '400'
	
			print(start_x,start_y,end_x,end_y)
	
			#Scroll down till the Capacity option is found
			self.driver.swipe(start_x, start_y, end_x, end_y, None)
			sleep(2)
			self.driver.swipe(start_x, start_y, end_x, end_y, None)
			sleep(2)
			self.driver.swipe(start_x, start_y, end_x, end_y, None)
			sleep(5)
				
			if int(default) == 1:
				#Click on Restore Defaults option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Restore Defaults')]").click()
				print("Device: Clicked on Restore Defaults option")
				sleep(5)
				
				if option == "Yes":
					#Click on Yes option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Yes')]").click()
					print("Device: Clicked on sort by Yes option")
					sleep(5)
				elif option == "No":
					#Click on No option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'No')]").click()
					print("Device: Clicked on No option")
					sleep(2)
				
				#Click on BACK
				self.driver.press_keycode(4)
				print("Device: Clicked on BACK button")
				sleep(2)
				status="PASS"
				
				#Click on HOME
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			elif int(logout) == 1:
				#Click on logout option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Logout')]").click()
				print("Device: Clicked on Logout option")
				sleep(5)
				
				if option == "Yes":
					#Click on Yes option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Yes')]").click()
					print("Device: Clicked on sort by Yes option")
					sleep(5)
				elif option == "No":
					#Click on No option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'No')]").click()
					print("Device: Clicked on No option")
					sleep(2)
				
					#Click on BACK
					self.driver.press_keycode(4)
					print("Device: Clicked on BACK button")
					sleep(2)
		
					#Click on HOME
					self.driver.press_keycode(3)
					print("Device: Clicked on Home Button")
					sleep(2)
	
				status="PASS"					
		elif int(login) == 1:
			
			#Open eptt app
			self.open_eptt_app()
			
			for i in range(0, 50):
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Login')]")
				if len(elem1) > 0:
					#Click on Yes option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Yes')]").click()
					print("Device: Clicked on Yes option")
					sleep(15)
					break
			
			elem=self.driver.find_elements_by_xpath(".//*[@text='Menu']")
			if len(elem)>0:
				status="PASS"
				
			#Click on HOME
			self.driver.press_keycode(3)
			print("Device: Clicked on Home Button")
			sleep(2)	
		
		return status
		
	#================================================================================================================
	# Method Name	     :  adhoc_call
	#
	# Description        :  This method will initiate adhoc call
	#
	# Arguments	         :  nameLst,hold_time_arg
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [18-Sep-2018]
	#================================================================================================================			

	def adhoc_call(self,nameLst,hold_time_arg, manual_dial=0, DND=0):
	
		"""This keyword will Initiate an adhoc call.
		
		Arguments are passed as given below.
		
		['name_1','name_2'...],hold_time_arg
		
		Here hold_time_arg is in seconds
		
		"""
		#Initializing the status value
		status="FAIL"	
		user_name = ast.literal_eval(nameLst)	
		
		#Open eptt app
		self.open_eptt_app()
		
		#Convert the hold time from seconds to mili-seconds
		hold_time = int(hold_time_arg)*1000
		print(hold_time)
		
		if int(manual_dial) == 0:	
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(user_name[0])	
			print("Device: Entered the given name in search bar")
			sleep(2)
		
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0 :
				#Select the Contact for IPA
				#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
								
				#Initiate EPTT Call
				#self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
				#sleep(2)
				
				for i in range (len(user_name[1:])):
					#Click on add participant option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'add participant')]").click()
					print("Device: Clicked on add participant option")
					sleep(2)
					
					#Input the name into search bar
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(user_name[i+1])	
					print("Device: Entered the given name in search bar")
					sleep(2)
				
					#Click Search/Done
					self.driver.press_keycode(66)
					print("Device: Clicked on search button")
					sleep(2)
					
					elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
					if len(elem) == 0 :
						#Select the Contact
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
						elem1[0].click()
						print("Device: Clicked on the contact name")
						sleep(5)
						
						#Click Save button
						self.driver.find_element_by_xpath(".//*[@text='Save']").click()
						print("Device: Clicked Save button")
						sleep(2)
					else:
						#Click on the clear search option
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
						print("Device: Clicked on the clear search option")
						sleep(2)
						
						#Click on the Back Option
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
						print("Device: Clicked on Back option")
						sleep(2)
										
				if int(DND) == 0:				
					#Click and hold the call button			
					elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
					if len(elem1) > 0:	
						#Initiate a EPTT call
						self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(hold_time).release().perform()
						print("Device: Initiated an EPTT call")
						status="PASS"
						sleep(5)
				elif int(DND) == 1:
					#Click and hold the call button			
					elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
					if len(elem1) > 0:	
						#Initiate a EPTT call
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
						print("Device: Clicked on the EPTT call")
						sleep(5)
		
						#Check for the information message
						elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Information')]")
						if len(elem2) > 0:
							print("Device: Information:'The Contact you are trying to call is in 'Do Not Disturb' status. Please try again later.'")
							sleep(5)
							#Click on the Back Button    
							self.driver.press_keycode(4)
							print("Device: Clicked on Back Button")
							sleep(2)
							status="PASS"	
					else:										
						#Click on the Back Option
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
						print("Device: Clicked on Back option")
						sleep(2)
			else:
				print("Device: No contact is found with the given name")
					
				#Click on the clear search option
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
				print("Device: Clicked on the clear search option")
				sleep(2)

		elif int(manual_dial) == 1:	
			#Select the Menu option
			self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
			print("Device: Navigated to the Menu option")
			sleep(2)
			
			#Select the Manual dial option
			self.driver.find_element_by_xpath(".//*[@text='Manual Dial']").click()
			print("Device: Navigated to the Manual Dial option")
			sleep(2)
			
			elem1=self.driver.find_elements_by_class_name("android.widget.EditText")
			if len(elem1) > 0:
				#Input the number
				name = str(user_name[0]).replace("-","")
				elem1[0].send_keys(name)
				#self.driver.find_element_by_xpath(".//*[@resource-id='ext-element-4630']").send_keys(name)				
				print("Device: Inserted the number")
				sleep(2)
	
				#Click OK/DONE button
				self.driver.press_keycode(66)
				print("Device: Clicked OK/DONE button")
				sleep(2)

				#Select the PTT Call option
				self.driver.find_element_by_xpath(".//*[@text='PTT Call']").click()
				print("Device: Navigated to the PTT Call option")
				sleep(2)	
				
				for i in range (len(user_name[1:])):
					#Click on add participant option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'add participant')]").click()
					print("Device: Clicked on add participant option")
					sleep(2)
					
					#Input the name into search bar
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(user_name[i+1])	
					print("Device: Entered the given name in search bar")
					sleep(2)
				
					#Click Search/Done
					self.driver.press_keycode(66)
					print("Device: Clicked on search button")
					sleep(2)
					
					elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
					if len(elem) == 0 :
						#Select the Contact
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
						elem1[0].click()
						print("Device: Clicked on the contact name")
						sleep(5)
						
						#Click Save button
						self.driver.find_element_by_xpath(".//*[@text='Save']").click()
						print("Device: Clicked Save button")
						sleep(2)
					else:
						#Click on the clear search option
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
						print("Device: Clicked on the clear search option")
						sleep(2)
						
						#Click on the Back Option
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
						print("Device: Clicked on Back option")
						sleep(2)
												
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'number')]")
				elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
				if len(elem2) > 0:
					print("Devices: The phone number entered is invalid")
					
					#Click on OK
					self.driver.find_element_by_xpath(".//*[@text='OK']").click()
					print("Device: Clicked OK button")
					sleep(2)
					
					#Click on Back
					self.driver.find_element_by_xpath(".//*[@text='Back']").click()
					print("Device: Clicked Back button")
					sleep(2)
				elif len(elem3) > 0:
					if int(DND) == 0:
						#Initiate a EPTT call
						self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]")).wait(hold_time).release().perform()
						print("Device: Initiated an EPTT call")
						
						elem4=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call cannot complete')]")
						if len(elem4) > 0:
							print("Device: Call cannot complete, not a PTT subscriber.")
							
							#Click on OK
							self.driver.find_element_by_xpath(".//*[@text='OK']").click()
							print("Device: Clicked OK button")
							sleep(2)
						
							#Click on Back
							self.driver.find_element_by_xpath(".//*[@text='Back']").click()
							print("Device: Clicked Back button")
							sleep(2)
						
							#Click on Back
							self.driver.find_element_by_xpath(".//*[@text='Back']").click()
							print("Device: Clicked Back button")
							sleep(2)						
						else:	
							status="PASS"
					elif int(DND) ==1:
						#Click and hold the call button			
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Call')]")
						if len(elem1) > 0:	
							#Initiate a EPTT call
							self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
							print("Device: Clicked on the EPTT call")
							sleep(5)
			
							#Check for the information message
							elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Information')]")								
							if len(elem2) > 0:
								print("Device: Information:'The Contact you are trying to call is in 'Do Not Disturb' status. Please try again later.'")
								sleep(5)
								#Click on the Back Button    
								self.driver.press_keycode(4)
								print("Device: Clicked on Back Button")
								sleep(2)
								status="PASS"								
						else:										
							#Click on the Back Option
							self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
							print("Device: Clicked on Back option")
							sleep(2)
					
		return status			

	#================================================================================================================
	# Method Name	     :  eptt_name
	#
	# Description        :  This method will return the eptt name.
	#
	# Arguments	         :  
	#
	# Returns	         :  name
	#
	# Date Modified      :  Newly Added [14-Sep-2018]
	#================================================================================================================
			
	def eptt_name(self, new_name="abc", option=0):
		
		"""This method will return the eptt name.
		
		"""
		#Initializing the counter value	
		status = "FAIL"
					
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Menu option
		self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
		print("Device: Navigated to the Menu option")
		sleep(5)
		
		#Select the Settings option
		self.driver.find_element_by_xpath(".//*[@text='Settings']").click()
		print("Device: Navigated to the Settings option")
		sleep(2)
				
		# Identifying the Screen coordinates
		size=self.driver.get_window_size()
		print(size)
		end_y = '700'
		start_y = '1700'
		end_x = '400'
		start_x = '400'

		print(start_x,start_y,end_x,end_y)

		#Scroll down till the Capacity option is found
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		sleep(2)
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		sleep(2)
		self.driver.swipe(start_x, start_y, end_x, end_y, None)
		sleep(5)
		
		#Click on Display Name option
		self.driver.find_element_by_xpath(".//*[contains(@text, 'Display Name')]").click()
		print("Device: Clicked on Display Name option")
		sleep(5)
		
		status = self.driver.find_element_by_xpath(".//*[contains(@class, 'android.widget.EditText')]").get_attribute("text")
		
		if int(option) == 1:
			#Clear the old name
			self.driver.find_element_by_xpath(".//*[contains(@class, 'android.widget.EditText')]").clear()
			print("Device: Cleared the old name")
			sleep(2)
			
			#Insert new name
			self.driver.find_element_by_xpath(".//*[contains(@class, 'android.widget.EditText')]").send_keys(new_name)
			print("Device: Inserted new name")
			sleep(2)
			
			#Click OK/DONE button
			self.driver.press_keycode(66)
			print("Device: Clicked OK/DONE button")
			sleep(2)
			
			#Click on save option
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Save')]").click()
			print("Device: Clicked on Save option")
			sleep(10)
			
			#Click on Display Name option
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Display Name')]").click()
			print("Device: Clicked on Display Name option")
			sleep(5)
			
			status2 = self.driver.find_element_by_xpath(".//*[contains(@class, 'android.widget.EditText')]").get_attribute("text")
			
		#Click on BACK
		self.driver.press_keycode(4)
		print("Device: Clicked on BACK button")
		sleep(2)
		
		#Click on HOME
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		
		if int(option) == 1:		
			return str(status), str(status2)
		else:
			return str(status)

	#================================================================================================================
	# Method Name	     :  eptt_tutorial
	#
	# Description        :  This method will open the tutorial screen on eptt app.
	#
	# Arguments	         :  
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [25-Sep-2018]
	#================================================================================================================
		
	def eptt_tutorial(self):

		"""This method will open the tutorial screen on eptt app.		
		"""
		#Initializing the counter value	
		status = "FAIL"
					
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Menu option
		self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
		print("Device: Navigated to the Menu option")
		sleep(5)
		
		#Select the Tutorial option
		self.driver.find_element_by_xpath(".//*[@text='Tutorial']").click()
		print("Device: Navigated to the Tutorial option")
		sleep(10)
		
		status = "PASS"
		
		#Swipe the screen
		self.driver.swipe(700, 700, 200, 700, None)
		print("Device: swiped to right")
		sleep(2)
		
		#Swipe the screen
		self.driver.swipe(200, 700, 700, 700, None)
		print("Device: swiped to left")
		sleep(2)
		
		return status
		
	#================================================================================================================
	# Method Name	     :  history_details
	#
	# Description        :  This method will give the time stamp and the user details.
	#
	# Arguments	         :  
	#
	# Returns	         : 
	#
	# Date Modified      :  Newly Added [26-Sep-2018]
	#================================================================================================================			

	def history_details(self, pc_flag=0, gc_flag=0, ipa_flag=0, mca_flag=0):
	
		"""This method will give the time stamp and the user details.		
		"""
		#Initializing the status value	
		status="FAIL"
		time=""
		name=""
		number=""
					
		#Open eptt app
		self.open_eptt_app()
		
		#Select the History tab
		self.driver.find_element_by_id("ext-tab-1").click()
		print("Device: Navigated to the History tab")
		sleep(5)
		
		if int(pc_flag)==1:						
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Private Call')]")
			if len(elem) > 0:
				status="PASS"
			
				#Store the call details
				time = elem[0].get_attribute("text")
			
				#Click on the first entry for private call
				elem[0].click()
				print("Device: Clicked on the latest entry for private call")
				sleep(2)
				
				#Click on Contact Details
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()
				print("Device: Clicked on Contact Details option")
				sleep(2)
				
				elem1=self.driver.find_elements_by_class_name("android.widget.EditText")
				if len(elem1) > 0:
					#Store the display name
					name = elem1[0].get_attribute("text")
					number = elem1[1].get_attribute("text")
				
				#Click on Back option
				for i in range (0, 2):
					elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
					if len(elem2) > 0:
						elem2[0].click()
						print("Device: Clicked on Back button")
						sleep(2)								
		
		elif int(gc_flag)==1:
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Group Call')]")
			if len(elem) > 0:
				status="PASS"
			
				#Store the call details
				time = elem[0].get_attribute("text")
		
		elif int(ipa_flag)==1:
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Instant Personal Alert')]")
			if len(elem) > 0:
				status="PASS"
			
				#Store the call details
				time = elem[0].get_attribute("text")
			
				#Click on the first entry for private call
				elem[0].click()
				print("Device: Clicked on the latest entry for private call")
				sleep(2)
				
				#Click on Contact Details
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()
				print("Device: Clicked on Contact Details option")
				sleep(2)
				
				elem1=self.driver.find_elements_by_class_name("android.widget.EditText")
				if len(elem1) > 0:
					#Store the display name
					name = elem1[0].get_attribute("text")
					number = elem1[1].get_attribute("text")
				
				#Click on Back option
				for i in range (0, 2):
					elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
					if len(elem2) > 0:
						elem2[0].click()
						print("Device: Clicked on Back button")
						sleep(2)
		
		elif int(mca_flag)==1:
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Missed Private Call')]")
			if len(elem) > 0:
				status="PASS"
			
				#Store the call details
				time = elem[0].get_attribute("text")
			
				#Click on the first entry for private call
				elem[0].click()
				print("Device: Clicked on the latest entry for private call")
				sleep(2)
				
				#Click on Contact Details
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Contact Details')]").click()
				print("Device: Clicked on Contact Details option")
				sleep(2)
				
				elem1=self.driver.find_elements_by_class_name("android.widget.EditText")
				if len(elem1) > 0:
					#Store the display name
					name = elem1[0].get_attribute("text")
					number = elem1[1].get_attribute("text")
				
				#Click on Back option
				for i in range (0, 2):
					elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
					if len(elem2) > 0:
						elem2[0].click()
						print("Device: Clicked on Back button")
						sleep(2)

		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		if 	int(gc_flag)==1:
			return	status, str(time)
		else:	
			return	status, str(time), str(name), str(number)
		
	#================================================================================================================
	# Method Name	     :  native_contact
	#
	# Description        :  This method will add the contact to native phone book.
	#
	# Arguments	         :  name,number
	#
	# Returns	         :  PASS/FAIL/The phone number entered already exists
	#
	# Date Modified      :  Newly Added [28-Sep-2018]
	#================================================================================================================

	def native_contact(self,name,number):
		
		"""This keyword will create a new contact to native phone book.
		
		Arguments are passed as given below.
		
		desired_name,desired_phonenumber,
		
		"""
		#Initializing the status value	
		status="FAIL"
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		
		#Click on the Phone app
		self.driver.find_element_by_xpath(".//*[@text='Phone']").click()
		print("Device: Clicked on Phone Button")
		sleep(5)
		
		# #Open Settings APP with Airplane Mode activity
		# self.driver.start_activity("com.samsung.android.contacts", "com.android.contacts.DialtactsContactsEntryActivity")
		# sleep(10)
		
		elem=self.driver.find_elements_by_xpath(".//*[@text='CONTACTS']")
		if len(elem)>0:
			elem[0].click()
			print("Device: Clicked on CONTACTS tab")
			sleep(2)
		else:
			#Click on the Back Button    
			self.driver.press_keycode(4)
			print("Device: Clicked on Back Button")
			sleep(2)
			
			self.driver.find_element_by_xpath(".//*[@text='CONTACTS']").click()
			print("Device: Clicked on CONTACTS tab")
			sleep(2)
		
		#Click on Create Create contact option
		self.driver.find_element_by_xpath(".//*[@text='Create contact']").click()
		print("Device: Clicked on Create contact option")
		sleep(2)
		
		elem=self.driver.find_elements_by_class_name("android.widget.EditText")
				
		#Insert the name
		#self.driver.find_element_by_xpath(".//*[@text='Name']").send_keys(name)
		elem[0].send_keys(name)
		print("Device: Inserted the name")
		sleep(2)
		
		#Click on the Back Button    
		self.driver.press_keycode(4)
		print("Device: Clicked on Back Button")
		sleep(2)
		
		#Insert the number
		#self.driver.find_element_by_xpath(".//*[@text='Phone']").send_keys(number)
		elem[2].send_keys(number)
		print("Device: Inserted the number")
		sleep(2)
		
		#Click on the Back Button    
		self.driver.press_keycode(4)
		print("Device: Clicked on Back Button")
		sleep(2)
		
		#Save the contact
		self.driver.find_element_by_xpath(".//*[@text='SAVE']").click()
		print("Device: Clicked on SAVE option")
		sleep(2)
		
		elem1=self.driver.find_elements_by_xpath(".//*[@text='SAVE ANYWAY']")
		if len(elem1)>0:
			#Click on SAVE ANYWAY option
			elem1[0].click()
		
		status="PASS"
		
		#Click on the Back Button    
		self.driver.press_keycode(4)
		print("Device: Clicked on Back Button")
		sleep(2)
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)
		
		return status

	#================================================================================================================
	# Method Name	     :  import_contact
	#
	# Description        :  This method will imported the contact to EPTT App.
	#
	# Arguments	         :  name,number,avatar='set avatar none',colour='set color none',favorite='FAVORITE',status_flag="0",delete_flag="0"
	#
	# Returns	         :  PASS/FAIL/The phone number entered already exists
	#
	# Date Modified      : Newly Added [28-Sep-2018]
	#================================================================================================================

	def import_contact(self,name,number, avatar="none", colour="none", favourite="null"):
		
		"""This keyword will import contact.
		
		Arguments are passed as given below.
		
		desired_name,'avatar','colour' and 'favorite',status_falg,delete_flag
		
		colour = none(default),red,blue,green,purple,orange,lightblue
		
		favorite = null(default),FAVORITE
		
		avatar = none(default),construction,driver,front desk,notepad,worker,warehouse,airplane,delivery,envelope,housekeeping,ptt phone,telephone,supervisor,book,desktop pc,field services,laptop pc,room service,tree,car,dispatcher,flower,medical,security,truck
		
		Here avatar, colour ,favorite, status_falg and delete_flag are optional arguments.
		
		"""
		#Initializing the status value	
		status="FAIL"
			
		print("Start of eptt")
		
		#Open eptt app
		self.open_eptt_app()
		
		#Select the Contact tab
		self.driver.find_element_by_id("ext-tab-3").click()
		print("Device: Navigated to the Contact tab")
		sleep(2)
		
		#Click on the Add Contact option
		self.driver.find_element_by_xpath(".//*[@text='Add Contact']").click()
		print("Device: Clicked on the Add Contact option")
		sleep(2)
		
		#Check if network error pop-up
		error=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Data connection')]")
		if len(error) > 0:
			print("Device: Data connection is unavailable error is found")
			
			#Click OK option
			self.driver.find_element_by_xpath(".//*[@text='OK']").click()
			print("Device: Clicked on OK option")
			sleep(2)
		else:
			#Click on Import Contact option
			elem=self.driver.find_elements_by_xpath(".//*[@text='Import Contact']")
			if len(elem) == 0:
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
				
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			else:
				elem[0].click()
				print("Device: Clicked on Import Contact option Button")
				sleep(5)
				
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
		
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
					
				elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
				print(len(elem))
				if len(elem) > 0:			
					print("Device: No contact is found with the given name")

					#Click on the clear search option
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)						
				elif len(elem) == 0 :
					print("Device: Contact with the given name is available")
					
					#Click on the contact found
					self.driver.find_element_by_xpath(".//*[contains(@text, '"+number+"')]").click()
					print("Device: Clicked on the clear search option")
					sleep(2)
																				
				#Select favorite
				if favourite == 'FAVORITE':
					#Set the contact as favorite
					self.driver.find_element_by_xpath(".//*[@text='FAVORITE']").click()
					print("Device: Contact is made as favorite")
					sleep(2)
				
				#Select the colour
				self.driver.find_element_by_xpath(".//*[@text='set color "+colour+"']").click()	
				print("Device: Selected "+colour+" colour")
				sleep(2)
								
				#Select the avatar
				self.driver.find_element_by_xpath(".//*[@text='select avatar']").click()				
				print ("Device: Clicked on avatar options")
				sleep(2)
				
				#Set avatar
				self.driver.find_element_by_xpath(".//*[@text='set avatar "+avatar+"']").click()
				print("Device: Selected "+avatar+" avatar")
				sleep(5)
								
				elem5=self.driver.find_elements_by_xpath(".//*[@text='Save']")
				if len(elem5)>0:
					#Save the contact
					self.driver.find_element_by_xpath(".//*[@text='Save']").click()
					print("Device: Clicked Save button")
						
					for i in range(0, 10):
						elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact created')]")
						elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'The phone number')]")
						if len(elem2) > 0:
							print("Device: Contact saved successfully")
							sleep(2)
							status="PASS"				
							break
						elif len(elem3) > 0:
							print("Devices: The phone number entered is invalid")
							
							#Click on OK
							self.driver.find_element_by_xpath(".//*[@text='OK']").click()
							print("Device: Clicked OK button")
							sleep(2)
							
							#Cancel the contact
							self.driver.find_element_by_xpath(".//*[@text='Cancel']").click()
							print("Device: Clicked Cancel button")
							sleep(2)
							
							#Click on Yes
							self.driver.find_element_by_xpath(".//*[@text='Yes']").click()
							print("Device: Clicked Yes button")
							sleep(2)						
						sleep(1)
				else:
					#Click on Back button
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
					print("Device: Clicked on Back button")
					sleep(2)
				
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2) 
		
		
		return status

	#================================================================================================================
	# Method Name	     :  send_message
	#
	# Description        :  This method will send ptx.
	#
	# Arguments	         :  name, text, group, record_time, file_name, msg_type, forward, history_flag, namelist
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [28-Sep-2018]
	#================================================================================================================		

	def send_message(self,name="NULL",text="NULL",group="NULL", record_time=5, filename="NULL", msg_type="NULL", forward="NULL", history_flag=0,namelist="NULL",group_flag=0):
	
		"""This keyword will send a PTX message
		Arguments are passed as given below.
		
		name="Desired_Name", text="Text to be Sent", group="Desired_Group", record_time=default value is 5 seconds, Desired number can be given for big attachment, filename="Desired Filename to be attached", msg_type=Text,Image,Video,Audio,File, forward=Contact,Group,Quick_Group,history flag,namelist=[name1,name2...name n],group_flag
		"""
		#Initializing the status value
		status="FAIL"		

		#Open eptt app
		self.open_eptt_app()
		
				
		if msg_type == 'Text' and text!='NULL' and name!= 'NULL':
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for PTX
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
				#Click on Send text option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
				sleep(2)
				print("Device: Clicked on Send Text")
				
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Enter Text')]")
			if len(elem1) > 0:	
				#Initiate a Text Message
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Enter Text')]").send_keys(text)
				#Click on the send button
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send PTX Message')]").click()
			
				print("Device: Clicked on Send Text button ")
				
				status="PASS"
				#Navigate to App Home page if different page is opened
				for i in range (0, 3):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			else:
				print("Device: Unable to send the Text Message ")
				
					
		if msg_type == "Image" and name!= 'NULL':
			
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for PTX
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
			#Click on Send text option
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
			sleep(2)
			print("Device: Clicked on Send Text")
			#Attach an Image
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Send image or video')]").click()
			print("Device: Navigated to Camera button")
			sleep(2)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Take a photo')]").click()
			print("Device: Clicked on Take a Photo")
			sleep(2)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Shutter')]").click()
			print("Device: Captured a Photo")
			sleep(2)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'OK')]").click()
			sleep(2)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'OK')]").click()
			print("Device: Sent a Photo")
			sleep(5)
			
			status = "PASS"
			#Navigate to App Home page if different page is opened
			for i in range (0, 2):
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
			#Click on the Home Button    
			self.driver.press_keycode(3)
			print("Device: Clicked on Home Button")
			sleep(2)
			
			
		if msg_type == "Video" and name!= 'NULL':
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for PTX
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
			#Click on Send text option
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
			sleep(2)
			print("Device: Clicked on Send Text")
			#Attach Video
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Send image or video')]").click()
			print("Device: Navigated to Camera button")
			sleep(2)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Record a Video')]").click()
			print("Device: Clicked on Record a Video")
			sleep(2)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Record')]").click()
			print("Device: Started Recording")
			sleep(record_time)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Stop')]").click()
			print("Device: Stopped Recording")
			sleep(2)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'OK')]").click()
			sleep(2)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'OK')]").click()
			print("Device: Sent a Video")
			sleep(2)
			
			status = "PASS"
			#Navigate to App Home page if different page is opened
			for i in range (0, 2):
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
			#Click on the Home Button    
			self.driver.press_keycode(3)
			print("Device: Clicked on Home Button")
			sleep(2)

		if msg_type == "Audio" and name!= 'NULL':
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for PTX
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
			#Click on Send text option
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
			sleep(2)
			print("Device: Clicked on Send Text")
			#Attach Audio
			self.driver.find_element_by_xpath(".//*[contains(@text, 'VOICE MESSAGE')]").click()
			print("Device: Navigated to Voice message button")
			sleep(2)
			self.actions.long_press(self.driver.find_element_by_xpath(".//*[contains(@text, 'record')]")).wait(10000).release().perform()
			print("Device: Initiated a Voice Message")
			sleep(5)
			self.driver.find_element_by_xpath(".//*[contains(@text, 'OK')]").click()
			sleep(2)
			print("Device: Sent a Voice Message")
			sleep(2)
			
			status = "PASS"
			#Navigate to App Home page if different page is opened
			for i in range (0, 2):
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
			#Click on the Home Button    
			self.driver.press_keycode(3)
			print("Device: Clicked on Home Button")
			sleep(2)
			
		if msg_type == "File" and filename != 'NULL' and name!= 'NULL':
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for PTX
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
			#Click on Send text option
			self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
			sleep(2)
			print("Device: Clicked on Send Text")
			#Attach File
			self.driver.find_element_by_xpath(".//*[contains(@text, 'File')]").click()
			print("Device: Navigated to File Button")
			sleep(5)
			elem1 = self.driver.find_elements_by_xpath(".//*[contains (@text, 'Downloads')]")
			if len(elem1) > 0:			
				self.driver.find_element_by_xpath(".//*[contains(@text, '"+filename+"')]").click()
				sleep(2)
				print("Device: Selected a Document")
				sleep(2)
				self.driver.find_element_by_xpath(".//*[contains(@text, 'OK')]").click()
				sleep(2)
				print("Device: Sent a File")
				status = "PASS"
				#Navigate to App Home page if different page is opened
				for i in range (0, 2):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
			else:
				self.driver.find_element_by_xpath(".//*[contains(@content-desc, 'Show')]").click()
				sleep(5)
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Downloads')]").click()
				sleep(2)
				print("Device: Navigated to Downloads")
				self.driver.find_element_by_xpath(".//*[contains(@text, '"+filename+"')]").click()
				sleep(2)
				print("Device: Selected a Document")
				sleep(2)
				self.driver.find_element_by_xpath(".//*[contains(@text, 'OK')]").click()
				sleep(2)
				print("Device: Sent a File")
				status = "PASS"
				#Navigate to App Home page if different page is opened
				for i in range (0, 2):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)

		if forward == "Contact" and text!= 'NULL':
		
		
			
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for PTX
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
				#Click on Send text option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
				sleep(2)
				print("Device: Clicked on Send Text")
				
			if text == 'Image':
				input="image, success"
			if text == 'Video':
				input="video, success"
			if text == 'Audio':
				input="audio, success"
			if text == 'File':
				input="file, success"
			#Select the Message to be forwarded
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '"+input+"')]")
			if len(elem) > 0:							
				#Long Press on the Message to be forwarded
				self.actions.long_press(elem[-1]).perform()
				print("Device: Long Pressed on the Message to be Forwarded")
				sleep(2)
			
				#Selected on Forward to Contact
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Forward to Contact')]").click()
				print("Device: Selected Forward to Contact")
				sleep(2)
				
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
				
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
				
				#Click on the Contact
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(2)
				
				#Click OK if asked
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'OK')]")
				sleep(2)
				if len(elem2)>0:
					elem2[0].click()
					print("Device: Forwarded the Message to Contact Successfully")
				
				#Click on the send button if present
				
				elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Send PTX Message')]")
				if len(elem3)>0:
					elem3[0].click()
					print("Device: Forwarded the Message to Contact Successfully")
				status = "PASS"
				#Navigate to App Home page if different page is opened
				for i in range (0, 2):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			else:
				print("Could not find the Message to be forwarded")
		
		
		if int(history_flag) == 1 and text!='NULL' and name!='NULL':
			
			
			element=self.driver.find_elements_by_xpath(".//*[@text='History']")
			print(len(element))
			sleep(2)
			if len(element) == 0:
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
				sleep(2)
				self.driver.find_elements_by_xpath(".//*[@text='History']").click()
			
			else:
				element[0].click()
				sleep(2)
			
			elem1 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Details')]")
			sleep(2)
			elem1[0].click()
			#Select the Message to be forwarded
			elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, '"+text+"')]")
			if len(elem2) > 0:							
				#Long Press on the Message to be forwarded
				self.actions.long_press(elem2[-1]).perform()
				print("Device: Long Pressed on the Message to be Forwarded")
				sleep(2)
			
				#Selected on Forward to Contact
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Forward to Contact')]").click()
				print("Device: Selected Forward to Contact")
				sleep(2)
				
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
				print("Device: Entered the given name in search bar")
				sleep(2)
				
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
				
				#Click on the Contact
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(2)
				
				#Click on the send button
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send PTX Message')]").click()
				print("Device: Forwarded the Message to Contact Successfully")
				
				status = "PASS"
				#Navigate to App Home page if different page is opened
				for i in range (0, 2):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			else:
				print("Could not find the Message to be forwarded")
		
		
		if forward == "Quick_Group" and namelist!= 'NULL' and text!= 'NULL':
			user_name = ast.literal_eval(namelist)
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for PTX
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
				#Click on Send text option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
				sleep(2)
				print("Device: Clicked on Send Text")
			if text == 'Image':
				input="image, success"
			if text == 'Video':
				input="video, success"
			if text == 'Audio':
				input="audio, success"
			if text == 'File':
				input="file, success"
			#Select the Message to be forwarded
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '"+input+"')]")
			if len(elem) > 0:							
				#Long Press on the Message to be forwarded
				self.actions.long_press(elem[-1]).perform()
				print("Device: Long Pressed on the Message to be Forwarded")
				sleep(2)
			
				#Selected on Forward to Contact
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Forward to Quick Group')]").click()
				print("Device: Selected Forward to Quick Group")
				sleep(2)
				
				for x in user_name:
					#Input the name into search bar
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(x)	
					print("Device: Entered the given name in search bar")
					sleep(2)
					#Select the Contact 
					elem1 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
					elem1[0].click()
					sleep(2)
					print("Device: Selected Contact",x)
					#Clear the Search
					self.driver.find_element_by_xpath(".//*[contains(@text, 'delete')]").click()
				
				
				print("Contacts selected for Quick Group")
				#Click on the send button
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Save')]").click()
				sleep(2)
				#Click OK if asked
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'OK')]")
				sleep(2)
				if len(elem2)>0:
					elem2[0].click()
					print("Device: Forwarded the Message to Contact Successfully")
				
				#Click on the send button if present
				
				elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Send PTX Message')]")
				if len(elem3)>0:
					elem3[0].click()
					print("Device: Forwarded the Message to Contact Successfully")
				
				status = "PASS"
				#Navigate to App Home page if different page is opened
				for i in range (0, 2):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			else:
				print("Could not find the Message to be forwarded")
		
		if forward == "Group" and group != 'NULL' and text!= 'NULL':
		
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(name)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for PTX
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
				#Click on Send text option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
				sleep(2)
				print("Device: Clicked on Send Text")
			if text == 'Image':
				input="image, success"
			if text == 'Video':
				input="video, success"
			if text == 'Audio':
				input="audio, success"
			if text == 'File':
				input="file, success"
			#Select the Message to be forwarded
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '"+input+"')]")
			if len(elem) > 0:							
				#Long Press on the Message to be forwarded
				self.actions.long_press(elem[-1]).perform()
				print("Device: Long Pressed on the Message to be Forwarded")
				sleep(2)
			
				#Selected on Forward to Contact
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Forward to Group')]").click()
				print("Device: Selected Forward to Group")
				sleep(2)
				
				print(group)
				#Input the name into search bar
				self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(group)	
				print("Device: Entered the given name in search bar")
				sleep(2)
				
				print("Device: Entered the group name in search bar")
				sleep(2)
				
				#Click Search/Done
				self.driver.press_keycode(66)
				print("Device: Clicked on search button")
				sleep(2)
				
				#Click on the Contact
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Group Name')]")
				elem1[0].click()
				print("Device: Clicked on the Group name")
				sleep(2)
				
				#Click OK if asked
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'OK')]")
				sleep(2)
				if len(elem2)>0:
					elem2[0].click()
					print("Device: Forwarded the Message to Contact Successfully")
				
				#Click on the send button if present
				
				elem3=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Send PTX Message')]")
				if len(elem3)>0:
					elem3[0].click()
					print("Device: Forwarded the Message to Contact Successfully")
				
				status = "PASS"
				#Navigate to App Home page if different page is opened
				for i in range (0, 2):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			else:
				print("Could not find the Message to be forwarded")
				
		if int(group_flag) == 1 and group!= 'NULL' and text!='NULL':
			#Select the Group tab
			self.driver.find_element_by_xpath(".//*[@text='Group']").click()
			print("Device: Navigated to the Group tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(group)	
			print("Device: Entered the given name in search bar")
			sleep(2)
			
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0:
				#Select the Contact for PTX
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Group Name "+group+"')]")
				elem1[0].click()
				print("Device: Clicked on the Group name")
				sleep(5)
				#Click on Send text option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
				sleep(2)
				print("Device: Clicked on Send Text")
				
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Enter Text')]")
			if len(elem1) > 0:	
				#Initiate a Text Message
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Enter Text')]").send_keys(text)
				#Click on the send button
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send PTX Message')]").click()
			
				print("Device: Clicked on Send Text button ")
				
				status="PASS"
				#Navigate to App Home page if different page is opened
				for i in range (0, 2):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
				
			else:
				print("Device: Unable to send the Text Message ")
				
		if int(group_flag) == 1 and namelist!= 'NULL' and text!='NULL':
			user_name = ast.literal_eval(namelist)
			#Select the Contact tab
			self.driver.find_element_by_id("ext-tab-3").click()
			print("Device: Navigated to the Contact tab")
			sleep(2)
			
			#Input the name into search bar
			self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(user_name[0])	
			print("Device: Entered the given name in search bar")
			sleep(2)
		
			#Click Search/Done
			self.driver.press_keycode(66)
			print("Device: Clicked on search button")
			sleep(2)
			
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
			print(len(elem))
			if len(elem) == 0 :
				#Select the Contact for IPA
				#self.driver.find_element_by_partial_link_text('"' + name + '"').click()
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
				elem1[0].click()
				print("Device: Clicked on the contact name")
				sleep(5)
								
				#Initiate EPTT Call
				#self.driver.find_element_by_xpath(".//*[contains(@text, 'Call')]").click()
				#sleep(2)
				
				for i in range (len(user_name[1:])):
					#Click on add participant option
					self.driver.find_element_by_xpath(".//*[contains(@text, 'add participant')]").click()
					print("Device: Clicked on add participant option")
					sleep(2)
					
					#Input the name into search bar
					self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'search')]").send_keys(user_name[i+1])	
					print("Device: Entered the given name in search bar")
					sleep(2)
				
					#Click Search/Done
					self.driver.press_keycode(66)
					print("Device: Clicked on search button")
					sleep(2)
					
					elem=self.driver.find_elements_by_xpath(".//*[contains(@text, 'No matches found')]")
					if len(elem) == 0 :
						#Select the Contact
						elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Contact presence')]")
						elem1[0].click()
						print("Device: Clicked on the contact name")
						sleep(5)
						
						#Click Save button
						self.driver.find_element_by_xpath(".//*[@text='Save']").click()
						print("Device: Clicked Save button")
						sleep(2)
					else:
						#Click on the clear search option
						self.driver.find_element_by_xpath(".//*[contains(@resource-id, 'clear')]").click()
						print("Device: Clicked on the clear search option")
						sleep(2)
						
						#Click on the Back Option
						self.driver.find_element_by_xpath(".//*[contains(@text, 'Back')]").click()
						print("Device: Clicked on Back option")
						sleep(2)
				
			#Click on Send text option
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send text')]").click()
				sleep(2)
				print("Device: Clicked on Send Text")
				
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Enter Text')]")
			if len(elem1) > 0:	
				#Initiate a Text Message
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Enter Text')]").send_keys(text)
				#Click on the send button
				self.driver.find_element_by_xpath(".//*[contains(@text, 'Send PTX Message')]").click()
			
				print("Device: Clicked on Send Text button ")
				
				status="PASS"
				#Navigate to App Home page if different page is opened
				for i in range (0, 2):
					#Click on the Back Button    
					self.driver.press_keycode(4)
					print("Device: Clicked on Back Button")
					sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
				
			else:
				print("Device: Unable to send the Text Message ")
		return status
		
	#================================================================================================================
	# Method Name		:	auto_download
	#
	# Description		:	This method will turn ON/OFF Automatic download of Attachments 
	#
	#Arguments			:	download
	#
	#Returns			:	PASS/FAIL
	#
	#Date Modified		:	Newly Added[06-Oct-2018]
	#=================================================================================================================
	
	def auto_download(self,download="ON"):
		"""This keyword will set Automatic Download On/OFF
		Arguments are passed as given below.
		
		download="ON/OFF"
		"""
		
		#Initializing the status value
		status="FAIL"		

		#Open eptt app
		self.open_eptt_app()		
		sleep(2)
		#Click on Menu
		self.driver.find_element_by_xpath(".//*[@text='Menu']").click()
		print("Device: Clicked on Menu")
		sleep(5)
		
		#Click on Settings
		self.driver.find_element_by_xpath(".//*[@text='Settings']").click()
		print("Device: Clicked on Settings")
		sleep(5)
		
		#Locate Auto download button
		elem = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[17]/android.view.View/android.widget.Button")
		sleep(2)
		
		#Swipe up to make the changes
		self.driver.swipe(500, 1750,500, 500, None)		
		sleep(5)
		
		if download == "ON":			
			#Below statement return text sometimes so commenting it 
			#print elem.get_attribute("text")
			status = elem.text
			print status
			if status == "ON":
				print("Device: Automatic download is already ON")
				status = "PASS"
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			elif status == "OFF":
				elem.click()
				sleep(2)
				print("Device: Automatic download turned ON successfully")
				status = "PASS"
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			else:
				print("Device: Couldn't",download,"Automatic download Button")
			
		if download == "OFF":
			
			#Below statement return text sometimes so commenting it 
			#print elem.get_attribute("text")
			status = elem.text
			print status
			if status == "ON":
				elem.click()
				print("Device: Automatic download Turned OFF successfully")			
				status = "PASS"
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			elif status == "OFF":
				sleep(2)
				print("Device: Automatic download is already OFF")
				status = "PASS"
				#Click on the Back Button    
				self.driver.press_keycode(4)
				print("Device: Clicked on Back Button")
				sleep(2)
				#Click on the Home Button    
				self.driver.press_keycode(3)
				print("Device: Clicked on Home Button")
				sleep(2)
			else:
				print("Device: Couldn't",download,"Automatic download Button")
		
		return status
		
	#=================================================================================================================
	#Method Name		 :	verify_message
	#
	#Description		 :	This method will verify the ptx being received.
	#
	# Arguments	         :  name, text, image_flag,text_flag,video_flag,audio_flag,file_flag
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [02-Oct-2018]
	#=================================================================================================================
	def verify_message(self,text="NULL", download="NULL", download_type="Manual", msg_type="NULL", reply_flag=0, url_flag=0):
		"""
		This keyword will verify message is being received at the MT from history.
		
		Arguments passed are as given below:
		text="Desired text to be verified", download="Image/Video/File/Audio",download_type="Manual/Automatic", msg_type="Image/Video/Audio/File",reply_flag,url_flag
		
		"""
	
		#Initializing the status value
		status="FAIL"		

		#Open eptt app
		self.open_eptt_app()
		#Navigate to App Home page if different page is opened
		for i in range (0, 2):
			elem = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Back')]")
			if len(elem) > 0:
				elem[0].click()
				print("Device: Clicked on Back button")
				sleep(2)
		
		if msg_type == "Text" and text!= 'NULL':		
			#Navigate to History Tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)		
			
			#Search for the text 
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '" + text + "')]")
			if len(elem) > 0:
				print("Device: Text Message Verified ")
				status = "PASS"
			else:
				print("Device: Unable to Receive Text Message ")				
		
		if msg_type == "Image":
			#Navigate to History Tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			
			#Search for the Image attachment
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Image Message')]")
			if len(elem1) > 0:
				print("Device: Image Attachment Verified")
				status = "PASS"
			else:
				print("Device: Unable to Receive Image Attachment")
				
		if msg_type == "Video":
			#Navigate to History Tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			#Search for the Video attachment
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Video Message')]")
			if len(elem1) > 0:
				print("Device: Video Attachment Verified")
				status = "PASS"
			else:
				print("Device: Unable to Receive Video Attachment")
				
		if msg_type == "File":
			#Navigate to History Tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			#Search for the file attachment
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'File Message')]")
			if len(elem1) > 0:
				print("Device: File Attachment Verified")
				status = "PASS"
			else:
				print("Device: Unable to Receive File Attachment")
				
		if msg_type == "Audio":
			#Navigate to History Tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			#Search for the audio attachment
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Audio Message')]")
			if len(elem1) > 0:
				print("Device: Audio Attachment Verified")
				status = "PASS"
			else:
				print("Device: Unable to Receive Audio Attachment")
				
		if int(reply_flag) == 1 and text!= 'NULL':
			#Navigate to History Tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			#Search for the text 
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '" + text + "')]")
			if len(elem) > 0:
				print("Device: Text Message Verified ")
				elem1 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Details')]")
				sleep(2)
				elem1[0].click()
				sleep(2)
				elem2=self.driver.find_elements_by_xpath(".//*[contains(@text, 'Enter Text')]")
				if len(elem2) > 0:	
					#Initiate a Text Message
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Enter Text')]").send_keys(text)
					#Click on the send button
					self.driver.find_element_by_xpath(".//*[contains(@text, 'Send PTX Message')]").click()
				
					print("Device: Clicked on Send Text button ")
					
					status="PASS"
					#Navigate to App Home page if different page is opened
					for i in range (0, 3):
						#Click on the Back Button    
						self.driver.press_keycode(4)
						print("Device: Clicked on Back Button")
						sleep(2)
					#Click on the Home Button    
					self.driver.press_keycode(3)
					print("Device: Clicked on Home Button")
					sleep(2)
			else:
				print("Device: Unable to Receive Text Message ")
		
		if download_type == "Manual" and download!='NULL':
			#Navigate to History Tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			#Search for the File to be downloaded
			elem = self.driver.find_elements_by_xpath(".//*[contains(@text, '"+download+" Message')]")
			print(len(elem))
			sleep(2)
			
			if len(elem) > 0:
				print(download,"Message is Verified in History download")
				elem1 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Details')]")
				sleep(2)
				elem1[0].click()
				sleep(2)
				
				elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'notdownloaded')]")
				if len(elem2) > 0:
					print(download,"Message is not downloaded")
					sleep(2)
					if download == "Image":
						elem3 = self.driver.find_elements_by_xpath(".//*[contains(@resource-id, 'ptxnotdownloaded')]")
						elem3[-1].click()
						sleep(2)
						print("Downloaded",download,"Message")
						status = "PASS"
						#Navigate to App Home page if different page is opened
						for i in range (0, 2):
							#Click on the Back Button    
							self.driver.press_keycode(4)
							print("Device: Clicked on Back Button")
							sleep(2)
						#Click on the Home Button    
						self.driver.press_keycode(3)
						print("Device: Clicked on Home Button")
						sleep(2)
					elif download == "Video":
						elem3 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'video, notdownloaded')]")
						elem3[-1].click()
						sleep(2)
						print("Downloaded",download,"Message")
						status = "PASS"
						#Navigate to App Home page if different page is opened
						for i in range (0, 2):
							#Click on the Back Button    
							self.driver.press_keycode(4)
							print("Device: Clicked on Back Button")
							sleep(2)
						#Click on the Home Button    
						self.driver.press_keycode(3)
						print("Device: Clicked on Home Button")
						sleep(2)
					elif download == "Audio":
						elem3 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'audio, notdownloaded')]")
						elem3[-1].click()
						sleep(2)
						print("Downloaded",download,"Message")
						status = "PASS"
						#Navigate to App Home page if different page is opened
						for i in range (0, 2):
							#Click on the Back Button    
							self.driver.press_keycode(4)
							print("Device: Clicked on Back Button")
							sleep(2)
						#Click on the Home Button    
						self.driver.press_keycode(3)
						print("Device: Clicked on Home Button")
						sleep(2)
					elif download == "File":
						elem3 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'file, notdownloaded')]")
						elem3[-1].click()
						sleep(2)
						print("Downloaded",download,"Message")
						status = "PASS"
						#Navigate to App Home page if different page is opened
						for i in range (0, 2):
							#Click on the Back Button    
							self.driver.press_keycode(4)
							print("Device: Clicked on Back Button")
							sleep(2)
						#Click on the Home Button    
						self.driver.press_keycode(3)
						print("Device: Clicked on Home Button")
						sleep(2)
						
		if download_type == "Automatic" and download!='NULL':
			#Navigate to History Tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			#Search for the File to be downloaded
			elem = self.driver.find_elements_by_xpath(".//*[contains(@text, '"+download+" Message')]")
			print(len(elem))
			sleep(2)
			
			if len(elem) > 0:
				print(download,"Message is Verified in History download")
				elem1 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Details')]")
				sleep(2)
				elem1[0].click()
				sleep(2)
				
				elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'notdownloaded')]")
				if len(elem2) == 0:
					print("Device:",download,"Message is Auto downloaded")
					sleep(2)
					status = "PASS"
					#Navigate to App Home page if different page is opened
					for i in range (0, 2):
						#Click on the Back Button    
						self.driver.press_keycode(4)
						print("Device: Clicked on Back Button")
						sleep(2)
					#Click on the Home Button    
					self.driver.press_keycode(3)
					print("Device: Clicked on Home Button")
					sleep(2)
			
		if int(url_flag) == 1 and text!='NULL':
			#Navigate to History Tab
			self.driver.find_element_by_id("ext-tab-1").click()
			print("Device: Navigated to the History tab")
			sleep(2)
			#Search for the text 
			elem=self.driver.find_elements_by_xpath(".//*[contains(@text, '" + text + "')]")
			if len(elem) > 0:
				print("Device: Text Message Verified ")
				elem1 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Details')]")
				sleep(2)
				elem1[0].click()
				print("Device: Message box opened")
				sleep(2)
				elem2 = self.driver.find_elements_by_xpath(".//*[contains(@text, '"+text+"')]")
				elem2[-1].click()
				sleep(2)
				elem3 = self.driver.find_elements_by_xpath(".//*[contains(@text, 'Bookmarks')]")
				if len(elem3) > 0:
					print("Device: Successfully Clicked on URL:", text)
					status = "PASS"
					sleep(5)
					#Navigate to App Home page if different page is opened
					
					for i in range (0, 3):
						#Click on the Back Button    
						self.driver.press_keycode(4)
						print("Device: Clicked on Back Button")
						sleep(2)
					#Click on the Home Button    
					self.driver.press_keycode(3)
					print("Device: Clicked on Home Button")
					sleep(2)
			
			
				
		return status

	#================================================================================================================
	# Method Name	     :  youtube_app
	#
	# Description        :  This method will open youtube app.
	#
	# Arguments	         :  
	#
	# Returns	         :  PASS
	#
	# Date Modified      :  Newly Added [08-Oct-2018]
	#================================================================================================================

	def youtube_app(self):
	
		"""
		This keyword will open youtube app.				
		"""
		#Initializing the status value
		status="PASS"
		
		#Click on the Home Button    
		self.driver.press_keycode(3)
		print("Device: Clicked on Home Button")
		sleep(2)

		#Open the Youtube app
		self.driver.start_activity("com.google.android.youtube", "com.google.android.apps.youtube.app.application.Shell$HomeActivity");
		print("Device: Opened youtube app")	
		sleep(5)
				
		return status

		
class IOS:
	
	def __init__(self,serial,timeout):
	
		desired_caps = {}
		desired_caps['udid'] = serial   
		desired_caps['automationName'] = 'XCUITest'
		desired_caps['browserName'] = 'safari'
		desired_caps['newCommandTimeout'] = timeout
		desired_caps['deviceConnectUsername'] = 'team@automation.com'
		desired_caps['deviceConnectApiKey'] = 'e627dfe3-2a84-4de1-bcb4-0edc35b84b75'
		
		self.driver = webdriver.Remote('http://107.250.171.220/Appium', desired_caps)
		self.actions = TouchAction(self.driver)
		
		# To deactivate the current app, Here safari Browser
		self.driver.background_app(-1)
		print("Device: Closed the background apps")	
		print("Device: operations are Started") 
		
		# pause a moment, so xml generation can occur
		sleep(2)				
		
	def close(self):
		self.driver.quit()			

	#================================================================================================================
	# Method Name	     :  open_eptt_app
	#
	# Description        :  This method will open EPTT App.
	#
	# Arguments	         :  
	#
	# Returns	         :  
	#
	# Date Modified      :  Newly Added [24-Aug-2018]
	#================================================================================================================		
		
	def open_eptt_app(self):		 
		
		self.driver.switch_to.context("NATIVE_APP")
	
		#Swipe the screen
		self.driver.swipe(500, 500, 1000, 500, None)		
		sleep(5)
	
		#Enter the EPTT text into the search field
		self.driver.find_element_by_xpath(".//*[@name='SpotlightSearchField']").send_keys("EPTT")
		print("Device: Entered EPTT text into the search field")
		sleep(2)
		
		#Click on the Search option
		self.driver.find_element_by_xpath(".//*[@name='Search']").click()
		print("Device: Entered EPTT text into the search field")	
		sleep(2)
		
		#Click on EPTT App found on the search screen
		self.driver.find_element_by_xpath(".//*[@label='EPTT']").click()
		print("Device: Opened EPTT App")	
		sleep(2)
		
		for i in range (0, 2):
			elem = self.driver.find_elements_by_xpath(".//*[contains(@label, 'Back')]")
			if len(elem) > 0:
				elem[0].click()
				print("Device: Clicked on Back button")
				sleep(2)

	#================================================================================================================
	# Method Name	     :  create_contact
	#
	# Description        :  This method will add the contact to EPTT App.
	#
	# Arguments	         :  name,number,avatar='set avatar none',colour='set color none',favorite='FAVORITE',status_flag="0",delete_flag="0"
	#
	# Returns	         :  
	#
	# Date Modified      :  Newly Added [24-Aug-2018]
	#================================================================================================================
		
	def create_contact(self,name,number, avatar="none", colour="none", favourite="null", status_flag="0", delete_flag="0"):

        #Initializing the status value	
		status="FAIL"
					
		print("Start of eptt")
		
		if int(delete_flag) == 1:
			#Delete the contact if already present
			self._delete_copy_contact(number)
			sleep(2)

		#Select the Contact tab
		self.driver.find_element_by_xpath(".//*[@label='Contact']").click()
		print("Device: Navigated to the Contact tab")
		sleep(2)
		
		#Click on the Add Contact option
		self.driver.find_element_by_xpath(".//*[@label='Add Contact']").click()
		print("Device: Clicked on the Add Contact option")
		sleep(2)
		
		#Click on New Contact option
		self.driver.find_element_by_xpath(".//*[@label='New Contact']").click()
		print("Device: Clicked on New Contact option Button")
		sleep(5)

		elem1=self.driver.find_elements_by_xpath(".//*[@type='XCUIElementTypeTextField']")
		if len(elem1) > 0:
			#Input the number
			elem1[1].send_keys(number)				
			print("Device: Inserted the number")
			sleep(2)
		
			#Input the name
			elem1[0].send_keys(name)	
			print("Device: Inserted the name")
			sleep(2)
			
			#Click OK/DONE button
			self.driver.find_element_by_xpath(".//*[@label='return']").click()
			print("Device: Clicked return option")
			sleep(2)	
		
		#Select favorite
		if favourite == 'FAVORITE':
			#Set the contact as favorite
			self.driver.find_element_by_xpath(".//*[@label='FAVORITE']").click()
			print("Device: Contact is made as favorite")
			sleep(2)	

		#Select the colour
		self.driver.find_element_by_xpath(".//*[@label='set color "+colour+"']").click()	
		print("Device: Selected "+colour+" colour")
		sleep(2)		
		
		#Select the avatar
		self.driver.find_element_by_xpath(".//*[@label='select avatar']").click()				
		print ("Device: Clicked on avatar options")
		sleep(2)

		#Set avatar
		self.driver.find_element_by_xpath(".//*[@label='set avatar "+avatar+"']").click()
		print("Device: Selected "+avatar+" avatar")
		sleep(5)

		#Save the contact
		self.driver.find_element_by_xpath(".//*[@label='Save']").click()
		print("Device: Clicked Save button")
		status="PASS"
		sleep(5)

		#Check the status is visible after adding a contact
		if status == "PASS" :
			if int(status_flag) == 1:
				p=self._check_status(name)
				return p
			else:		
				return status

	#================================================================================================================
	# Method Name	     :  _delete_copy_contact
	#
	# Description        :  This method will delete the copy contact.
	#
	# Arguments	         :  number
	#
	# Returns	         :  
	#
	# Date Modified      :  Newly Added [24-Aug-2018]
	#================================================================================================================
		
	def _delete_copy_contact(self,number):

		"""This keyword will delete the copy of contact.
		
		Arguments are passed as given below.
		
		number_1, driver
		
		"""									
		
		#Select the Contact tab
		self.driver.find_element_by_xpath(".//*[@label='Contact']").click()
		print("Device: Navigated to the Contact tab")
		sleep(2)

		#Check if contacts tab is empty or not
		elem2=self.driver.find_elements_by_xpath(".//*[contains(@label, 'To add contacts:')]")
		if len(elem2) == 0:		
			#Input the number into search bar
			self.driver.find_element_by_xpath(".//*[contains(@type, 'XCUIElementTypeSearchField')]").send_keys(number)	
			print("Device: Entered the given number in search bar")
			sleep(2)
	
			#Click Done
			self.driver.find_element_by_xpath(".//*[@label='Done']").click()
			print("Device: Clicked on Done button")
			sleep(2)
				
			elem=self.driver.find_elements_by_xpath(".//*[contains(@label, 'No matches found')]")
			print(len(elem))
			if len(elem) > 0:			
				print("Device: No contact is found with the given number")
				
				#Click on the clear search option
				self.driver.find_element_by_xpath(".//*[contains(@label, 'Clear')]").click()
				print("Device: Clicked on the clear search option")
				sleep(2)
			elif len(elem) == 0 :
				#Select the contact found
				elem1=self.driver.find_elements_by_xpath(".//*[contains(@label, 'Contact presence')]")
				
				#Long press on the contact found
				#self.actions.press(elem1[0]).wait(5001).release().perform()
				self.actions.press(elem1[0]).wait(5000).release()
				print("Device: Long pressed on the contact found")
				sleep(2)
				
				#Click on Delete Contact
				self.driver.find_element_by_xpath(".//*[contains(@label, 'Delete Contact')]").click()
				print("Device: Clicked on Delete Contact option")
				sleep(2)
				
				#Click on OK option
				self.driver.find_element_by_xpath(".//*[contains(@label, 'OK')]").click()
				print("Device: Clicked on OK option")
				sleep(2)
		else:
			print("Device: No Contacts to search and delete")
			
	#================================================================================================================
	# Method Name	     :  _check_status
	#
	# Description        :  This method will get the status for the given name in the contact.
	#
	# Arguments	         :  name
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [24-Aug-2018]
	#================================================================================================================
			
	def _check_status(self,name):
		
		"""This keyword will get the status for the given name in the contact.
		
		Arguments are passed as given below.
		
		name_1
		
		"""
		#Initializing the status value	
		status="FAIL"
		
		sleep(10)				
		
		#Select the Contact tab
		self.driver.find_element_by_xpath(".//*[@label='Contact']").click()
		print("Device: Navigated to the Contact tab")
		sleep(2)
		
		#Check whether the given name is already available in the contacts
		elem=self.driver.find_elements_by_xpath(".//*[contains(@label, '" + name + "')]")
		if len(elem) > 0:
			#Select the Contact for IPA
			elem[0].click()
			print("Device: Clicked on the contact name")
			sleep(5)
			
			#Click on Contact Details button
			self.driver.find_element_by_xpath(".//*[contains(@label, 'Contact Details')]").click()	
			print("Device: Clicked on Contact Details option")
			sleep(5)
			
			elem1=self.driver.find_elements_by_xpath(".//*[contains(@label, 'Status')]")	
			if len(elem1)> 0:
				status="PASS"
				print("Device: Status is found")
				sleep(2)
			else:
				print("Device: Status is not found")
			
			#Click on the Back Option
			self.driver.find_element_by_xpath(".//*[contains(@label, 'Back')]").click()
			print("Device: Clicked on Back option")
			sleep(2)
			
			#Click on the Back Option
			self.driver.find_element_by_xpath(".//*[contains(@label, 'Back')]").click()
			print("Device: Clicked on Back option")
			sleep(2)
			
		else:
			print("Device: Given name is not found in the contact")
			status="FAIL"
			sleep(2)

		return status
		
	#================================================================================================================
	# Method Name	     :  airplane_mode_off
	#
	# Description        :  This method performs the airplane mode off activity.
	#
	# Arguments	         : 
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [27-Aug-2018]
	#================================================================================================================

	def airplane_mode_off(self):
		#Initializing the status value
		status="FAIL"
		
		#Close the background apps
		self.driver.background_app(-1)	
		
		#######################################
		##Airplane Mode: OFF : START
		#######################################
		
		self.driver.switch_to.context("NATIVE_APP")
	
		# #Swipe the screen
		# self.driver.swipe(500, 500, 1000, 500, None)		
		# sleep(5)
	
		# #Enter the EPTT text into the search field
		# self.driver.find_element_by_xpath(".//*[@name='SpotlightSearchField']").send_keys("Settings")
		# print("Device: Entered Settings text into the search field")
		# sleep(2)
		
		# #Click on the Search option
		# self.driver.find_element_by_xpath(".//*[@name='Search']").click()
		# print("Device: Clicked on Search option")	
		# sleep(2)
		
		#Click on Settings App found on the search screen
		self.driver.find_element_by_xpath(".//*[@label='Settings']").click()
		print("Device: Opened Settings App")	
		sleep(2)
		
		#Set the airplane mode status
		mode=self.driver.find_element_by_xpath(".//*[@type='XCUIElementTypeSwitch']").get_attribute("value")
		if mode == "0":
			print("Device: Airplane mode is already OFF")
			status="PASS"
		elif mode == "1":
			self.driver.find_element_by_xpath(".//*[@type='XCUIElementTypeSwitch']").click()
			print("Device: Airplane mode is OFF now")
			status="PASS"
		
		sleep(5)
		#######################################
		##Mobile Airplane Mode: OFF : END
		####################################### 

		#Close the background apps
		self.driver.background_app(-1)
		
		self.driver.switch_to.context("NATIVE_APP")
	
		#Swipe the screen
		self.driver.swipe(500, 500, 1000, 500, None)		
		sleep(5)
	
		#Enter the EPTT text into the search field
		self.driver.find_element_by_xpath(".//*[@name='SpotlightSearchField']").send_keys("EPTT")
		print("Device: Entered EPTT text into the search field")
		sleep(2)
		
		#Click on the Search option
		self.driver.find_element_by_xpath(".//*[@name='Search']").click()
		print("Device: Entered EPTT text into the search field")	
		sleep(2)
		
		#Click on EPTT App found on the search screen
		self.driver.find_element_by_xpath(".//*[@label='EPTT']").click()
		print("Device: Opened EPTT App")	
		sleep(2)
		
		for i in range (0, 2):
			elem = self.driver.find_elements_by_xpath(".//*[contains(@label, 'Back')]")
			if len(elem) > 0:
				elem[0].click()
				print("Device: Clicked on Back button")
				sleep(2)	
			
		return status
		
	#================================================================================================================
	# Method Name	     :  airplane_mode_on
	#
	# Description        :  This method performs the airplane mode on activity.
	#
	# Arguments	         :  
	#
	# Returns	         :  PASS/FAIL
	#
	# Date Modified      :  Newly Added [27-Aug-2018]
	#================================================================================================================

	def airplane_mode_on(self):
		
		#Initializing the status value
		status="FAIL"
		
		#Close the background apps
		self.driver.background_app(-1)	
				
		#######################################
		##Airplane Mode: ON : START
		####################################### 
		
		self.driver.switch_to.context("NATIVE_APP")
	
		# #Swipe the screen
		# self.driver.swipe(500, 500, 1000, 500, None)		
		# sleep(5)
	
		# #Enter the EPTT text into the search field
		# self.driver.find_element_by_xpath(".//*[@name='SpotlightSearchField']").send_keys("Settings")
		# print("Device: Entered Settings text into the search field")
		# sleep(2)
		
		# #Click on the Search option
		# self.driver.find_element_by_xpath(".//*[@name='Search']").click()
		# print("Device: Clicked on Search option")	
		# sleep(2)
		
		#Click on Settings App found on the search screen
		self.driver.find_element_by_xpath(".//*[@label='Settings']").click()
		print("Device: Opened Settings App")	
		sleep(2)
		
		#Set the airplane mode status
		mode=self.driver.find_element_by_xpath(".//*[@type='XCUIElementTypeSwitch']").get_attribute("value")
		if mode == "1":
			print("Device: Airplane mode is already ON")
			status="PASS"
		elif mode == "0":
			self.driver.find_element_by_xpath(".//*[@type='XCUIElementTypeSwitch']").click()
			print("Device: Airplane mode is ON now")
			status="PASS"
		 
		sleep(5)	
		#######################################
		##Mobile Airplane Mode: ON : END
		#######################################    

		#Close the background apps
		self.driver.background_app(-1)
		
		return status	
			
