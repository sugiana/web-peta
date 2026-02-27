from pyramid.view import view_config
from pyramid.response import Response
from models import Wilayah
from sqlalchemy import func
import json


FIELDS = [
    'jumlah_penduduk', 'pria', 'wanita', 'islam', 'kristen', 'katholik',
    'hindu', 'budha', 'konghucu']


def thousand(n):
    s = '{0:,}'.format(n)
    return s.replace(',', '.')


def get_field(row, field):
    if field not in row.data:
        return
    label = ' '.join(field.split('_'))
    label = label.title()
    s = thousand(row.data[field])
    return f'{label} {s}'


@view_config(route_name='home', renderer='templates/index.pt')
def home_view(request):
    return {'project': 'Indonesian Map'}


@view_config(route_name='geojson', renderer='json')
def geojson_view(request):
    def add_description():
        value = get_field(row, field)
        if value is not None:
            ket.append(value)

    tingkat_id = request.params.get('tingkat', 1)  # Default: Provinsi
    bbox = request.params.get('bbox')

    query = request.dbsession.query(
        Wilayah.id,
        Wilayah.nama_lengkap,
        Wilayah.data,
        func.ST_AsGeoJSON(Wilayah.batas).label('geometry')
    ).filter(
        Wilayah.tingkat_id == tingkat_id,
        Wilayah.batas != None
    )

    if bbox:
        # bbox is expected as 'min_lng,min_lat,max_lng,max_lat'
        try:
            min_lng, min_lat, max_lng, max_lat = map(float, bbox.split(','))
            query = query.filter(
                func.ST_Intersects(
                    Wilayah.batas,
                    func.ST_MakeEnvelope(
                        min_lng, min_lat, max_lng, max_lat, 4326)
                )
            )
        except ValueError:
            pass

    results = query.all()

    features = []
    for row in results:
        ket = [row.nama_lengkap]
        if row.data:
            for field in FIELDS:
                add_description()
        ket = '<br>'.join(ket)
        feature = {
            "type": "Feature",
            "id": row.id,
            "properties": {
                "name": ket
            },
            "geometry": json.loads(row.geometry)
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }
