from setup_environment import *
from footium_api import GqlConnection
from footium_api.queries import get_formations_as_pd
import pandas as pd

gql = GqlConnection()
formations = get_formations_as_pd(gql)

print(formations)
formations.index = "'" + formations.index.astype(str)
# formations.to_csv("formations.csv")
print("done")