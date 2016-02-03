# -*- coding: utf-8 -*-
import sys
import time
import httplib2

AUTO_RECONNECT_TIMES = 5

crawl_tips_json = {}

SERVER = 'http://api.cn.faceplusplus.com/'

category_Arts_Entertainment = ['Aquarium', 'Arcade', 'Art Gallery', 'Bowling Alley', 'Casino', 'Circus', 'Comedy Club',
                               'Concert Hall', 'Country Dance Club', 'Disc Golf', 'General Entertainment',
                               'Go Kart Track', 'Historic Site', 'Laser Tag', 'Mini Golf', 'Movie Theater',
                               'Indie Movie Theater', 'Multiplex', 'Museum', 'Art Museum', 'Erotic Museum',
                               'History Museum', 'Planetarium', 'Science Museum', 'Music Venue', 'Jazz Club',
                               'Piano Bar', 'Rock Club', 'Performing Arts Venue', 'Dance Studio', 'Indie Theater',
                               'Opera House', 'Theater', 'Pool Hall', 'Public Art', 'Outdoor Sculpture', 'Street Art',
                               'Racetrack', 'Roller Rink', 'Salsa Club', 'Stadium', 'Baseball Stadium',
                               'Basketball Stadium', 'Cricket Ground', 'Football Stadium', 'Hockey Arena',
                               'Soccer Stadium', 'Tennis Stadium', 'Track Stadium', 'Threet Art', 'Theme Park',
                               'Theme Park Ride / Attraction', 'Water Park', 'Zoo']

category_College_University = ['College Academic Building', 'College Arts Building', 'College Communications Building',
                               'College Engineering Building', 'College History Building', 'College Math Building',
                               'College Science Building', 'College Technology Building',
                               'College Administrative Building', 'College Auditorium', 'College Bookstore',
                               'College Cafeteria', 'College Classroom', 'College Gym', 'College Lab',
                               'College Library', 'College Quad', 'College Rec Center', 'College Residence Hall',
                               'College Stadium', 'College Baseball Diamond', 'College Basketball Court',
                               'College Cricket Pitch', 'College Football Field', 'College Hockey Rink',
                               'College Soccer Field', 'College Tennis Court', 'College Track', 'College Theater',
                               'Community College', 'Fraternity House', 'General College & University', 'Law School',
                               'Medical School', 'Sorority House', 'Student Center', 'Trade School', 'University']

category_Event = ['Conference', 'Convention', 'Festival', 'Music Festival', 'Other Event', 'Parade', 'Stoop Sale',
                  'Street Fair']

male_tipping_duration = []

female_tipping_duration = []

all_tip_timestamp = {}

category_Food = ['Afghan Restaurant', 'African Restaurant', 'Ethiopian Restaurant', 'American Restaurant',
                 'New American Restaurant', 'Arepa Restaurant', 'Argentinian Restaurant', 'Asian Restaurant',
                 'Dim Sum Restaurant', 'Donburi Restaurant', 'Japanese Curry Restaurant', 'Kaiseki Restaurant',
                 'Kushikatsu Restaurant', 'Monjayaki Restaurant', 'Nabe Restaurant', 'Okonomiyaki Restaurant',
                 'Ramen Restaurant', 'Shabu-Shabu Restaurant', 'Soba Restaurant', 'Sukiyaki Restaurant',
                 'Takoyaki Place', 'Tempura Restaurant', 'Tonkatsu Restaurant', 'Udon Restaurant', 'Unagi Restaurant',
                 'Wagashi Place', 'Yakitori Restaurant', 'Yoshoku Restaurant', 'Korean Restaurant',
                 'Malaysian Restaurant', 'Mongolian Restaurant', 'Noodle House', 'Thai Restaurant',
                 'Tibetan Restaurant', 'Vietnamese Restaurant', 'Australian Restaurant', 'Austrian Restaurant',
                 'BBQ Joint', 'Bagel Shop', 'Bakery', 'Belarusian Restaurant', 'Belgian Restaurant', 'Bistro',
                 'Brazilian Restaurant', 'Acai House', 'Baiano Restaurant', 'Central Brazilian Restaurant',
                 'Churrascaria', 'Empada House', 'Goiano Restaurant', 'Mineiro Restaurant',
                 'Northeastern Brazilian Restaurant', 'Northern Brazilian Restaurant', 'Pastelaria',
                 'Southeastern Brazilian Restaurant', 'Southern Brazilian Restaurant', 'Tapiocaria', 'Breakfast Spot',
                 'Bubble Tea Shop', 'Buffet', 'Burger Joint', 'Burrito Place', 'Cafeteria', u'Café',
                 'Cajun / Creole Restaurant', 'Cambodian Restaurant', 'Caribbean Restaurant', 'Caucasian Restaurant',
                 'Chinese Restaurant', 'Anhui Restaurant', 'Beijing Restaurant', 'Cantonese Restaurant',
                 'Chinese Aristocrat Restaurant', 'Chinese Breakfast Place', 'Dongbei Restaurant', 'Fujian Restaurant',
                 'Guizhou Restaurant', 'Hainan Restaurant', 'Hakka Restaurant', 'Henan Restaurant',
                 'Hong Kong Restaurant', 'Huaiyang Restaurant', 'Hubei Restaurant', 'Hunan Restaurant',
                 'Imperial Restaurant', 'Jiangsu Restaurant', 'Jiangxi Restaurant', 'Macanese Restaurant',
                 'Manchu Restaurant', 'Peking Duck Restaurant', 'Shaanxi Restaurant', 'Shandong Restaurant',
                 'Shanghai Restaurant', 'Shanxi Restaurant', 'Szechuan Restaurant', 'Taiwanese Restaurant',
                 'Tianjin Restaurant', 'Xinjiang Restaurant', 'Yunnan Restaurant', 'Zhejiang Restaurant', 'Coffee Shop',
                 'Comfort Food Restaurant', 'Creperie', 'Cuban Restaurant', 'Cupcake Shop', 'Czech Restaurant',
                 'Deli / Bodega', 'Dessert Shop', 'Dim Sum Restaurant', 'Diner', 'Distillery', 'Donut Shop',
                 'Dumpling Restaurant', 'Eastern European Restaurant', 'English Restaurant', 'Ethiopian Restaurant',
                 'Falafel Restaurant', 'Fast Food Restaurant', 'Filipino Restaurant', 'Fish & Chips Shop',
                 'Fondue Restaurant', 'Food Truck', 'French Restaurant', 'Fried Chicken Joint', 'Gastropub',
                 'German Restaurant', 'Gluten-free Restaurant', 'Greek Restaurant', 'Bougatsa Shop',
                 'Cretan Restaurant', 'Fish Taverna', 'Grilled Meat Restaurant', 'Kafenio', 'Magirio',
                 'Meze Restaurant', 'Modern Greek Restaurant', 'Ouzeri', 'Patsa Restaurant', 'Taverna',
                 'Tsipouro Restaurant', 'Halal Restaurant', 'Hawaiian Restaurant', 'Himalayan Restaurant',
                 'Hot Dog Joint', 'Hotpot Restaurant', 'Hungarian Restaurant', 'Ice Cream Shop', 'Indian Restaurant',
                 'Indonesian Restaurant', 'Acehnese Restaurant', 'Balinese Restaurant', 'Betawinese Restaurant',
                 'Javanese Restaurant', 'Manadonese Restaurant', 'Meatball Place', 'Padangnese Restaurant',
                 'Sundanese Restaurant', 'Irish Pub', 'Italian Restaurant', 'Japanese Restaurant', 'Jewish Restaurant',
                 'Juice Bar', 'Korean Restaurant', 'Kosher Restaurant', 'Latin American Restaurant',
                 'Empanada Restaurant', 'Mac & Cheese Joint', 'Malaysian Restaurant', 'Mediterranean Restaurant',
                 'Mexican Restaurant']

category_Food.extend(['Middle Eastern Restaurant', 'Modern European Restaurant', 'Molecular Gastronomy Restaurant',
                      'Mongolian Restaurant', 'Moroccan Restaurant', 'New American Restaurant', 'Pakistani Restaurant',
                      'Persian Restaurant', 'Peruvian Restaurant', 'Pie Shop', 'Pizza Place', 'Polish Restaurant',
                      'Portuguese Restaurant', 'Ramen / Noodle House', 'Restaurant', 'Romanian Restaurant',
                      'Russian Restaurant', 'Blini House', 'Pelmeni House', 'Salad Place', 'Sandwich Place',
                      'Scandinavian Restaurant', 'Seafood Restaurant', 'Snack Place', 'Soup Place',
                      'South American Restaurant', 'Southern / Soul Food Restaurant', 'Souvlaki Shop',
                      'Spanish Restaurant', 'Paella Restaurant', 'Steakhouse', 'Sushi Restaurant', 'Swiss Restaurant',
                      'Taco Place', 'Tapas Restaurant', 'Tatar Restaurant', 'Tea Room', 'Thai Restaurant',
                      'Tibetan Restaurant', 'Turkish Restaurant', 'Borek Place', 'Cigkofte Place', 'Doner Restaurant',
                      'Gozleme Place', 'Home Cooking Restaurant', 'Kebab Restaurant', 'Kofte Place',
                      u'Kokoreç Restaurant', 'Manti Place', 'Meyhane', 'Pide Place', 'Ukrainian Restaurant',
                      'Varenyky restaurant', 'West-Ukrainian Restaurant', 'Vegetarian / Vegan Restaurant',
                      'Vietnamese Restaurant', 'Winery', 'Wings Joint', 'Frozen Yogurt', 'Friterie',
                      'Andhra Restaurant', 'Awadhi Restaurant', 'Bengali Restaurant', 'Chaat Place',
                      'Chettinad Restaurant', 'Dhaba', 'Dosa Place', 'Goan Restaurant', 'Gujarati Restaurant',
                      'Indian Chinese Restaurant', 'Indian Sweet Shop', 'Irani Cafe', 'Jain Restaurant',
                      'Karnataka Restaurant', 'Kerala Restaurant', 'Maharashtrian Restaurant', 'Mughlai Restaurant',
                      'Multicuisine Indian Restaurant', 'North Indian Restaurant', 'Northeast Indian Restaurant',
                      'Parsi Restaurant', 'Punjabi Restaurant', 'Rajasthani Restaurant', 'South Indian Restaurant',
                      'Udupi Restaurant', 'Indonesian Meatball Place', 'Abruzzo', 'Turkish Home Cooking Restaurant',
                      'Sri Lankan Restaurant', 'Veneto Restaurant', 'Umbrian Restaurant', 'Tuscan Restaurant',
                      'Trentino Restaurant', 'Trattoria/Osteria', 'South Tyrolean Restaurant', 'Sicilian Restaurant',
                      'Sardinian Restaurant', 'Roman Restaurant', 'Romagna Restaurant', 'Rifugio di Montagna',
                      'Puglia Restaurant', 'Piedmontese Restaurant', 'Piadineria', 'Molise Restaurant',
                      'Marche Restaurant', 'Malga', 'Lombard Restaurant', 'Ligurian Restaurant', 'Friuli Restaurant',
                      'Emilia Restaurant', 'Campanian Restaurant', 'Calabria Restaurant', 'Basilicata Restaurant',
                      'Aosta Restaurant', 'Agriturismo', 'Abruzzo Restaurant', ''])

category_Nightlife_Spot = ['Bar', 'Beach Bar', 'Beer Garden', 'Brewery', 'Champagne Bar', 'Cocktail Bar', 'Dive Bar',
                           'Gay Bar', 'Hookah Bar', 'Hotel Bar', 'Karaoke Bar', 'Lounge', 'Night Market', 'Nightclub',
                           'Other Nightlife', 'Pub', 'Sake Bar', 'Speakeasy', 'Sports Bar', 'Strip Club', 'Whisky Bar',
                           'Wine Bar', 'Speakeasy']

category_Outdoors_Recreation = ['Athletics & Sports', 'Badminton Court', 'Baseball Field', 'Basketball Court',
                                'Bowling Green', 'Golf Course', 'Hockey Field', 'Paintball Field', 'Rugby Pitch',
                                'Skate Park', 'Skating Rink', 'Soccer Field', 'Sports Club', 'Squash Court',
                                'Tennis Court', 'Volleyball Court', 'Bath House', 'Bathing Area', 'Beach',
                                'Nudist Beach', 'Surf Spot', 'Botanical Garden', 'Bridge', 'Campground', 'Castle',
                                'Cemetery', 'Dive Spot', 'Dog Run', 'Farm', 'Field', 'Fishing Spot', 'Forest', 'Garden',
                                'Gun Range', 'Harbor / Marina', 'Hot Spring', 'Island', 'Lake', 'Lighthouse',
                                'Mountain', 'National Park', 'Nature Preserve', 'Other Great Outdoors', 'Palace',
                                'Park', 'Pedestrian Plaza', 'Playground', 'Plaza', 'Pool', 'Rafting',
                                'Recreation Center', 'River', 'Rock Climbing Spot', 'Scenic Lookout',
                                'Sculpture Garden', 'Ski Area', 'Apres Ski Bar', 'Ski Chairlift', 'Ski Chalet',
                                'Ski Lodge', 'Ski Trail', 'Stables', 'States & Municipalities', 'City', 'County',
                                'Country', 'Neighborhood', 'State', 'Town', 'Village', 'Summer Camp', 'Trail', 'Tree',
                                'Vineyard', 'Volcano', 'Well']

category_Professional_Other_Places = ['Animal Shelter', 'Auditorium', 'Building', 'Club House', 'Community Center',
                                      'Convention Center', 'Meeting Room', 'Cultural Center', 'Distribution Center',
                                      'Event Space', 'Factory', 'Fair', 'Funeral Home', 'Government Building',
                                      'Capitol Building', 'City Hall', 'Courthouse', 'Embassy / Consulate',
                                      'Fire Station', 'Monument / Landmark', 'Police Station', 'Town Hall', 'Library',
                                      'Medical Center', 'Acupuncturist', 'Alternative Healer', 'Chiropractor',
                                      "Dentist's Office",  "Doctor's Office",  'Emergency Room', 'Eye Doctor',
                                      'Hospital', 'Laboratory', 'Mental Health Office', 'Veterinarian', 'Military Base',
                                      'Non-Profit', 'Office', 'Advertising Agency', 'Campaign Office',
                                      'Conference Room', 'Coworking Space', 'Tech Startup', 'Parking', 'Post Office',
                                      'Prison', 'Radio Station', 'Recruiting Agency', 'School', 'Circus School',
                                      'Driving School', 'Elementary School', 'Flight School', 'High School',
                                      'Language School', 'Middle School', 'Music School', 'Nursery School', 'Preschool',
                                      'Private School', 'Religious School', 'Swim School', 'Social Club',
                                      'Spiritual Center', 'Buddhist Temple', 'Church', 'Hindu Temple', 'Monastery',
                                      'Mosque', 'Prayer Room', 'Shrine', 'Synagogue', 'Temple', 'TV Station',
                                      'Voting Booth', 'Warehouse']

category_Residence = ['Assisted Living', 'Home (private)', 'Housing Development',
                      'Residential Building (Apartment / Condo)', 'Trailer Park']

category_Shop_Service = ['Construction & Lanscape', 'Event Service', 'ATM', 'Adult Boutique', 'Antique Shop',
                         'Arts & Crafts Store', 'Astrologer', 'Auto Garage', 'Automotive Shop', 'Baby Store', 'Bank',
                         'Betting Shop', 'Big Box Store', 'Bike Shop', 'Board Shop', 'Bookstore', 'Bridal Shop',
                         'Camera Store', 'Candy Store', 'Car Dealership', 'Car Wash', 'Carpet Store',
                         'Check Cashing Service', 'Chocolate Shop', 'Christmas Market', 'Clothing Store',
                         'Accessories Store', 'Boutique', 'Kids Store', 'Lingerie Store', "Men's Store",
                         'Shoe Store', "Women's Store", 'Comic Shop', 'Convenience Store', 'Cosmetics Shop',
                         'Costume Shop', 'Credit Union', 'Daycare', 'Department Store', 'Design Studio',
                         'Discount Store', 'Dive Shop', 'Drugstore / Pharmacy', 'Dry Cleaner', 'EV Charging Station',
                         'Electronics Store', 'Fabric Shop', 'Financial or Legal Service', 'Fireworks Store',
                         'Fishing Store', 'Flea Market', 'Flower Shop', 'Food & Drink Shop', 'Beer Store', 'Butcher',
                         'Cheese Shop', 'Farmers Market', 'Fish Market', 'Food Court', 'Gourmet Shop', 'Grocery Store',
                         'Health Food Store', 'Liquor Store', 'Organic Grocery', 'Street Food Gathering', 'Supermarket',
                         'Wine Shop', 'Frame Store', 'Fruit & Vegetable Store', 'Furniture / Home Store', 'Gaming Cafe',
                         'Garden Center', 'Gas Station / Garage', 'Gift Shop', 'Gun Shop', 'Gym / Fitness Center',
                         'Boxing Gym', 'Climbing Gym', 'Cycle Studio', 'Gym Pool', 'Gymnastics Gym', 'Gym',
                         'Martial Arts Dojo', 'Track', 'Yoga Studio', 'Hardware Store', 'Herbs & Spices Store',
                         'Hobby Shop', 'Hunting Supply', 'IT Services', 'Internet Cafe', 'Jewelry Store',
                         'Knitting Store', 'Laundromat', 'Laundry Service', 'Lawyer', 'Leather Goods Store',
                         'Locksmith', 'Lottery Retailer', 'Luggage Store', 'Mall', 'Marijuana Dispensary', 'Market',
                         'Massage Studio', 'Mattress Store', 'Miscellaneous Shop', 'Mobile Phone Shop',
                         'Motorcycle Shop', 'Music Store', 'Nail Salon', 'Newsstand', 'Optical Shop',
                         'Other Repair Shop', 'Outdoor Supply Store', 'Outlet Store', 'Paper / Office Supplies Store',
                         'Pawn Shop', 'Perfume Shop', 'Pet Service', 'Pet Store', 'Photography Lab', 'Piercing Parlor',
                         'Pop-Up Shop', 'Print Shop', 'Real Estate Office', 'Record Shop', 'Recording Studio',
                         'Recycling Facility', 'Salon / Barbershop', 'Shipping Store', 'Shoe Repair', 'Smoke Shop',
                         'Smoothie Shop', 'Souvenir Shop', 'Spa', 'Sporting Goods Shop', 'Stationery Store',
                         'Storage Facility', 'Tailor Shop', 'Tanning Salon', 'Tattoo Parlor', 'Thrift / Vintage Store',
                         'Toy / Game Store', 'Travel Agency', 'Used Bookstore', 'Video Game Store', 'Video Store',
                         'Warehouse Store', 'Watch Repair Shop']

category_Travel_Transport = ['Cruise', 'Metro Station', 'Transportation Service', 'Airport', 'Airport Food Court',
                             'Airport Gate', 'Airport Lounge', 'Airport Terminal', 'Airport Tram', 'Plane',
                             'Bike Rental / Bike Share', 'Boat or Ferry', 'Border Crossing', 'Bus Station', 'Bus Line',
                             'Bus Stop', 'Cable Car', 'General Travel', 'Hotel', 'Bed & Breakfast', 'Boarding House',
                             'Hostel', 'Hotel Pool', 'Motel', 'Resort', 'Roof Deck', 'Intersection', 'Light Rail',
                             'Moving Target', 'Pier', 'RV Park', 'Rental Car Location', 'Rest Area', 'Road', 'Street',
                             'Subway', 'Taxi Stand', 'Taxi', 'Toll Booth', 'Toll Plaza', 'Tourist Information Center',
                             'Train Station', 'Platform', 'Train', 'Tram', 'Travel Lounge', 'Tunnel']



reload(sys)
sys.setdefaultencoding('utf-8')
h = httplib2.Http(disable_ssl_certificate_validation=True)


def get_raw_info(url):
    success = 0
    retry = 0
    content = -1
    while success == 0:
        try:
            resp, content = h.request(url, "GET")
            success = 1
            if resp['status'] != '200':
                return -1
        except:
            time.sleep(3)
            retry += 1
            if retry == AUTO_RECONNECT_TIMES:
                return -2
    return content
