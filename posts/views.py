from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            messages.success(request, 'Post created successfully!')
            return redirect('profile')  # Change this to your actual post list view name
    else:
        post_form = forms.PostForm()

    return render(request, 'add_post.html', {'form': post_form}) 


    
    
    
    
@login_required
def edit_post(request, id):
    post =  models.Post.objects.get(pk=id)
    post_form = forms.PostForm(instance=post)
    if request.method =='POST':
        post_form = forms.PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            return redirect('home')
    return render(request, 'add_post.html', {'form':post_form})

@login_required
def delete_post(request, id):
    post = models.Post.objects.get(pk=id)
    post.delete()
    return redirect('home')


# class based view
@method_decorator(login_required, name='dispatch')
class AddPost(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class EditPost(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')
    
@method_decorator(login_required, name='dispatch')    
class DeletePost(DeleteView):
    model = models.Post
    template_name = 'delete_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')
    
class PostDetails(DetailView):
    model = models.Post
    template_name = 'post_details.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all().order_by('-created_on')  # show latest first
        context['form'] = forms.CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object   # attach comment to this post
            comment.save()
            return redirect('post_details', id=self.object.id)
        # if invalid, re-render with errors
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class CommentDelete(DeleteView):
    model = models.Comment
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("home")  # change this to post list or detail page

    def get_success_url(self):
        # after delete, redirect back to the post details
        post = self.object.post
        return reverse_lazy('post_details', kwargs={'id': post.id})

   
  
    