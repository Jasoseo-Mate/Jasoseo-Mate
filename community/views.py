from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    queryset = Post.objects.select_related("author").annotate(comment_count=Count("comments"))
    posts = Paginator(queryset, 20).get_page(request.GET.get("page"))
    return render(request, 'community/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '게시글이 성공적으로 등록되었습니다.')
            return redirect('community:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'community/post_form.html', {'form': form, 'title': '게시글 작성'})

def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related("author").annotate(comment_count=Count("comments")),
        pk=pk,
    )
    Post.objects.filter(pk=pk).update(views=F("views") + 1)
    post.refresh_from_db(fields=["views"])
    
    comments = post.comments.select_related("author")
    comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'community/post_detail.html', context)

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('community:post_detail', pk=pk)
        
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '게시글이 성공적으로 수정되었습니다.')
            return redirect('community:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
        
    return render(request, 'community/post_form.html', {'form': form, 'title': '게시글 수정'})

@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('community:post_detail', pk=pk)
        
    post.delete()
    messages.success(request, '게시글이 삭제되었습니다.')
    return redirect('community:post_list')

@login_required
@require_POST
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, '댓글이 등록되었습니다.')
    else:
        messages.error(request, '댓글 등록에 실패했습니다.')
    return redirect('community:post_detail', pk=pk)

@login_required
@require_POST
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post_id=post_pk)
    if comment.author != request.user:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        comment.delete()
        messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('community:post_detail', pk=post_pk)
