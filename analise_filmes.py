import sys
import io

sys.stdout = io.TextIOWrapper(
    sys.stdout.buffer,
    encoding="utf-8"
)

# Identifica se o Hadoop chamou o script como --mapper ou --reducer
mode = sys.argv[1] if len(sys.argv) > 1 else ""


if mode == "--mapper":

    for line in sys.stdin:
        # Remove espaços em branco e divide por tabulação
        fields = line.strip().split("\t")

        # u.data: userID, movieID, rating, timestamp
        if len(fields) == 4:
            movie_id = fields[1]
            rating = fields[2]

            # Saída: ID do filme + nota
            print("{}\t{}".format(movie_id, rating))


elif mode == "--reducer":

    # Carrega os nomes dos filmes do arquivo u.item
    filmes = {}

    with open("u.item", "r", encoding="latin-1") as arquivo:
        for linha in arquivo:
            campos = linha.strip().split("|")

            if len(campos) >= 2:
                filmes[campos[0]] = campos[1]

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
            # Finaliza o filme anterior
            if current_movie is not None:
                media = sum(ratings) / len(ratings)
                nota_maxima = max(ratings)
                total = len(ratings)

                nome_filme = filmes.get(
                    current_movie,
                    "Desconhecido"
                )

                print("{}\t{}\t{:.2f}\t{:.1f}\t{}".format(
                    current_movie,
                    nome_filme,
                    media,
                    nota_maxima,
                    total
                ))

            # Inicia o próximo filme
            current_movie = movie_id
            ratings = [rating]

    # Finaliza o último filme
    if current_movie is not None:
        media = sum(ratings) / len(ratings)
        nota_maxima = max(ratings)
        total = len(ratings)

        nome_filme = filmes.get(
            current_movie,
            "Desconhecido"
        )

        print("{}\t{}\t{:.2f}\t{:.1f}\t{}".format(
            current_movie,
            nome_filme,
            media,
            nota_maxima,
            total
        ))
