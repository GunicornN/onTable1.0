
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from company.serializers import CompanyOutputSerializer
from company.models import Company

from rest_framework.response import Response

@api_view(['GET'])
def CompanyOfUser(request):
    # Récupérer un Restaurant à partir du token
    company = request.user.company
    serializer = CompanyOutputSerializer(company)
    return Response(serializer.data)
