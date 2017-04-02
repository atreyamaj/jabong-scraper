from bs4 import BeautifulSoup
import requests
import re
import sys
import csv
import time

count = 0
start_time = time.time()
process = 0

with open('jabong.csv', 'w') as csvfile:

	# Start writing the CSV File
	jabongwriter = csv.writer(csvfile, delimiter=',')
	jabongwriter.writerow(['ID', 'Title', 'Original Price', 'Discounted Price', 'URL'])
	csvfile.flush()

	# Choose the number of requests to the webpage
	for i in range(1,300):
		# Request the webpage using requests 'GET' request
		r = requests.get('http://www.jabong.com/men/clothing/polos-tshirts/?sort=popularity&dir=desc&source=topnav_men&limit=1015&page='+str(i))
		data = r.text

		# Calculate Processing Time
		process = 0
		start_process = 0
		end_process = 0

		# Initialise Process time
		start_process = time.time()

		# Declare the Beautiful Soup instance using lxml parser
		soup = BeautifulSoup(data, "lxml")

		# Find the div item for search products
		items = soup.find_all("section", class_="row search-product animate-products")

		# Find the div item for product information
		products = soup.find_all("div", class_="product-info")

		# Link to append for relative links in the item URL
		link = "http://www.jabong.com/men/clothing/polos-tshirts"

		# Used to iterate through all the items fetched in the products 
		for product in products:

			# Find the title of each product
			title = product.find('div', class_='h4')
			title_list = title.text
			title_list = unicode(title_list).encode('utf-8')

			# Initialize strings for MRP Price and Discounted Price
			mrp_price = ""
			discounted_price = ""

			# Find the two prices in the div 
			price = product.find('div', class_="price")
			parent = price.find_all('span')
			standard_price = product.find_all('span', class_='standard-price')

			# If Standard Price div is empty, it means that a dummy object has been inserted
			if len(standard_price) != 0:
				# The first value in the standard price list is the MRP Price
				mrp_price = standard_price[0].string
				mrp_price = unicode(mrp_price).encode('utf-8')
				
				# If the Standard Price List has two items, then it also contains a discount
				if len(standard_price) == 2:
					discounted_price = standard_price[1].string
					discounted_price = unicode(discounted_price).encode('utf-8')
				# Else, it does not have a discounted price
				else:
				    discounted_price = standard_price[0].string
				    discounted_price = unicode(discounted_price).encode('utf-8')
				
				# Get the URL Link for the given product
				url_link = link + str(product.parent.get('href'))
				url_link = unicode(url_link).encode('utf-8')
				print("count = " + str(count))

				# An ID of the product to be fetched
				id_item = product.parent.parent.get('data-product-id')
				id_item = unicode(id_item).encode('utf-8')

				# If no ID is given that means it is a dummy item
				if id_item == None:
					continue
				# If an ID is present it means that it means 
				else:
					jabongwriter.writerow([id_item, title_list, mrp_price, discounted_price, url_link])
					csvfile.flush()

				# Increment count to limit it till 10000
				count += 1		

				# If count == 10000, then limit is reached
				if count == 10000:
					end_time = time.time()
					# List out total what all information
					print("Total of " + str(count) + " items taken")
					print("Total time is: " + str(end_time-start_time))
					sys.exit(0)
				# Else keep on iterating till limit is reached
				else:
					continue

		# Processing time calculation
		end_process = time.time()
		process += (end_process - start_process)
		print("Process time for this cycle is: " + str(end_process-start_process))


