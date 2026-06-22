from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

# FIX: Import YOUR custom User model from your local models file
from .models import User  

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_student_exists(request, username):
    """
    Checks if a learner username exists directly within your custom users system.
    """
    try:
        # This will now look inside your custom 'users' database table!
        user = User.objects.get(username=username)
        
        return Response({
            "exists": True,
            "username": user.username,
            "full_name": f"{user.first_name} {user.last_name}".strip() or user.username,
            "grade": user.role or "Active Learner" # Uses your custom 'role' field
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            "exists": False, 
            "error": "Learner not found."
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Safeguard: logs any other unexpected errors right to your terminal
        print(f"Backend Exception: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)