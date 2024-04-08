#! /bin/bash

# scrip d'import des données SIM2 (sim2/ISBA) dans postgresql

psql -c "
create table sim2 (LAMBX int,LAMBY int,DATE varchar,PRENEI_Q float,PRELIQ_Q float,T_Q float,FF_Q float,Q_Q float, DLI_Q float, SSI_Q float,HU_Q float,EVAP_Q float,ETP_Q float,PE_Q float,SWI_Q float,DRAINC_Q float,RUNC_Q float,RESR_NEIGE_Q float,RESR_NEIGE6_Q float, HTEURNEIGE_Q  float, HTEURNEIGE6_Q float, HTEURNEIGEX_Q float, SNOW_FRAC_Q float, ECOULEMENT_Q float, WG_RACINE_Q float, WGI_RACINE_Q float, TINF_H_Q float, TSUP_H_Q float);"
create table sim2_grid (lambx int, lamby int, lat varchar, lon varchar);
\copy sim2_grid from 'coordonnees_grille_sim2_lambert-2-etendu.csv' with (format csv, header true, delimiter ';');
alter table sim2_grid add geom geometry(point,4326) ;
update sim2_grid set geom = st_makepoint(replace(lon,',','.')::numeric, replace(lat,',','.')::numeric);
create index sim2_grid_geom on sim2_grid using gist(geom);
"

for F in QUOT_SIM2*.csv;
    do echo $F;
    psql -c "\copy sim2 from $F with (format csv, header true, delimiter ';');"
done

psql -c " CREATE INDEX sim2_date on sim2 (date); " &
psql -c " CREATE INDEX sim2_geo_date on sim2 (lambx,lamby,date); " &
wait
