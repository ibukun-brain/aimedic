from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from classification.api.serializers import HeartClassificationSerializer


class HeartClassificationAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = HeartClassificationSerializer

    @extend_schema(
        summary="Endpoint for AI heart disease classification",
        parameters=[
            HeartClassificationSerializer,
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={
                    "result": "probably have high risk of heart disease"
                },
                description="AI result",
                examples=[
                    OpenApiExample(
                        "High risk",
                        value={
                            "result": "probably have high risk of heart disease"
                        },
                    ),
                    OpenApiExample(
                        "Low risk",
                        value={
                            "result":
                            "probably does not have high risk of heart disease"
                        },
                    )
                ]
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        classifier = serializer.save()
        return Response(classifier, status=status.HTTP_200_OK)
