from geopandas.geodataframe import GeoDataFrame
from pyspark.sql.functions import lit, udf, pandas_udf
from pyspark.sql import DataFrame
from pyspark.sql import types

import geopandas as gpd
import h3


def create_sjoin_pnu(gdf: GeoDataFrame, join_column_name: str):
    def sjoin_settlement(x, y):
        gdf_temp = gpd.GeoDataFrame(
            data=[[x] for x in range(len(x))], geometry=gpd.points_from_xy(x, y)
        ).set_crs(epsg=4326, inplace=True)
        settlement: GeoDataFrame = gpd.sjoin(gdf_temp, gdf, how="left", op="within")
        settlement = settlement.drop_duplicates(subset="geometry")

        return (
            settlement.agg({"PNU": str(x)})
            .reset_index()
            .loc[:, join_column_name]
            .astype("str")
        )

    return pandas_udf(sjoin_settlement, returnType=types.StringType())


def _coord_to_pnu(
    origin_df: DataFrame, gdf: GeoDataFrame, x_colname: str, y_colname: str
):
    sjoin_udf = create_sjoin_pnu(gdf, "PNU")
    res_df = origin_df.withColumn(
        "PNU", sjoin_udf(origin_df[x_colname], origin_df[y_colname])
    )
    return res_df


def _join_with_table(table_df: DataFrame, pnu_df: DataFrame):
    # temp_df = self.coord_to_pnu()
    table_df = table_df.dropDuplicates(["bupjungdong_code"])
    res_df = pnu_df.join(
        table_df, [pnu_df.PNU[0:10] == table_df.bupjungdong_code], how="left_outer"
    )
    res_df = res_df.dropDuplicates(["PNU"])

    return res_df


class CustomDataFrame(object):
    """
    CustomDataFrame()
    :param	origin_df
    :param	gdf
    :param	table_df
    :param	x_colname
    :param	y_colname

    coord_to_h3()
    :param	h3_level

    coord_to_pnu()

    join_with_table()
    """

    def __init__(
        self,
        origin_df: DataFrame,
        gdf=None,
        table_df=None,
        x_colname=None,
        y_colname=None,
    ):
        self._origin_df = origin_df
        self._gdf = gdf
        self._table = table_df
        self._x_colname = x_colname
        self._y_colname = y_colname

        self.pnu_df = _coord_to_pnu(origin_df, gdf, x_colname, y_colname).cache()
        self.joined_df = _join_with_table(table_df, self.pnu_df).cache()
        # self.pnu_df.show()
        # self._integrated_df = self.join_with_table()
        # self._integrated_df.show()
        # self._gdf = gdf

    def coord_to_h3(self, h3_level):
        udf_to_h3 = udf(
            lambda x, y: h3.geo_to_h3(float(x), float(y), h3_level),
            returnType=types.StringType(),
        )

        res_h3 = self._origin_df.withColumn(
            "h3",
            udf_to_h3(
                self._origin_df[self._y_colname], self._origin_df[self._x_colname]
            ),
        )
        return res_h3

    def coord_to_pnu(self):
        return self.pnu_df

    def coord_to_zipcode(self):
        joined_df = self.joined_df.select("PNU", "zipcode")
        res_df = self.pnu_df.join(joined_df, "PNU", "leftouter")
        return res_df

    def coord_to_emd(self):
        joined_df = self.joined_df.select("PNU", "bupjungdong_code")
        res_df = self.pnu_df.join(joined_df, "PNU", "leftouter")
        return res_df

    def coord_to_doromyoung(self):
        joined_df = self.joined_df.select(
            "PNU",
            "sido",
            "sigungu",
            "roadname",
            "is_basement",
            "building_primary_number",
            "building_secondary_number",
            "bupjungdong_code",
        )
        res_df = self.pnu_df.join(joined_df, "PNU", "leftouter")
        return res_df

    def coord_to_jibun(self):
        joined_df = self.joined_df.select(
            "PNU",
            "sido",
            "sigungu",
            "eupmyeondong",
            "bupjungli",
            "jibun_primary_number",
            "jibun_secondary_number",
        )
        res_df = self.pnu_df.join(joined_df, "PNU", "leftouter")
        return res_df

    """
	def coord_to_zipcode2(self):
		pnu_df = self.pnu_df
		res_df = pnu_df.withColumn('zipcode', self.joined_df['zipcode'])
		return res_df
	"""

    def join_with_table(self):
        return self.joined_df

    """
	def create_sjoin_pnu(self, join_column_name):
		def sjoin_settlement(x, y):
			gdf_temp = gpd.GeoDataFrame(
				data=[[x] for x in range(len(x))], geometry=gpd.points_from_xy(x, y)
			).set_crs(epsg=4326, inplace=True)
			settlement = gpd.sjoin(gdf_temp, self._gdf, how='left', op='within')
			settlement = settlement.drop_duplicates(subset='geometry')

			return (
				settlement.agg({"PNU": lambda x: str(x)})
				.reset_index()
				.loc[:, join_column_name]
				.astype("str")
			)
		return pandas_udf(sjoin_settlement, returnType=types.StringType())

	def join_with_table(self):
		temp_df = self.coord_to_pnu()
		table_df = self._table.dropDuplicates(["bupjungdong_code"])
		res_df = temp_df.join(
			table_df, [temp_df.PNU[0:10] == table_df.bupjungdong_code], how='left_outer'
		)

		return res_df
	"""

    """
	def coord_to_pnu(self):
		sjoin_udf = self.create_sjoin_pnu("PNU")
		res_df = self._origin_df.withColumn("PNU", sjoin_udf(self._origin_df[self._x_colname], self._origin_df[self._y_colname]))

		return res_df
	"""


"""
class AddressTo
	def address_to_h3(self, )

	def coord_to_zip(self, gdf):
		self.origin_df = self

	def coord_to_emd(self, x_colname, y_colname):
		self.origin_df = self

	def coord_to_address(self):
		self.origin_df = self

	def address_to_h3(self):
		self.origin_df = self

	def address_to_zip(self):
		self.origin_df = self

	def address_to_emd(self):
		self.origin_df = self

	def address_to_coord(self):
		self.origin_df = self
"""
