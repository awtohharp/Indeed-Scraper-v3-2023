# Indeed-Scraper-v3-2023
This is a (personal) fork of a simple and recent Indeed scraper. 

The default locale is the United States; your inputs return a list of job titles, along with:
- Company
- Location
- Company rating
- Salary (minimum, maximum, and whether it's yearly/monthly/hourly)
- URL

Note that some features in this fork have not been tested in other locales. [The original repository appears to work with searches in India and the United States](https://github.com/RDxR10/Indeed-Scraper-v3-2023), so long as you change the base_url in scraper.py.

Filters include: 
- Search text
- Location
- Radius
- Remote-only
- Posting age

# Installation - Arch Linux

This has been tested with an existing installation of Python 3.10.

1. Install Chromium
```
pacman -Syu
pacman -S chromium
```
2. (Navigate to your desired parent directory and) clone this package
```
git clone https://github.com/awtohharp/Indeed-Scraper-v3-2023.git
```
3. Prepare your virtual environment
```
cd Indeed-Scraper-v3-2023
python -m venv venv
source venv/bin/activate
pip install -r  requirements.txt
```
4. Give it a whirl
```
python scraper.py
```

Given the right parameters, this script will output a CSV in the top directory of this package.

To run again, navigate to your directory (.../Indeed-Scraper-v3-2023) and execute the following:
```
source venv/bin/activate
pip install -r  requirements.txt
```
