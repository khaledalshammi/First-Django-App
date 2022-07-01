from django.db.models import Count
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Board
from django.utils import timezone
from .models import Topic,Post
from .forms import NewTopicForm,PostForm,NewBoardForm
from django.contrib.auth.decorators import login_required 
from django.views.generic import UpdateView,ListView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})
# class home(ListView):
#     model = Board
#     context_object_name = 'boards'
#     template_name = 'home.html'
def board_topics(request,board_id):
    board = get_object_or_404(Board,pk=board_id)
    queryset = board.topics.order_by('-created_dt').annotate(comment=Count('posts'))
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,10)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request,'topics.html',{'board':board,'topics':topics})
@login_required
def new_topic(request,board_id):
    board = get_object_or_404(Board,pk=board_id)
    # user = User.objects.first()
    if request.method == "POST":
        form =NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                created_by = request.user,
                topic=topic
            )
            return redirect('board_topics',board_id=board.pk)
    else:
        form = NewTopicForm()
    return render(request,'new_topic.html',{'board':board,'form':form})
def topic_posts(request,board_id,topic_id):
    topic = get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    s_k = 'view_topic_{}'.format(topic.pk)
    if not request.session.get(s_k,False):
        topic.views +=1
        topic.save()
        request.session[s_k] = True
    return render(request,'topic_posts.html',{'topic':topic})
@login_required
def reply_topic(request, board_id,topic_id):
    topic = get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    if request.method == "POST":
        form =PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.up_by = request.user
            topic.up_dt = timezone.now()
            topic.save()
            return redirect('topic_posts',board_id=board_id, topic_id = topic_id)
    else:
        form = PostForm()
    return render(request,'reply_topic.html',{'topic':topic,'form':form})
@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    def form_valid(self,form):
        post = form.save(commit=False)
        post.up_by = self.request.user
        post.up_dt = timezone.now()
        post.save()
        return redirect('topic_posts',board_id=post.topic.board.pk,topic_id=post.topic.pk)
def about(request):
    return HttpResponse(request,"yes")

@login_required
def new_board(request):
    if request.method == "POST":
        form =NewBoardForm(request.POST)
        if form.is_valid():
            board = form.save()
            return redirect('home',)
    else:
        form = NewBoardForm()
    return render(request,'new_board.html',{'form':form})