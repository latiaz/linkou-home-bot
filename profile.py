import pygsheets
import requests


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
            user_all = [[str(d['displayName']), str(d['userId']), str(d['statusMessage']), str(d['pictureUrl'])] for d in user_list]
            profile = [data['displayName'], data['userId'], data['statusMessage'] if data['statusMessage'] is not None else '', data['pictureUrl']]
            user_all.append(profile)
            wks_user.update_values('A2', user_all)
        else:
            pass


if __name__ == "__main__":
    user = 'Ub4a5a2457645d5fe2314da679b937049'
    user_profile(user)
