from django.shortcuts import render, get_object_or_404, redirect
from .models import DB_Books, Category, SubCategory, Author, RackName
from .forms import BookForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from pathlib import Path

from django.views.decorators.http import require_POST



def managebook(request):
    if 'query' in request.GET:
        query = request.GET['query']
        search_book = Q(Q(book_title__icontains=query)|Q(book_language__icontains=query)|Q(book_author__name__icontains=query)|Q(categories__name__icontains=query)|Q(rack_number__name__icontains=query))
        book_obj = DB_Books.objects.filter(search_book)
        if not book_obj.count():
            messages.error(request, f'No records found for the {query} query.')
        else:
            if query != '':
                messages.success(request, f'{book_obj.count()} Record Found For:{query}')
    else:
        book_obj = DB_Books.objects.all()

    # Get All author
    authors = Author.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    racks = RackName.objects.all()
    context = {'book_obj': book_obj, 'authors': authors, 'categories': categories, 'subcategories': subcategories, 'racks': racks}
    return render(request, 'books/managebook.html', context)





@require_POST
def add_book(request):
    book_title = request.POST.get('book_title')
    author_id = request.POST.get('book_author')
    new_author = request.POST.get('new_author')
    category_ids = request.POST.getlist('categories')
    sub_category_id = request.POST.get('sub_category')
    publish_date = request.POST.get('publish_date')
    # status = request.POST.get('status')
    book_language = request.POST.get('book_language')
    no_of_copies_actual = request.POST.get('no_of_copies_actual')
    rack_numbers = request.POST.get('rack_number')
    book_price = request.POST.get('book_price')
    book_description = request.POST.get('book_description')
    book_publisher = request.POST.get('book_publisher')
    isbn = request.POST.get('isbn')
    cover_image = request.FILES.get('cover_image')

    # Get or create the author instance
    if author_id == 'new' and new_author:
        author, created = Author.objects.get_or_create(name=new_author)
    else:
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            author = None

    # Get or create the sub_category instance
    sub_category, created = SubCategory.objects.get_or_create(id=sub_category_id)

    # Get the category instances
    categories = Category.objects.filter(id__in=category_ids)

    # Get the rack instances
    racks = RackName.objects.filter(id__in=rack_numbers)

    # Perform validation here if needed

    # Create the book object and save it to the database
    book = DB_Books(
                    book_title=book_title,
                    book_author=author,
                    # new_author=new_author,
                    # categories=categories,
                    # sub_category=sub_category,
                    publish_date=publish_date,
                    # status=status,
                    book_language=book_language,
                    no_of_copies_actual=no_of_copies_actual,
                    # rack_number=rack_number,
                    book_price=book_price,
                    description=book_description,
                    publisher=book_publisher,
                    isbn=isbn,
                    cover_image=cover_image)

    if DB_Books.objects.filter(book_title=book_title).exists():
        messages.error(request, f'Book Name already used. Please use a different Book Name.')
        return redirect('/books/managebook')
    else:
        book.save()
        # Set the many-to-many relationship for categories and sub_category
        book.categories.set(categories)
        book.sub_category.set([sub_category])
        book.rack_number.set(racks)
        messages.success(request, f'{book_title}\'s record added successfully!')
        return redirect('/books/managebook')


def view_book(request):
    book_obj = DB_Books.objects.all()
    context = {'book_obj': book_obj}
    return redirect(request, '/books/managebook', context)


def delete_book(request, id):
    if request.method == 'POST':
        print(id)
        book_obj = DB_Books.objects.filter(id=id)
        book_qr_code_url = request.POST.get('book_qr_code')
        book_cover_image_url = request.POST.get('book_cover_image')
        if book_qr_code_url != 'NO_QR_CODE_IMG':
            file_path_qr = 'C:\\Users\\admin\\Downloads\\lmsys\\' + book_qr_code_url
            file_path_qr = Path(file_path_qr)

            if file_path_qr.exists():
                file_path_qr.unlink()

        if book_cover_image_url != 'NO_COVER_IMG':
            file_path_cover_img = 'C:\\Users\\admin\\Downloads\\lmsys\\' + book_cover_image_url
            file_path_cover_img = Path(file_path_cover_img)

            if file_path_cover_img.exists():
                file_path_cover_img.unlink()

        # BASE_DIR = Path(__file__).resolve().parent.parent
        # print(BASE_DIR)
        # print('----------------------')
        # file_path = BASE_DIR / qr_code_url



        book_obj.delete()
        messages.success(request, 'Book Details deleted successfully!')
        context = {'book_obj': book_obj}
        return redirect('/books/managebook')


# view Book qr code
def view_bookqrcode(request):
    book_obj = DB_Books.objects.all()
    context = {'book_obj': book_obj}
    return redirect(request, '/books/managebook', context)


def edit_book(request):
    book_obj = DB_Books.objects.all()
    context = {'book_obj': book_obj}
    return redirect(request, '/books/managebook', context)


def update_book(request, id):
    if request.method == 'POST':
        book_title = request.POST.get('book_title')
        author_id = request.POST.get('book_author')
        category_ids = request.POST.getlist('categories')
        sub_category_id = request.POST.get('sub_category')
        # status = request.POST.get('status')
        book_language = request.POST.get('book_language')
        no_of_copies_actual = request.POST.get('no_of_copies_actual')
        no_of_copies_current = request.POST.get('no_of_copies_actual')
        rack_numbers = request.POST.get('rack_number')
        # Get the QR CODE image URL
        book_qr_code_url = request.POST.get('book_qr_code')
        # if cover_image_url is present get file path and replace that path with new file uploaded with 'cover_image'
        # book_cover_image_url = request.POST.get('cover_image_url') #already img is there we need to replace it with new uploaded image
        # cover_image = request.FILES.get('cover_image')
        # print('_'*40)
        # print(book_title, author_id, category_ids, sub_category_id,status, book_language,no_of_copies_actual,no_of_copies_current, rack_numbers,book_qr_code_url)

        # Find the Category object to update
        book_obj = DB_Books.objects.get(id=id)
        # Update the Book data
        # book_obj.book_title = book_title
        author_obj = Author.objects.get(id=author_id)
        book_obj.book_author = author_obj
        # book_obj.category_ids = category_ids
        # book_obj.sub_category_id = sub_category_id
        # book_obj.status = status   # Auto update
        book_obj.book_language = book_language
        book_obj.no_of_copies_actual = int(no_of_copies_actual)
        # book_obj.no_of_copies_current = int(no_of_copies_current)
        # book_obj.rack_numbers = rack_numbers

        # Update book cover if present else upload new
        # if book_cover_image_url:
        #     file_name = os.path.basename(book_cover_image_url)
        #     # Delete the existing file
        #     if book_obj.cover_image.name == file_name:
        #         # Remove the existing file
        #         os.remove(book_obj.cover_image.path)
        #     # Update the cover_image with the new file
        #     book_obj.cover_image.save(file_name, cover_image, save=True)
        # else:
        #     file_name = cover_image.name
        #     # Update the cover_image with the new file
        #     book_obj.cover_image.save(file_name, cover_image, save=True)

        # ManyToManyField
        # Update the categories
        book_obj.categories.set(category_ids)
        # Update the sub_category
        book_obj.sub_category.set([sub_category_id])
        # Update the rack numbers
        book_obj.rack_number.set(rack_numbers)

        # file_path = 'C:\\Users\\admin\\Downloads\\lmsys\\' + book_qr_code_url
        # file_path = Path(file_path)
        #
        # if file_path.exists():
        #     file_path.unlink()

        book_obj.save()
        messages.success(request, 'Book data updated successfully!')
        return redirect('/books/managebook')


##---------------- Category ----------------------
def managecategory(request):
    if 'query' in request.GET:
        query = request.GET['query']
        search_category = Q(Q(name__icontains=query))
        cat_obj = Category.objects.filter(search_category)
        if not cat_obj.count():
            messages.error(request, f'No records found for the {query} query.')
        else:
            if query != '':
                messages.success(request, f'{cat_obj.count()} Record Found For:{query}')
    else:
        cat_obj = Category.objects.all()
    context = {'cat_obj': cat_obj}
    return render(request, 'books/managecategory.html', context)


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
    
        if Category.objects.filter(name=category_name).exists():
            messages.error(request, f'Category Name already used. Please use a different Category.')
            return redirect('/books/managecategory')
        else:
            cat_obj = Category(name=category_name)
            cat_obj.save()
            messages.success(request, f'{category_name}\'s record added successfully!')
            return redirect('/books/managecategory')


def edit_category(request):
    cat_obj = Category.objects.all()
    context = {'cat_obj': cat_obj}
    return redirect(request, '/books/managecategory', context)


def update_category(request, id):
     if request.method == 'POST':
        category_name = request.POST.get('category_name')
              
        # Find the Category object to update
        cat_obj = Category.objects.get(id=id)       
        # Update the user data
        cat_obj.name = category_name
        cat_obj.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('/books/managecategory')
     
def delete_category(request, id):
    if request.method == 'POST':
        cat_obj = Category.objects.filter(id=id)
        cat_obj.delete()
        messages.success(request, 'Category deleted successfully!')
        context = {'cat_obj': cat_obj}
        return redirect('/books/managecategory')
    
def view_category(request):
    category_obj = Category.objects.all()
    context = {'cat_obj': category_obj}
    return redirect(request, '/books/managecategory', context)

# def search_category(request):
#     cat_obj = Category.objects.all()
#     search_contains = request.GET.get('search_contains')
#     if search_contains!='' and search_contains is not None:
#         cat_obj = cat_obj.filter(name__icontains=search_contains) 
#     context = {'cat_obj': cat_obj}
#     return redirect(request, '/books/managecategory', context)



##----------------Sub Category----------------------

def managesubcategory(request):
    if 'query' in request.GET:
        query = request.GET['query']
        search_category = Q(Q(name__icontains=query))
        cat_obj = SubCategory.objects.filter(search_category)
        if  not cat_obj.count(): 
            messages.error(request, f'No records found for the {query} query.')
        else:
            if query !='':
                messages.success(request, f'{cat_obj.count()} Record Found For:{query}')
    else:
        cat_obj = SubCategory.objects.all()
    categories = Category.objects.all()
    context = {'cat_obj': cat_obj, 'categories' : categories}
    return render(request, 'books/managesubcategory.html', context)

# https://www.youtube.com/watch?v=LmYDXgYK1so&ab_channel=CodeBand  
def add_subcategory(request):
    if request.method == 'POST':
        # Retrieve the selected category value
        selected_category_id = request.POST.get('categories')
        # Retrieve the Category object based on the selected ID
        selected_category = Category.objects.get(id=selected_category_id)

        subcategory_name = request.POST.get('subcategory_name')
    
        if SubCategory.objects.filter(name=subcategory_name).exists():
            messages.error(request, f'Subcategory Name already used. Please use a different Subcategory.')
            return redirect('/books/managesubcategory')
        else:
            cat_obj = SubCategory(name=subcategory_name, category=selected_category)
            cat_obj.save()
            messages.success(request, f'{subcategory_name}\'s record added successfully!')
            return redirect('/books/managesubcategory')


def edit_subcategory(request):
    cat_obj = SubCategory.objects.all()
    context = {'cat_obj':cat_obj}
    return redirect(request, '/books/managesubcategory', context)


def update_subcategory(request,id):
     if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')
              
        # Find the Category object to update
        cat_obj = SubCategory.objects.get(id=id)       
        # Update the user data
        cat_obj.name = subcategory_name
        cat_obj.save()
        messages.success(request, 'Subcategory updated successfully!')
        return redirect('/books/managesubcategory')
     
def delete_subcategory(request,id):
    if request.method == 'POST':
        cat_obj = SubCategory.objects.filter(id=id)
        cat_obj.delete()
        messages.success(request, 'Subcategory deleted successfully!')
        context = {'cat_obj':cat_obj}
        return redirect('/books/managesubcategory')
    
def view_subcategory(request):
    subcategory_obj = SubCategory.objects.all()
    context = {'cat_obj': subcategory_obj}
    return redirect(request, '/books/managesubcategory', context)

# def search_subcategory(request):
#     cat_obj = SubCategory.objects.all()
#     search_contains = request.GET.get('search_contains')
#     if search_contains!='' and search_contains is not None:
#         cat_obj = cat_obj.filter(name__icontains=search_contains) 
#     context = {'cat_obj': cat_obj}
#     return redirect(request, '/books/managesubcategory', context)
