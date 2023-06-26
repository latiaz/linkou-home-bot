import pygsheets
import requests
import os
import random
import string


def user_profile(user):
    channel_access_token = 'S8+kgGvknCXVLDKMWgOZqGc+MLPS+fyaf8TWtLthWzU2mWPBEG9R+NAhEWKzQvrTFlbhFut+9Fwt+54sz0Fz8AnVN5AG7QNEGu6DvKEPyJPnEP6eWHDAYML3BJCOLOrk19eYJVR6XGv+o3yMfM/39wdB04t89/1O/w1cDnyilFU='
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')
    wks_user = linkou.worksheet_by_title('user')
    user_list = wks_user.get_all_records()
    for item in user_list:
        if item['userId'] == user:
            break
    else:
        url = f"https://api.line.me/v2/bot/profile/{user}"
        headers = {
            'Authorization': f'Bearer {channel_access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            user_all = [[str(d['displayName']), str(d['userId']), str(d['statusMessage']), str(d['pictureUrl'])] for d
                        in user_list]
            status_message = data.get('statusMessage', '')
            picture_url = data.get('pictureUrl', '')
            profile = [data['displayName'], data['userId'], status_message, picture_url]
            user_all.append(profile)
            wks_user.update_values('A2', user_all)
        else:
            pass


def download_profile():
    channel_access_token = 'S8+kgGvknCXVLDKMWgOZqGc+MLPS+fyaf8TWtLthWzU2mWPBEG9R+NAhEWKzQvrTFlbhFut+9Fwt+54sz0Fz8AnVN5AG7QNEGu6DvKEPyJPnEP6eWHDAYML3BJCOLOrk19eYJVR6XGv+o3yMfM/39wdB04t89/1O/w1cDnyilFU='
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')
    wks_user = linkou.worksheet_by_title('user')
    user_list = wks_user.get_all_records()
    # print(user_list)
    for item in user_list:
        picture_url = item['pictureUrl']
        user_id = item['userId']
        file_name = '/Users/leohuang/Pictures/price/' + user_id + '.jpg'
        if picture_url == '':
            url = f"https://api.line.me/v2/bot/profile/{user_id}"
            headers = {
                'Authorization': f'Bearer {channel_access_token}'
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                picture_url = data.get('pictureUrl', '')
                file_name = '/Users/leohuang/Pictures/price/' + user_id + '-' + generate_random_code(5) + '.jpg'
                if picture_url == '':
                    print(f"{user_id} has no pictureUrl")
                else:
                    response = requests.get(picture_url)
                    if response.status_code == 200:
                        with open(file_name, 'wb') as file:
                            file.write(response.content)
                        print(f"{user_id} downloaded")
                        print(picture_url)
            else:
                pass
        else:
            response = requests.get(picture_url)
            if response.status_code == 200:
                if os.path.exists(file_name):
                    print(f"{user_id} exists")
                    continue
                else:
                    with open(file_name, 'wb') as file:
                        file.write(response.content)
                    print(f"{user_id} downloaded")
            elif response.status_code == 404:
                url = f"https://api.line.me/v2/bot/profile/{user_id}"
                headers = {
                    'Authorization': f'Bearer {channel_access_token}'
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    picture_url = data.get('pictureUrl', '')
                    file_name = '/Users/leohuang/Pictures/price/' + user_id + '-' + generate_random_code(5) + '.jpg'
                    if picture_url == '':
                        print(f"{user_id} has no pictureUrl")
                    else:
                        response = requests.get(picture_url)
                        if response.status_code == 200:
                            with open(file_name, 'wb') as file:
                                file.write(response.content)
                            print(f"{user_id} downloaded")
                            print(picture_url)
                else:
                    pass


def generate_random_code(length):
    digits = string.digits
    code = ''.join(random.choice(digits) for _ in range(length))
    return code


if __name__ == "__main__":
    # user = 'Ub4a5a2457645d5fe2314da679b937049'
    # user_profile(user)
    download_profile()
