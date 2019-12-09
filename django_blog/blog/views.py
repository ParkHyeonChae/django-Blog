from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
# ex) q = get_object_or_404(Question, pk=id) 1번째 Model, 2번쨰 인자는 Keyword, Keyword 없을 시 404 error 발생.
from django.urls import reverse
from blog.models import Post


def posts_list(request):
    posts = Post.objects.order_by('-created_at')

    return render(request, 'blogs/posts_list.html',  context={'posts':posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    return render(request, 'blogs/post_detail.html', context={'post':post})

@login_required
def post_write(request):
    errors = []
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title:
            errors.append('제목을 입력해주세요.')

        if not content:
            errors.append('내용을 입력해주세요.')

        if not errors:
            post = Post.objects.create(user=request.user, title=title, content=content, image=image)

            return redirect(reverse('post_detail', kwargs={'post_id': post.id}))
    
    return render(request, 'blogs/post_write.html', {'user':request.user, 'errors':errors})
