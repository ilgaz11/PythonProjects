from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":"  + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    #print(json_result)
    if len(json_result) == 0:
        print("No artist found...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit=20"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def get_album_tracklist(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks?limit=30"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def get_user(token):
    url = f"https://api.spotify.com/v1/me/top/artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def album_info(token, ids_list: list, titles_list: list):
    try:
        get_index = int(input("Enter album index: "))
        print(f"\nTitle: {titles_list[get_index - 1]}")
        print("\nTracklist:")
        tracks = get_album_tracklist(token, ids_list[get_index - 1])
        for idx, song in enumerate(tracks):
            print(f"{f'{idx + 1}.':3} {song["name"]}")
        print("")
    except ValueError:
        print("Invalid index")
    except IndexError:
        print("Index out of range")

#for user interface program
def search_loop(artist_name):
    token = get_token()
    result = search_for_artist(token, artist_name)
    artist_id = result["id"]
    return result

def get_songs(artist_id):
    token = get_token()
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    songs = "\n\n".join([f"{idx + 1:2}. {song['name'][:35]}" for idx, song in enumerate(json_result)])
    return songs

#not finished
def get_albums(artist_id):
    token = get_token()
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit=20"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    albums = "\n\n".join([])
    return json_result


def main():
    token = get_token()

    while True:
        artist_name = input("Search for an artist: ")
        result = search_for_artist(token, artist_name)
        artist_id = result["id"]
        command = input("0 - Return to search\n1 - Top Songs\n2 - Albums\nCommand: ")
        if command == "0":
            continue
        elif command == "1":
            print("\nTop Songs:")
            songs = get_songs_by_artist(token, artist_id)

            for idx, song in enumerate(songs):
                print(f"{idx + 1}. {song['name']}")
            print("")

        elif command == "2":
            albums = get_albums_by_artist(token, artist_id)

            print("")
            print(f"{"Index":7} {"Year":8} Title")
            print("-"*40)
            album_ids = []
            album_titles = []
            index = 1
            for idx, album in enumerate(albums):
                if album["album_type"] == "album":
                    if album["artists"][0]["name"].lower() == artist_name.lower():
                        print(f"  {index:<5} {album["release_date"][:4]:8} {album['name']}")
                        album_ids.append(album["id"])
                        album_titles.append(album['name'])
                        index += 1
            print("")
            while True:
                alb_command = input("0 - Return to search\n1 - Get album tracklist\nCommand: ")
                print("")
                if alb_command == "0":
                    break
                elif alb_command == "1":
                    album_info(token, album_ids, album_titles)
                else: 
                    print("Invalid input")
                print("")


if __name__ == "__main__":
    main()