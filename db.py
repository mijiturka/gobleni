from sqlalchemy import create_engine, MetaData, Table

engine = create_engine('sqlite:///read.db', convert_unicode=True)
metadata = MetaData(bind=engine)
gobleni = Table('gobleni', metadata, autoload=True)
hudojnici = Table('hudojnici', metadata, autoload=True)

def goblen_info(number):
    return gobleni.select(gobleni.c.id == number).execute().first()

def goblen_name(number):
    return gobleni.select(gobleni.c.id == number).execute().first()['name']

# TODO is it really worth doing 2 db lookups to spare writing it twice? Could db duplicate name field automatically?
# TODO there are too many names for artist; author; hudojnik
def goblen_hudojnik(hudojnik_id):
    print(hudojnik_id)
    return hudojnici.select(hudojnici.c.id == hudojnik_id).execute().first()['name']    

def hudojnik_info(name):
    return hudojnici.select(hudojnici.c.link_name == name).execute().first()

# TODO these link-names shouldn't exist, they should be escaped for urls only
def gobleni_ot(hudojnik_link_name):
    # TODO this fails ugly when none found
    # TODO do prints as logging.debug
    # TODO add ready offers too
    hudojnik_id = hudojnici.select(hudojnici.c.link_name == hudojnik_link_name).execute().first()['id']
    return gobleni.select(gobleni.c.author == hudojnik_id).execute()

# a = gobleni_ot('elisabeth-vigee-le-brun')
# print(a)
# for g in a:
#     print(g['name'])
#
# print(g_info(106)['name'])
# print(g_name(106))

# # Prebroi goblenite po kategorii
# gobleni_all = gobleni.select().execute()
# categories = {}
# for g in gobleni_all:
#     cat = g['cat']
#     if cat in categories:
#         categories[cat] += 1
#     else:
#         categories[cat] = 1
# print(categories)
#
# # Prebroi goblenite ot kategoriq "religiozni"
# gobleni_religiozni = gobleni.select(gobleni.c.cat == 'religious').execute()
# categories = {}
# for g in gobleni_religiozni:
#     print(g['name'])
