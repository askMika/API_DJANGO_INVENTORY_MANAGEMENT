from django.urls import path
from inventoryManagement.views import (
    ProductListView, 
    ProductDetailView, 
    StockItemListView, 
    StockItemDetailView,
    addToQueue,
    getAllQueueEntries,
    checkBookExistsByISBN,
    check_book_exists,  # Imported functional view
    get_book_by_id,
    getBookByISBN ,     # Imported functional view,
    checkinBookByIsbn,
    isBorrowed
)

urlpatterns = [
    # Base Product Endpoints
    path('InventorymanagementProduct/', ProductListView.as_view(), name='InventorymanagementProduct'),
    path('InventorymanagementProduct/<int:pk>/', ProductDetailView.as_view(), name='InventorymanagementProduct-detail'),
    
    # Base Stock Item Endpoints
    path('StockItems/', StockItemListView.as_view(), name='stock-list'),
    path('StockItems/<int:pk>/', StockItemDetailView.as_view(), name='stock-detail'),

    # FIXED: Routing directly to standalone functions to prevent class TypeErrors
    path('books/<int:pk>/', get_book_by_id, name='get-book-by-id'),
    path('books/<int:pk>/exists/', check_book_exists, name='book-exists'),
    path('books/<str:isbn>/checkin/', getBookByISBN, name='checkin-book'),
    path('books/<str:isbn>/isExisting/',checkBookExistsByISBN, name='check-ifExists'),
    path('books/queue',addToQueue),
    path('book/getQueue',getAllQueueEntries),
    path('books/checkin/<str:asset_id>',checkinBookByIsbn,name='checkinBook'),
    path('books/CheckIfBookExistsByID/<str:asset_id>',isBorrowed,name='isBorrowed')
]