import folium
import pandas as pd
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
import json
import matplotlib.pyplot as plt

cul = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/culture.csv', encoding = 'CP949')
tra = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/station.csv', encoding = 'CP949')
gym = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/health_facility.csv', encoding = 'UTF-8')
par = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/park_final.csv', encoding = 'UTF-8')
hot = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/hotel_final.csv', encoding = 'UTF-8')
sch = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/school.csv', encoding = 'UTF-8')
uni = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/univ_final2.csv', encoding = 'UTF-8')
tou = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/tourlist_final.csv', encoding = 'CP949')
han = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/seoul_hanPark.csv', encoding = 'UTF-8')
rop = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/road_for_people.csv', encoding = 'UTF-8')
rop2 = pd.read_csv('C://Users/user/anaconda_src/data/loc_lat/road_for_people2.csv', encoding = 'UTF-8')

gu_name = "강동구"

cul_gu = cul.set_index("구").loc[gu_name]
cul_gu = cul_gu.reset_index()
cul_gu.rename(columns = {'문화공간명':'이름','X좌표':'X','Y좌표':'Y','구':'시군구'}, inplace=True)

tra_gu = tra.set_index('구').loc[gu_name]
tra_gu = tra_gu.reset_index()
tra_gu.rename(columns = {'구':'시군구','전철역명':'이름'}, inplace=True)

gym_gu = gym[['names','구','lat','lon']].set_index('구').loc[gu_name]
gym_gu = gym_gu.reset_index()
gym_gu.rename(columns = {'구':'시군구','names':'이름','lat':'X','lon':'Y'}, inplace=True)

park_gu = par[['공원명','구','공원면적','위도','경도']].set_index('구').loc[gu_name]
park_gu = park_gu.reset_index()
park_gu.rename(columns = {'구':'시군구','공원명':'이름','위도':'X','경도':'Y'}, inplace=True)

hotel_gu = hot[['자치구','호텔명','위도','경도']].set_index("자치구").loc[gu_name]
hotel_gu = hotel_gu.reset_index()
hotel_gu.rename(columns = {'자치구':'시군구','호텔명':'이름','위도':'X','경도':'Y'}, inplace=True)

school_gu = sch[['구','학교명','위도','경도']].set_index('구').loc[gu_name]
school_gu = school_gu.reset_index()
school_gu.rename(columns = {'구':'시군구','학교명':'이름','위도':'X','경도':'Y'}, inplace=True)

univ_gu = uni[['구','대학교명','lat','lon']].set_index('구').loc[gu_name]
univ_gu = univ_gu.reset_index()
univ_gu.rename(columns = {'구':'시군구','대학교명':'이름','lat':'X','lon':'Y'}, inplace=True)

tour_gu = tou[['구','관광명소','lat','lon']].set_index('구').loc[gu_name]
tour_gu = tour_gu.reset_index()
tour_gu.rename(columns = {'구':'시군구','관광명소':'이름','lat':'X','lon':'Y'}, inplace=True)

han_gu = han[['구','위도','경도']].set_index('구').loc[gu_name]
han_gu = han_gu.reset_index()
han_gu['이름'] = '없음'
han_gu.rename(columns = {'구':'시군구','위도':'X','경도':'Y'}, inplace=True)

rop_gu = rop[['시군구명','보행자우선도로명','보행자우선도로시작점위도','보행자우선도로시작점경도','보행자우선도로종료점위도','보행자우선도로종료점경도','도로폭']].set_index('시군구명').loc[gu_name]
rop_gu = rop_gu.reset_index()
rop_gu.rename(columns = {'시군구명':'시군구','보행자우선도로명':'이름','보행자우선도로시작점위도':'X','보행자우선도로시작점경도':'Y','보행자우선도로종료점위도':'EX','보행자우선도로종료점경도':'EY'}, inplace=True)

rop_gu2 = rop2[['시군구명','보행자우선도로명','보행자우선도로종료점위도','보행자우선도로종료점경도','도로폭']].set_index('시군구명').loc[gu_name]
rop_gu2 = rop_gu2.reset_index()
rop_gu2.rename(columns = {'시군구명':'시군구','보행자우선도로명':'이름','보행자우선도로종료점위도':'X','보행자우선도로종료점경도':'Y'}, inplace=True)

df = pd.read_csv("C://Users/user/Desktop/project/3.csv", encoding='UTF-8')
df4 = pd.read_csv("C://Users/user/Desktop/project/4.csv", encoding='UTF-8')
df5 = pd.read_csv("C://Users/user/Desktop/project/5.csv", encoding='UTF-8')
df6 = pd.read_csv("C://Users/user/Desktop/project/6.csv", encoding='UTF-8')
df7 = pd.read_csv("C://Users/user/Desktop/project/7.csv", encoding='UTF-8')
df8 = pd.read_csv("C://Users/user/Desktop/project/8.csv", encoding='UTF-8')
df9 = pd.read_csv("C://Users/user/Desktop/project/9.csv", encoding='UTF-8')
df10 = pd.read_csv("C://Users/user/Desktop/project/10.csv", encoding='UTF-8')

code = pd.read_csv("C://Users/user/anaconda_src/data/admin_code.csv", encoding='UTF-8')
code = code.rename(columns = {'행자부행정동코드':'행정동코드'})

df = pd.concat([df, df4, df5, df6, df7, df8, df9, df10])

df_all = df[['기준일ID','시간대구분','행정동코드','총생활인구수']]
df_all_dong = df_all.groupby('행정동코드').mean()[['총생활인구수']]
df_ad = pd.merge(df_all_dong, code, on = '행정동코드')[['시군구명','행정동명','행정동코드','총생활인구수']]
df_add = df_ad.set_index("시군구명")
df_add.head()

dfs = df_add.loc[gu_name].reset_index()[['행정동명','총생활인구수']]

geo_path = 'C://Users/user/anaconda_src/data/dong_shape.json'
geo_str = json.load(open(geo_path, encoding='utf-8-sig'))

guDatS = pd.DataFrame({'adm_nm':dfs['행정동명'], 'counts':dfs['총생활인구수']})

map1 = folium.Map(location=[37.546706, 127.087004], zoom_start=14)
map1.choropleth(geo_data=geo_str,
                  data=guDatS,
                  columns=['adm_nm', 'counts'],
                  fill_color='Reds', #PuRd, YlGnBu
                  key_on='feature.properties.adm_nm')

for row in cul_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in tra_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in gym_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in park_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in hotel_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in school_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in univ_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in tour_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in rop_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in rop_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.EX,row.EY], popup=row.이름))
for row in han_gu.itertuples():
    map1.add_child(folium.Marker(location=[row.X,row.Y]))

map2 = folium.Map(location=[37.546706, 127.087004], zoom_start=14)
map2.choropleth(geo_data=geo_str,
                  data=guDatS,
                  columns=['adm_nm', 'counts'],
                  fill_color='Reds', #PuRd, YlGnBu
                  key_on='feature.properties.adm_nm')
mc = MarkerCluster()
for row in cul_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in tra_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in gym_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in park_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in hotel_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in school_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in univ_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in tour_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in rop_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y], popup=row.이름))
for row in rop_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.EX,row.EY], popup=row.이름))
for row in han_gu.itertuples():
    mc.add_child(folium.Marker(location=[row.X,row.Y]))
map2.add_child(mc)

df = pd.concat([cul_gu[['이름','X','Y']], tra_gu[['이름','X','Y']], gym_gu[['이름','X','Y']], park_gu[['이름','X','Y']], hotel_gu[['이름','X','Y']], school_gu[['이름','X','Y']], univ_gu[['이름','X','Y']], rop_gu[['이름','X','Y']], rop_gu2[['이름','X','Y']]])

heat_data = [[row.X, row.Y] for index, row in df.iterrows()]
map3 = folium.Map(location = [37.546706, 127.087004], zoom_start = 14)
HeatMap(heat_data, max_zoom = 300, blur = 20, radius = 30, min_opacity=0.5, overlay=False).add_to(map3)
map3.choropleth(geo_data=geo_str,
                  data=guDatS,
                  columns=['adm_nm', 'counts'],
                  fill_color='YlGnBu', #PuRd, YlGnBu
                  key_on='feature.properties.adm_nm',
                  fill_opacity = 0.3)

map1.save('./강동구1.html')
map2.save('./강동구2.html')
map3.save('./강동구3.html')
