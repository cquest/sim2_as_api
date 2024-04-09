#! /usr/bin/python3

# modules additionnels
import falcon
import psycopg2

class mf_sim2(object):
    def getSIM2(self, req, resp):
        db = psycopg2.connect("")  # connexion à la base PG locale
        cur = db.cursor()

        where = b' WHERE (1=1) '

        date = req.params.get('date', None)
        if date and len(date) >=4:
            date = date.replace('-','')
            where = where + cur.mogrify(" AND date LIKE %s ", (date+"%",))

        debut = req.params.get('from', None)
        if debut and len(debut) >= 8:
            debut = debut.replace('-','')
            where = where + cur.mogrify(" AND date >= %s ", (debut,))

        fin = req.params.get('to', None)
        if fin and len(fin) >= 8:
            fin = fin.replace('-','')
            where = where + cur.mogrify(" AND date <= %s ", (fin,))

        lat = req.params.get('lat', 48.85)
        lon = req.params.get('lon', 2.35)

        if lat and lon:  # recherche géographique
            query = cur.mogrify("""
select json_build_object('source', 'SIM2 - Météo-France',
    'derniere_maj', '2024',
    'licence', 'Licence ouverte 2.0',
    'type','Featurecollection',
    'features',
    case when count(*)=0 then array[]::json[]
    else
        array_agg(json_build_object('type','Feature',
            'properties',json_strip_nulls(row_to_json(d)),
            'geometry',st_asgeojson(geom,6,0)::json)
        order by date)
    end )::text
    from (select * from sim2_grid order by geom <-> st_setsrid(st_makepoint(%s,%s),4326) limit 1)
        natural join sim2 d
""", (lon, lat)) + where

            cur.execute(query)
            sim2 = cur.fetchone()

            resp.status = falcon.HTTP_200
            resp.set_header('X-Powered-By', 'sim2_as_api')
            resp.set_header('Access-Control-Allow-Origin', '*')
            resp.set_header("Access-Control-Expose-Headers","Access-Control-Allow-Origin")
            resp.set_header('Access-Control-Allow-Headers','Origin, X-Requested-With, Content-Type, Accept')
            resp.set_header('X-Robots-Tag', 'noindex, nofollow')
            resp.body = sim2[0]
        else:
            resp.status = falcon.HTTP_413
            resp.body = '{"erreur": "aucun critère de recherche indiqué"}'

        db.close()

    def on_get(self, req, resp):
        self.getSIM2(req, resp);

# instance WSGI et route vers notre API
app = falcon.API()
app.add_route('/sim2', mf_sim2())

