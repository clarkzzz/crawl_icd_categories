# Crawl ICD Categories' Codes and Corresponding Descriptions
Target website: https://www.icd10data.com/ICD10CM/Codes

## Goal
I want to obtain data in the form of:
code| description
---| ---
code_1| description_1
code_2| description_2
code_3| description_3

## Problem
To obtain data in the above format, I would need to visit over 280 URLs and note down the information manually, which would not be time well spent.

## Solution
Using the target website, this code:
1. extracts the ICD groups from the initial page
2. builds a list of URLs for each category group
3. extract each category code and corresponding description from the aforementioned list of URLs
