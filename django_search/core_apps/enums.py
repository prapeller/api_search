from enum import Enum


class GenresNamesEnum(str, Enum):
    action = "Action"
    adventure = "Adventure"
    fantasy = "Fantasy"
    sci_fi = "Sci - Fi"
    drama = "Drama"
    music = "Music"
    romance = "Romance"
    thriller = "Thriller"
    mystery = "Mystery"
    comedy = "Comedy"
    animation = "Animation"
    family = "Family"
    biography = "Biography"
    musical = "Musical"
    crime = "Crime"
    short = "Short"
    western = "Western"
    documentary = "Documentary"
    history = "History"
    war = "War"
    game_show = "Game - Show"
    reality_tv = "Reality - TV"
    horror = "Horror"
    sport = "Sport"
    talk_show = "Talk - Show"
    news = "News"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class FilmTypesEnum(str, Enum):
    movie = 'movie'
    short = 'short'
    tv_series = 'tv-series'
    cartoon = 'cartoon'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
