# OBJECTIVE:  Get all images (not in carousel) from a user's profile page, download it, 
#             send it to AlTrollan API to make user transition to the platform easier.


import instagrapi
import datetime
import sys
import json
import requests
import os


# Create a new instance of the Client class
client = instagrapi.Client()

# Login to Instagram
username = 'divasavum.troll'
password = 'hellothere!'

print('Logging in as ', username, '...')

try:
    client.login(username=username, password=password)
    print('Successfully logged in!')

except Exception:
    print('Login Failed!')
    sys.exit()

altrollan_id = ''                    #fill it with req altrollan id
insta_username = 'abhijithkonnayil'  #fill it with corresponding instagram id
print('Visiting the profile page of ', insta_username)

dir_to_store_photos = ''

try:
    user = client.user_info_by_username(insta_username)
    print('Profile page found!')

    dir_to_store_photos = './'+insta_username
    if not os.path.exists(dir_to_store_photos):
        os.makedirs(dir_to_store_photos)
        print('Photos will be saved the directory: '+ insta_username)

except:
    print('Profile page not found!')
    sys.exit()

user_id = user.pk

#print('User details is: ',user.dict());

num_posts_to_extract = user.media_count
user_media = client.user_medias(user_id, num_posts_to_extract)

post_count = 1

for media in user_media:

    media_date = media.taken_at.date()
    date_to_consider = datetime.date.today()
    print('\n\t\t\tIMAGE URL IN POST NO:', post_count, '\n')
    print(media.thumbnail_url)

    if(media_date == date_to_consider or True):  

        #c = media
        #url = c.thumbnail_url.scheme+'://'+c.thumbnail_url.host+c.thumbnail_url.path+'?'+c.thumbnail_url.query
        url = media.thumbnail_url

        if url is not None:
            response = requests.get(url)
            image_path = dir_to_store_photos+'/image '+str(post_count)+'.jpg'
            with open(image_path, 'wb') as f:
                f.write(response.content)


            #Sending Image to Altrollan API
            api_url = 'fill_with_api_end_point'
            data = {
                'instagram_username' : insta_username,
                'instagram_id'       : user_id,
                'altrollan_id'       : altrollan_id,
            }
            files = {'image': response.content}

            response = requests.post(url, data = data, files=files)

            if response.status_code == 200: 
                print('API Request Successful')
            else:
                print('API Request Failed')

        ##-----------to get all photos if the post is a carousal type -> multiple photos in one post
        ##if media.thumbnail_url is None -> it is a carousal
        #else:
        #    count = 1
        #    for resource in media.resources:

        #        if resource.media_type == 1: #to consider only imags
                    
        #            print(resource.thumbnail_url)
        #            response = requests.get(resource.thumbnail_url)
        #            image_path = 'image '+str(post_count)+'-'+str(count)+'.jpg'
        #            with open(image_path, 'wb') as f:
        #                f.write(response.content)
        #            count += 1

    post_count += 1
