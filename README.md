# Spark Plus
Apache Spark Plugin to analyze Korea's address system
Spark+는 H3, 위/경도 좌표 등의 공간 정보를 국내 주소체계(신주소/구주소)와 함께 처리할 수 있도록 지원하는 Plugin입니다.

Spark+는 Apache Spark와 MySQL을 지원합니다.

## Structure
- spark-plugin: 패키지 폴더
- setup.py: 패키지의 설정, 서문
- .pypirc: 패키지 업로드를 위한 설정
- 추가: MANIFEST.in 등의 파일

### dependecnies
- spark
   - `start_spark(app_name, master, jar_packages, files, spark_config)`
      ```
      from dependecnies.spark import start_spark 

      spark, *_ = start_spark  
      ```
      - spark session을 시작합니다.
      - params
         - app_name: str, 어플리케이션 이름(default: my_spark_app)
         - master: str, master 노드(default: local[*])
         - jar_packages: list, Spark Jar package 이름
         - files: list, Spark Cluster(master/worker)로 전송할 파일
         - spark_config: dict, config key-value pairs
      - return
         - Spark session
         - logger
         - config dict

- logging
   - `Log4j(object: spark session)`


### jobs
- load_database
   - `load_tables(spark, url, user, password, driver, opt)`
      ```
      from jobs.load_tables import load_tables

      driver = "driver"
      url = "url"
      user = "user"
      password = "password"
      opt = "seoul"

      df = load_tables(spark, url, user, password, driver, opt)
      df.show()
      ```
      - 데이터베이스에서 테이블을 불러옵니다
      - params
         - spark: obj, spark session
         - url: str, db url
         - user: str, db user
         - password: str, db password
         - driver: str, mysql driver(default: "com.mysql.cj.jdbc.Driver"
         - opt: str, 불러올 테이블 지역(default: "all")
- conversion
   - `coord_to_emd(spark, gdf, sdf, lng_colname, lat_colname)`
   - `coord_to_jibun(spark, gdf, sdf, table_df)`
   - `coord_to_roadname(spark, gdf, sdf, table_df)`

### package 
- /gis
   - `gis_init()`
   - `coord_to_dong(spark, gdf, spark_df, lng_colname, lat_colname)`

### testjob

### resource
- /EMD_202101: 법정동 정보를 담고 있는 shp 디렉토리입니다.

## Constructor

### GeomFromWKT
- `GeomFromWKT(Wkt: string)`
### GeomFromWKB **
- `GeomFromWKB(Wkb: string)`
### GeomFromGeoJSON
- `GeomFromGeoJSON(GeoJson: string)`

### DfFromSHP

### GeomFromJUSO

### JusoContainsGeom

### Point
- `Point(X: decimal, Y: decimal)`
### PorintFromText
- `PointFromText(Text: string, Delimiter: char)`
### PolygonFromText
- `PolygonFromText(text: string, Delimiter: char)`
### LineStringFromText
- `LineStringFromText(text: string, Delimiter: char)`
### PolygonFromEnvelope **
- `PolygonFromEnvelope(MinX: decimal, MinY: decimal, MaxX: decimal, MinX: decimal)`

## 패키지 빌드 및 업로드
1. `setuptools`, `wheel` 설치
   - `pip install setuptools wheel`
   - `python -m pip install --user --upgrade setuptools wheel`
  
2. 프로젝트 폴더에서 패키지 빌드
   - `python setup.py sdist bdist_wheel`
   - dist 폴더에 `.tar.gz`, `.whl` 파일 생성되었는지 확인

3. PyPi에 패키지 업로드
   - `pip install twine`
   - `python -m twine upload dist/*`
      - PyPi username과 password 입력
