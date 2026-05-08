
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import optimize_route

class RouteOptimizationAPIView(APIView):

    def post(self, request):
        start = request.data.get('start')
        finish = request.data.get('finish')

        result = optimize_route(start, finish)

        return Response(result)
