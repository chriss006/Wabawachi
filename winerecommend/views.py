from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .recommend import preprocess_doc, recommend_similar_wine

class SimilarWineListView(APIView):
        def get(self, request, wine_id):
    
                doc = preprocess_doc()
                input_vec = doc[doc['wine_id']==wine_id].values
                wine_list= recommend_similar_wine(input_vec, doc)
                
                return Response(list(wine_list))
