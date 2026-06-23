from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .serializers import CategorySerializer, CartSerializer, CartItemSerializer, RegisterSerializer, UserSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView


@api_view(['GET'])
def get_products(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_categories(request):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def create_product(request):
    try:
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['PUT'])
def update_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    except Product.DoesNotExist:
        return Response(
            {"message": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['DELETE'])
def delete_product(request, pk):    
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    except Product.DoesNotExist:
        return Response(
            {"message": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return Response({'message': 'Product added to cart',"cart":CartSerializer(cart).data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_quantity(request):
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')
   
    if not item_id or quantity is None:
        return Response({'error': 'Item ID and quantity are required'}, status=400)
    
    try:
        item = CartItem.objects.get(id=item_id)
        if int(quantity) < 1:
            item.delete()
            return Response({'error': 'Quantity must be at least 1'}, status=400)
        
        item.quantity = quantity
        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    item_id = request.data.get('item_id')
    CartItem.objects.filter(id=item_id).delete()
    return Response({'message': 'Item removed from cart'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        data = request.data
        name = data.get('name')
        address = data.get('address')
        phone = data.get('phone')
        payment_method = data.get('payment_method','COD')

        #validate Phone Number
        if not phone.isdigit() or len(phone) < 10:
            return Response({'error': 'Invalid phone number'}, status=400)
        
        # Get user's cart
        cart , created = Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=400)
        
        total = sum([item.product.price * item.quantity for item in cart.items.all()])

        order = Order.objects.create(user = request.user, total_amount=total)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        # Clear the cart
        cart.items.all().delete()
        return Response({'message': 'Order created successfully', 'order_id': order.id})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
  
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created successfully", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#CBVs

class ProductListView(APIView):

    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CategoryListView(APIView):

    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CreateProductView(APIView):

    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class UpdateProductView(APIView):

    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk)

            serializer = ProductSerializer(
                product,
                data=request.data
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class DeleteProductView(APIView):

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            product.delete()

            return Response(
                {"message": "Product deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User created successfully",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class CartView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        serializer = CartSerializer(cart)

        return Response(serializer.data)
    
class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get('product_id')

        product = Product.objects.get(id=product_id)

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            item.quantity += 1
            item.save()

        return Response({
            'message': 'Product added to cart',
            'cart': CartSerializer(cart).data
        })
    
class UpdateCartQuantityView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')

        if not item_id or quantity is None:
            return Response(
                {'error': 'Item ID and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = CartItem.objects.get(id=item_id)

            if int(quantity) < 1:
                item.delete()
                return Response(
                    {'error': 'Quantity must be at least 1'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            item.quantity = quantity
            item.save()

            serializer = CartItemSerializer(item)

            return Response(serializer.data)

        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
class RemoveFromCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        item_id = request.data.get('item_id')

        CartItem.objects.filter(id=item_id).delete()

        return Response(
            {'message': 'Item removed from cart'},
            status=status.HTTP_200_OK
        )
    
class CreateOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            data = request.data

            name = data.get('name')
            address = data.get('address')
            phone = data.get('phone')
            payment_method = data.get(
                'payment_method',
                'COD'
            )

            # Validate phone number
            if not phone.isdigit() or len(phone) < 10:
                return Response(
                    {'error': 'Invalid phone number'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get user's cart
            cart, created = Cart.objects.get_or_create(
                user=request.user
            )

            if not cart.items.exists():
                return Response(
                    {'error': 'Cart is empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            total = sum([
                item.product.price * item.quantity
                for item in cart.items.all()
            ])

            order = Order.objects.create(
                user=request.user,
                total_amount=total
            )

            for item in cart.items.all():

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Clear cart
            cart.items.all().delete()

            return Response(
                {
                    'message': 'Order created successfully',
                    'order_id': order.id
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
