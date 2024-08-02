"""Initial tables

Revision ID: f41e60ec5f3a
Revises:
Create Date: 2024-07-31 11:14:54.158339

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f41e60ec5f3a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "career_roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_career_roles")),
        sa.UniqueConstraint("name", name=op.f("uq_career_roles_name")),
    )
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_countries")),
        sa.UniqueConstraint("name", name=op.f("uq_countries_name")),
    )
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_genres")),
        sa.UniqueConstraint("name", name=op.f("uq_genres_name")),
    )
    op.create_table(
        "languages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_languages")),
        sa.UniqueConstraint("name", name=op.f("uq_languages_name")),
    )
    op.create_table(
        "persons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("birthday", sa.DATE(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_persons")),
    )
    op.create_table(
        "series",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("production_year", sa.Date(), nullable=False),
        sa.Column("seasons_count", sa.Integer(), nullable=False),
        sa.Column("IMDb_rating", sa.DECIMAL(precision=3, scale=1), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("age_category", sa.String(), nullable=False),
        sa.Column("poster_url", sa.String(), nullable=True),
        sa.Column("trailer_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_series")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "role",
            sa.Enum("OWNER", "MANAGER", "ADMIN", "MEMBER", name="userrole"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("production_year", sa.Date(), nullable=False),
        sa.Column("director_id", sa.Integer(), nullable=False),
        sa.Column("budget", sa.Integer(), nullable=True),
        sa.Column("box_office", sa.Integer(), nullable=True),
        sa.Column("IMDb_rating", sa.DECIMAL(precision=3, scale=1), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("age_category", sa.String(), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("poster_url", sa.String(), nullable=True),
        sa.Column("trailer_url", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["director_id"], ["persons.id"], name=op.f("fk_movies_director_id_persons")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_movies")),
    )
    op.create_table(
        "person_career_role",
        sa.Column("person_id", sa.Integer(), nullable=True),
        sa.Column("career_role_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["career_role_id"],
            ["career_roles.id"],
            name=op.f("fk_person_career_role_career_role_id_career_roles"),
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["persons.id"],
            name=op.f("fk_person_career_role_person_id_persons"),
        ),
    )
    op.create_table(
        "person_genre",
        sa.Column("person_id", sa.Integer(), nullable=True),
        sa.Column("genre_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["genre_id"], ["genres.id"], name=op.f("fk_person_genre_genre_id_genres")
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["persons.id"],
            name=op.f("fk_person_genre_person_id_persons"),
        ),
    )
    op.create_table(
        "series_country",
        sa.Column("series_id", sa.Integer(), nullable=True),
        sa.Column("country_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
            name=op.f("fk_series_country_country_id_countries"),
        ),
        sa.ForeignKeyConstraint(
            ["series_id"],
            ["series.id"],
            name=op.f("fk_series_country_series_id_series"),
        ),
    )
    op.create_table(
        "series_director",
        sa.Column("series_id", sa.Integer(), nullable=True),
        sa.Column("director_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["director_id"],
            ["persons.id"],
            name=op.f("fk_series_director_director_id_persons"),
        ),
        sa.ForeignKeyConstraint(
            ["series_id"],
            ["series.id"],
            name=op.f("fk_series_director_series_id_series"),
        ),
    )
    op.create_table(
        "series_genre",
        sa.Column("series_id", sa.Integer(), nullable=True),
        sa.Column("genre_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["genre_id"], ["genres.id"], name=op.f("fk_series_genre_genre_id_genres")
        ),
        sa.ForeignKeyConstraint(
            ["series_id"], ["series.id"], name=op.f("fk_series_genre_series_id_series")
        ),
    )
    op.create_table(
        "series_language",
        sa.Column("series_id", sa.Integer(), nullable=True),
        sa.Column("language_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["language_id"],
            ["languages.id"],
            name=op.f("fk_series_language_language_id_languages"),
        ),
        sa.ForeignKeyConstraint(
            ["series_id"],
            ["series.id"],
            name=op.f("fk_series_language_series_id_series"),
        ),
    )
    op.create_table(
        "user_watchlist_series",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("series_id", sa.Integer(), nullable=False),
        sa.Column("added_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["series_id"],
            ["series.id"],
            name=op.f("fk_user_watchlist_series_series_id_series"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_watchlist_series_user_id_users"),
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "series_id", name=op.f("pk_user_watchlist_series")
        ),
    )
    op.create_table(
        "movie_country",
        sa.Column("movie_id", sa.Integer(), nullable=True),
        sa.Column("country_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
            name=op.f("fk_movie_country_country_id_countries"),
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"], ["movies.id"], name=op.f("fk_movie_country_movie_id_movies")
        ),
    )
    op.create_table(
        "movie_genre",
        sa.Column("movie_id", sa.Integer(), nullable=True),
        sa.Column("genre_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["genre_id"], ["genres.id"], name=op.f("fk_movie_genre_genre_id_genres")
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"], ["movies.id"], name=op.f("fk_movie_genre_movie_id_movies")
        ),
    )
    op.create_table(
        "movie_language",
        sa.Column("movie_id", sa.Integer(), nullable=True),
        sa.Column("language_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["language_id"],
            ["languages.id"],
            name=op.f("fk_movie_language_language_id_languages"),
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"], ["movies.id"], name=op.f("fk_movie_language_movie_id_movies")
        ),
    )
    op.create_table(
        "user_watchlist_movies",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("added_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
            name=op.f("fk_user_watchlist_movies_movie_id_movies"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_watchlist_movies_user_id_users"),
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "movie_id", name=op.f("pk_user_watchlist_movies")
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_watchlist_movies")
    op.drop_table("movie_language")
    op.drop_table("movie_genre")
    op.drop_table("movie_country")
    op.drop_table("user_watchlist_series")
    op.drop_table("series_language")
    op.drop_table("series_genre")
    op.drop_table("series_director")
    op.drop_table("series_country")
    op.drop_table("person_genre")
    op.drop_table("person_career_role")
    op.drop_table("movies")
    op.drop_table("users")
    op.drop_table("series")
    op.drop_table("persons")
    op.drop_table("languages")
    op.drop_table("genres")
    op.drop_table("countries")
    op.drop_table("career_roles")
    # ### end Alembic commands ###
