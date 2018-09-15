import json
from collections import OrderedDict

from src.database.dbtools import DbTool
from src.objects.fields import FieldType, Field
from src.objects.creatures import CreatureGroup, CreatureType, SpawnedCreature
from src.objects.containers import ContainerType, Container
from src.objects.items import BoundedItem, Item
from src.tools.globals.global_paths import CREATURES_DATA_FILE, ITEMS_DATA_FILE
from src.tools.globals.global_paths import CONTAINERS_TYPES_DATA_FILE, FIELD_CONTAINERS_DATA_FILE,\
    CREATURES_CONTAINERS_DATA_FILE, STATIC_CONTAINERS_DATA_FILE
from src.tools.globals.global_paths import FIELDS_DATA_FILE, FIELDS_TYPE_DATA_FILE

obj_file_dict = {
    FIELDS_TYPE_DATA_FILE: OrderedDict(FieldType=FieldType),
    FIELDS_DATA_FILE: OrderedDict(Field=Field),
    CREATURES_DATA_FILE:
        OrderedDict(CreatureGroup=CreatureGroup, CreatureType=CreatureType, SpawnedCreature=SpawnedCreature),
    CONTAINERS_TYPES_DATA_FILE: OrderedDict(ContainerType=ContainerType),
    FIELD_CONTAINERS_DATA_FILE: OrderedDict(Container=Container),
    CREATURES_CONTAINERS_DATA_FILE: OrderedDict(Container=Container),
    STATIC_CONTAINERS_DATA_FILE: OrderedDict(Container=Container),
    ITEMS_DATA_FILE: OrderedDict(Item=Item, BoundedItem=BoundedItem)
}


def load_initial_data():
    for file_path, table_group in obj_file_dict.items():
        with open(file_path) as f:
            json_data = json.loads(f.read())
            insert_to_database(json_data, table_group)


def insert_to_database(json_data, obj_dict):
    for table_name in obj_dict.keys():
        for row in json_data[table_name]:
            DbTool().insert_row(obj_dict[table_name](**row))