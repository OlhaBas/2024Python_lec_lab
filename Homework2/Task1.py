import requests
import pprint
import csv
from datetime import datetime, timedelta
from collections import defaultdict

class DataAnalysisTool:
    def __init__(self, pages):
        self.pages = pages
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
        }
        self.genres = self._fetch_genres()

    def _fetch_genres(self):
        url = f"{self.base_url}/genre/movie/list?language=en"
        response = requests.get(url, headers=self.headers)
        genres_data = response.json()["genres"]
        genres = {genre["id"]: genre["name"] for genre in genres_data}
        return genres

    def fetch_data(self):
        all_data = []
        for page_num in range(1, self.pages + 1):
            url = f"{self.base_url}/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={page_num}"
            response = requests.get(url, headers=self.headers)
            data = response.json()["results"]
            all_data.extend(data)
        return all_data

    def get_all_data(self):
        return self.fetch_data()

    def get_data_with_indexes(self, start, end, step):
        all_data = self.fetch_data()
        return all_data[start:end:step]

    def get_most_popular_title(self):
        all_data = self.fetch_data()
        most_popular = max(all_data, key=lambda x: x["popularity"])
        return most_popular["title"]

    def get_titles_with_keywords(self, keywords):
        all_data = self.fetch_data()
        matching_titles = [movie["title"] for movie in all_data if any(keyword in movie["overview"] for keyword in keywords)]
        return matching_titles

    def get_unique_genres(self):
        return set(self.genres.values())

    def delete_movies_by_genre(self, genre_id):
        all_data = self.fetch_data()
        filtered_data = [movie for movie in all_data if genre_id not in movie["genre_ids"]]
        return filtered_data

    def get_most_popular_genres(self):
        all_data = self.fetch_data()
        genre_count = defaultdict(int)
        for movie in all_data:
            for genre_id in movie["genre_ids"]:
                genre_count[genre_id] += 1
        popular_genres = [(self.genres[genre_id], count) for genre_id, count in sorted(genre_count.items(), key=lambda x: x[1], reverse=True)]
        return popular_genres

    def group_titles_by_genre(self):
        all_data = self.fetch_data()
        grouped_titles = defaultdict(list)
        for movie in all_data:
            for genre_id in movie["genre_ids"]:
                grouped_titles[genre_id].append(movie["title"])
        return grouped_titles

    def replace_genre_id(self):
        all_data = self.fetch_data()
        modified_data = all_data.copy()
        for movie in modified_data:
            movie["genre_ids"][0] = 22
        return all_data, modified_data

    def _last_day_in_cinema(self, release_date):
        release_date = datetime.strptime(release_date, "%Y-%m-%d")
        last_day = release_date + timedelta(days=77)  # 2 months and 2 weeks
        return last_day.strftime("%Y-%m-%d")

    def _format_movie(self, movie):
        return {
            "Title": movie["title"],
            "Popularity": round(movie["popularity"], 1),
            "Score": int(movie["vote_average"]),
            "Last_day_in_cinema": self._last_day_in_cinema(movie["release_date"])
        }

    def get_sorted_movie_data(self):
        all_data = self.fetch_data()
        sorted_data = sorted(all_data, key=lambda x: (int(x["vote_average"]), x["popularity"]), reverse=True)
        formatted_data = [self._format_movie(movie) for movie in sorted_data]
        return formatted_data

    def write_to_csv(self, data, file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Title", "Popularity", "Score", "Last_day_in_cinema"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for movie in data:
                writer.writerow(movie)

# Используем функции и печатем то что мы там наполучали
tool = DataAnalysisTool(pages=3)

print("Most Popular Title:")
print(tool.get_most_popular_title())
print("\nTitles with Keywords 'action' or 'adventure':")
pprint.pprint(tool.get_titles_with_keywords(["action", "adventure"]))
print("\nUnique Genres:")
pprint.pprint(tool.get_unique_genres())
print("\nMost Popular Genres:")
pprint.pprint(tool.get_most_popular_genres())
print("\nGrouped Titles by Genre:")
pprint.pprint(tool.group_titles_by_genre())
data = tool.get_sorted_movie_data()
tool.write_to_csv(data, "movie_data.csv")
