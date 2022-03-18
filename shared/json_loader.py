import json
import pathlib
from apps.basin.models import Basin
from apps.well.models import Well, VerticalUnities


def load_json(path):
    _path = pathlib.Path(path)
    with open(_path) as j:
        data = json.load(j)
    return data


class BatchAGPLoader:
    """
    Main class to batch load wells from AGP files keys and values.
    """
    data = []

    def __init__(self, path):
        self.open_json(path)
        self.create_well()

    def open_json(self, path: str):
        self.data.extend(load_json(path))

    def create_well(self):
        """
        Creates wells for the json objects
        """
        # - Creates instances of the basins
        parnaiba_onshore, created = Basin.objects.update_or_create(
            name='Parnaíba OnShore', onshore=True)
        alagoas_onshore, created = Basin.objects.update_or_create(
            name='Alagoas Onshore', onshore=True)
        sergipe_onshore, created = Basin.objects.update_or_create(
            name='Sergipe Onshore', onshore=True)
        # - Offshore Basins
        alagoas_offshore, created = Basin.objects.update_or_create(
            name='Alagoas Offshore', offshore=True)
        sergipe_offshore, created = Basin.objects.update_or_create(
            name='Sergipe Offshore', offshore=True)
        #
        # - Loops over each object in json/dict in data.
        for well in self.data:
            data_dict = {}
            # - Set Brazil for default country for AGP
            data_dict['country'] = 'Brazil'
            # - Well Name
            name = well['POCO']
            data_dict['formal_name'] = name
            # - Commom Name
            common_name = well['NOME']
            data_dict['common_name'] = common_name
            # - Latitude
            lat = float(well['LATITUDE'][0:9])
            data_dict['lat'] = lat
            # - Longitude
            long = float(well['LONGITUDE'][0:9])
            data_dict['long'] = long
            # - State
            state = well['ESTADO']
            data_dict['state'] = state
            # - City
            city = well['MUNICIPIO']
            data_dict['city'] = city
            # - Well Id
            well_id = well['IDENTIFICADOR']
            data_dict['well_id'] = well_id
            # - Rotative Table and BAP fieelds
            vertunities = well['FORMAC']
            try:
                if well['MESA ROTATIVA']:
                    rotative_table = float(well['MESA ROTATIVA'][0:9])
                    data_dict['rotative_table'] = rotative_table
                else:
                    rotative_table = None
                    data_dict['rotative_table'] = rotative_table
                # - BAP
                if well['B.A.P']:
                    bap = float(well['B.A.P'][0:9])
                    data_dict['bap'] = bap
                else:
                    bap = None
                    data_dict['bap'] = bap

            except Exception as e:
                data_dict['rotative_table'] = None
                data_dict['bap'] = None
                print(e, well['POCO'])

            basin = well['BACIA']
            # - ONSHORE BASINS
            if basin == 'PARNAIBA':
                well_obj, created = Well.objects.update_or_create(
                    **data_dict, basin=parnaiba_onshore, onshore=True)

            if basin == "ALAGOAS (T)":
                well_obj, created = Well.objects.update_or_create(
                    **data_dict, basin=alagoas_onshore, onshore=True)

            if basin == "SERGIPE (T)":
                well_obj, created = Well.objects.update_or_create(
                    **data_dict, basin=sergipe_onshore, onshore=True)

            # - OFFSHORE BASINS
            if basin == "ALAGOAS (M)":
                well_obj, created = Well.objects.update_or_create(
                    **data_dict, basin=alagoas_offshore, offshore=True)

            if basin == "SERGIPE (M)":
                well_obj, created = Well.objects.update_or_create(
                    **data_dict, basin=sergipe_offshore, offshore=True)

            for k, v in vertunities.items():
                vertunities: dict
                if v['TOPO'] == 'null':
                    v['TOPO'] = None
                if v['BASE'] == 'null':
                    v['BASE'] = None
                if v['TOPO COTA'] == 'null':
                    v['TOPO COTA'] = None
                if v['BASE COTA'] == 'null':
                    v['BASE COTA'] = None
                vert_dict = {}
                vert_dict['name'] = k
                vert_dict['well_name'] = well_obj
                vert_dict['top_depth'] = v['TOPO']
                vert_dict['base_depth'] = v['BASE']
                vert_dict['top_quota'] = v['TOPO COTA']
                vert_dict['base_quota'] = v['BASE COTA']
                vert, created = VerticalUnities.objects.update_or_create(
                    **vert_dict, well=well_obj
                )
