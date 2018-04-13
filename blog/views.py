from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from comments.forms import CommentForm
from .models import Post,Category
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import markdown

# Create your views here.
# def index(request):
#     post_list = Post.objects.all().order_by('-create_time')
#     return render(request,'blog/index.html',context={
#         'post_list':post_list
#     })

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator,page,is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages -1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last
        }
        return data

# def detail(request,pk):
#     post = get_object_or_404(Post,pk=pk)
#     post.increase_views()
#     post.body = markdown.markdown(post.body,extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {
#         'post':post,
#         'form':form,
#         'comment_list':comment_list
#     }
#     return render(request,'blog/detail.html',context=context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context

# def archives(request,year,month):
#     post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})

class ArchivesView(IndexView):
    def get_queryset(self):
        print(self.kwargs.get('year'))
        return super().get_queryset().filter(create_time__year=self.kwargs.get('year'),create_time__month=self.kwargs.get('month'))

# def category(request,id):
#     post_list = Post.objects.filter(category__pk=id).order_by('-create_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})

class CategoryView(IndexView):
    def get_queryset(self):
        print(self.kwargs.get('id'))
        return super().get_queryset().filter(category__id=self.kwargs.get('id'))

class TagView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(tag__id=self.kwargs.get('id'))