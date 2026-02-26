from pyramid.view import view_config
from pyramid.response import Response
from models import Wilayah
from sqlalchemy import func
import json


@view_config(route_name='home', renderer='templates/index.pt')
def home_view(request):
    return {'project': 'Indonesian Map'}


@view_config(route_name='geojson', renderer='json')
def geojson_view(request):
    tingkat_id = request.params.get('tingkat', 1)  # Default: Provinsi
    bbox = request.params.get('bbox')

    query = request.dbsession.query(
        Wilayah.id,
        Wilayah.nama_lengkap,
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
        feature = {
            "type": "Feature",
            "id": row.id,
            "properties": {
                "name": row.nama_lengkap
            },
            "geometry": json.loads(row.geometry)
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }
