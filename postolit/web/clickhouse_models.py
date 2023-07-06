from infi.clickhouse_orm import Model, UInt32Field, StringField, MergeTree, NullableField
from postolit.clickhouse import create_connection

db = create_connection()


class Vedomost3(Model):
    ID_C = UInt32Field()
    ID_P = UInt32Field()
    ID_D = UInt32Field()
    Otsenka = UInt32Field()
    engine = MergeTree(partition_key=(ID_C, ), order_by=(ID_C, ID_D))        
    class Meta:
        database = db
        table_name = "Vedomost3" 


class Distsipliny1(Model):
    ID_D = UInt32Field()
    Distsiplina = StringField()
    Napravleniye = NullableField(StringField())
    engine = MergeTree(partition_key=(ID_D, ), order_by=(ID_D,))
    class Meta:
        database = db
        table_name = "Distsipliny1" 