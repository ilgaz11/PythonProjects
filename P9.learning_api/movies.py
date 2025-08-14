from requests import get, post
import json, textwrap


def search_item():
    title = input("Search By Title: ")
    title_url = "".join(["+" if item == " " else item for item in title])
    response = get(f"http://www.omdbapi.com/?apikey=6f27363&t={title_url}&plot=full")
    json_result = json.loads(response.content)
    if json_result["Response"] == "False":
        print("Movie or show not found")
    else:
        main_info(json_result)
        test_bool = True
        while test_bool:
            print("0 - Quit\n1 - View Cast\n2 - View Description")
            test_bool = extra_info(json_result)
            print("")
    

def main_info(data):
    if data["Type"] == "series":
        time_info = f"Seasons: {data["totalSeasons"]}"
        year = f"Years: {data["Year"]}"
    elif data["Type"] == "movie":
        time_info = f"Runtime: {data["Runtime"]}" 
        year = f"Release date: {data["Released"][-4:]}"
    print(f"Title: {data['Title']} \n{year}\n{time_info}\nRating: {data["imdbRating"]}")
    print("")

def extra_info(data):
    command = input("Command: ")
    print("")
    if command == "0":
        return False
    elif command == "1":
        director = data["Director"] if data["Director"] != "N/A" else data["Writer"]
        cast = data["Actors"]
        print(f" - Director/Writer: {director}\n - Cast: {cast}")
    elif command == "2":
        formatted_plot = textwrap.fill(data["Plot"], width=85)
        print(f" - Genre: {data["Genre"]}\n - Plot: {formatted_plot}")
    else:
        print("Invalid command")
    return True


if __name__ == "__main__":
    while True:
        search_item()