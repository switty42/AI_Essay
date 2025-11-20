# Test code written for Hannah witty
# Author Stephen Witty switty@level500.com
# 7-12-25
# Test uniqueness of Gemini responses
#
# Base code from AI_Probe at level500.com
#
# V1 7-12-25 - Initial release / dev
#
# Notes - Add your API key below

from google import genai
from google.genai import types
import time
import sys
import os
import random

# Put API key here
key = “XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX”

# AI model desired here
ai_model="gemini-2.5-flash"

###################### Constants ##########################################################
NUMBER_OF_CYCLES = 100                                 # Number of cycles to run before exiting
AI_RETRY_LIMIT = 25                                    # Number of times to retry API if errors occur
PROMPT = "How many Rs are in the word strawberry?"               # AI prompt

########## This function creates the AI prompt #######
def create_ai_prompt():
   prompt_message = PROMPT
   return prompt_message

########### This function formats an output string ####################
def print_string(string):
   cnt = 0
   for char in string:
      if not (char == " " and cnt == 0):
         print(char, end = "")
         cnt = cnt + 1
      if (cnt > 115 and char == " "):
         print()
         cnt = 0
   print()
   sys.stdout.flush()

############### Function - Call AI API #########################################
def call_ai(prompt_message):
   try:
      client = genai.Client(api_key=key)
      response = client.models.generate_content(
      model=ai_model,
      contents=prompt_message,
      config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)),)

   except Exception as e:
      return False, "", "WARNING:  System Error during AI api  call: " + str(e)

   return True, response.text, ""

###############  Start of main routine ##############################################################
number_of_cycles = 0
answer_history = []
duplicate = 0
duplicate_history = []
time_history = []
max_time = 0
min_time = 9999999999
ai_errors = 0
min_words = 999999999
max_words = 0
word_history = []

print("Starting........")
print("Prompt: " + PROMPT)
print("Model: " + ai_model)
print("------------------------\n\n")

while(number_of_cycles < NUMBER_OF_CYCLES): # Main loop to run prompts

   retry_count = 0
   success = False # Keep running prompt until we get a valid answer to check

   while (not success):

      if (retry_count == AI_RETRY_LIMIT):
         print("\n\nERROR: Too many AI errors, exiting\n")
         sys.exit()

      store_time = time.time()

      success, ai_reply, error_text = call_ai(PROMPT) # Call AI, retry if error
      if (not success):
         print(error_text)
         retry_count = retry_count + 1
         ai_errors = ai_errors + 1
         continue

      final_time = time.time() - store_time
      time_history.append(final_time)
      if (max_time < final_time):
         max_time = final_time
      if (min_time > final_time):
         min_time = final_time

      number_of_words = len(ai_reply.split())
      if (max_words < number_of_words):
         max_words = number_of_words
      if (min_words > number_of_words):
         min_words = number_of_words
      word_history.append(number_of_words)

      if (ai_reply in answer_history):
         duplicate = duplicate + 1
         duplicate_history.append(ai_reply)
      else:
         answer_history.append(ai_reply)

      print("Number: " + str(number_of_cycles + 1) + " Duplicates: " + str(duplicate) + " **************************** \n")
      print_string(ai_reply)
      print("\n")


   number_of_cycles = number_of_cycles + 1

avg_time = 0
for i in time_history:
   avg_time = avg_time + i
avg_time = avg_time / number_of_cycles

avg_words = 0
for i in word_history:
   avg_words = avg_words + i
avg_words = avg_words / number_of_cycles

print("\n\n----------- Final report -------------- ")
print("AI Test Prompt: " + PROMPT)
print("AI model: " + ai_model)

if (len(answer_history) > 4):
   print("\nFirst 5 non duplicate answers **********\n")
   for i in range(0,5,1):
      print("- " + answer_history[i])

print("\nNumber of cycles: " + str(number_of_cycles))
print("AI Errors: " + str(ai_errors))
print("AI prompt min time in seconds: " + str(round(min_time,2)))
print("AI prompt max time in seconds: " + str(round(max_time,2)))
print("AI average prompt time in seconds: " + str(round(avg_time,2)))
print("Max words in a reply: " + str(max_words))
print("Min words in a reply: " + str(min_words))
print("Average words in a reply: " + str(round(avg_words,2)))
print("Duplicate replies: " + str(duplicate))

if (duplicate > 0):
   print("\nDuplicate answers ***********")
   for i in duplicate_history:
      print("- " + i)

print("\n")
