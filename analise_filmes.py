import sys

mode = sys.argv[1] if len(sys.argv) > 1 else ""

movies = {}

if mode == "--reducer":
    try:
        with open("/tmp/u.item") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) > 1:
                    movies[parts[0]] = parts[1]
    except:
        pass

if mode == "--mapper":
    for line in sys.stdin:
        fields = line.strip().split("\t")

        if len(fields) == 4:
            movie_id = fields[1]
            rating = fields[2]
            print("{}\t{}".format(movie_id, rating))

elif mode == "--reducer":
    current_movie = None
    ratings = []

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        movie_id, rating = line.split("\t")
        rating = float(rating)

        if current_movie == movie_id:
            ratings.append(rating)
        else:
            if current_movie is not None:
                media = sum(ratings) / len(ratings)
                total = len(ratings)
                max_rating = max(ratings)
                nome = movies.get(current_movie, "Desconhecido")

                print("{}\t{}\t{:.2f}\t{}\t{}".format(
                    current_movie,
                    nome,
                    media,
                    max_rating,
                    total
                ))

            current_movie = movie_id
            ratings = [rating]

    if current_movie is not None:
        media = sum(ratings) / len(ratings)
        total = len(ratings)
        max_rating = max(ratings)
        nome = movies.get(current_movie, "Desconhecido")

        print("{}\t{}\t{:.2f}\t{}\t{}".format(
            current_movie,
            nome,
            media,
            max_rating,
            total
        ))