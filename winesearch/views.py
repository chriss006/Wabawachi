from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from elasticsearch import Elasticsearch


class SearchView(APIView):

    def get(self, request):
        es = Elasticsearch([{'host':'192.168.20.68', 'port':'9200'}])

        # 검색어
        search_word = request.query_params.get('search')

        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})
        docs = es.search(index='wine_dict',
                         body={
                             "query": {
                                 "multi_match": {
                                     "query": search_word,
                                     "fields": [
                                         "kname",
                                         'winetype^3'
                                ]
                                 }
                             }
                         })

        data = docs['hits']['hits']

        
        return Response(data)
    
class SearchDetailView(APIView):

    def get(self, request):
        es = Elasticsearch([{'host':'192.168.20.68', 'port':'9200'}])

        # 검색어
        search_word = request.query_params.get('search')

        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})
        docs = es.search(index='wine_dict',
                         body={
                             "query": {
                                 "multi_match": {
                                     "query": search_word,
                                     "fields": [
                                         "kname",
                                         'winetype^3'
                                ]
                                 }
                             }
                         })

        data = docs['hits']['hits'][0]['_source']
        result = dict()
        result['wine_picture'] = data['wine_picture']
        result['kname'] = data['kname']
        result['ename'] = data['ename']
        result['winery'] = data['winery']
        result['kr_country'] = data['kr_country']
        result['kr_region'] = data['kr_region']
        result['winetype'] = data['winetype']
        result['kr_grape_list'] = data['kr_grape_list']    
        result['sweet']=data['sweet']
        result['acidic']=data['acidic']
        result['body']=data['body']
        result['tannic']=data['tannic']
        result['notes_list']=data['notes_list']
        result['food_list']=data['food_list']
        
        return Response(result)


