#!python3
# Requires Movielens dataset already downloaded
import d2

critics = d2.load_dataset()
print( d2.sim_distance(critics,1,2)  )
print( d2.topMatches(critics,1,n=5)  ) # Top 5 people similar to you
print( "\n",d2.getRecos(critics,1)  ) # Movies recommended for critic 1

# a = r.sim_distance(r.critics,'Lisa Rose','Gene Seymour') # Similartity score between critics
# b = r.sim_pearson(r.critics,'Lisa Rose','Gene Seymour') # Similarity score between critics

# print(r.topMatches(r.critics, 'Toby', n=3)) # Which people are similar to you
# print( r.getRecos(r.critics, 'Toby') ) # Recos of movies for you

# movies = r.transformPrefs(r.critics)
# print( r.topMatches(movies, 'Superman Returns') ) # Movies similar to this one

# print( r.getRecos(movies, 'Just My Luck') ) # Recommend critics for a movie
