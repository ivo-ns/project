import json

from django.contrib.auth import get_user_model, views as auth_views, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy
import datetime

from .forms import SignUpForm, ArtistAddForm, VinylAddForm, LabelAddForm, SignInForm
from .models import Artist, Genre, Vinyl, Article, Style, RecordLabel, Profile, Order, OrderItem, ShippingAddress

UserModel = get_user_model()


class SignUpView(views.CreateView):
    template_name = 'sign-up.html'
    form_class = SignUpForm

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)
        return result


class SignInView(auth_views.LoginView):
    template_name = 'sign-in.html'
    form_class = SignInForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['username'] = request.POST['username']
    #     return context
    #
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     return kwargs
    #
    # def form_invalid(self, form):
    #     messages.error(self.request,
    #                    'Please enter a correct email and password. Note that both fields may be case-sensitive.',
    #                    extra_tags='error')
    #     return super(SignInView, self).form_invalid(form)

    # def form_valid(self, form):
    #     messages.error(self.request,
    #                    'Please enter a correct email and password. Note that both fields may be case-sensitive.')
    #     return super(SignInView, self).form_valid(form)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super(SignInView, self).dispatch(request, *args, **kwargs)


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')
    template_name = 'sign-out.html'


class ProfileView(views.DetailView):
    model = UserModel
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Profile.objects.filter(pk=self.request.user.pk)
        context['vinyls'] = Vinyl.objects.filter(user=self.request.user)
        return context


# class IndexView(views.TemplateView):
#     template_name = 'index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['articles'] = Article.objects.all()
#
#         return context

class IndexView(views.ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = 'articles'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = Article.objects.filter(headline=True).first()
        return context

def vinylstorefbview(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    vinyls = Vinyl.objects.all().order_by('-added_on')[:4]
    vinyls_price = Vinyl.objects.all().order_by('-price')[:4]
    vinyls_latest = Vinyl.objects.all().order_by('-release_date')[:4]
    context = {
        'vinyls': vinyls,
        'vinyls_price': vinyls_price,
        'vinyls_latest': vinyls_latest,
        'cartItems': cartItems,
    }
    return render(request, 'vinyls.html', context)


class MarketplaceView(views.ListView):
    template_name = 'marketplace.html'
    model = Vinyl


class VinylBuyView(views.TemplateView):
    template_name = 'buy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        context['sort_by'] = self.request.GET.get("sort")
        context['newest_release'] = self.request.GET.get('newest_release')
        context['oldest_release'] = self.request.GET.get('oldest_release')
        context['date_added_new'] = self.request.GET.get('date_added_new')
        context['date_added_old'] = self.request.GET.get('date_added_old')
        if context['sort_by'] == 'l2h':
            context['vinyls'] = Vinyl.objects.order_by('price')
        elif context['sort_by'] == 'h2l':
            context['vinyls'] = Vinyl.objects.order_by('-price')
        elif context['newest_release'] == '':
            context['vinyls'] = Vinyl.objects.order_by('-release_date')
        elif context['oldest_release'] == '':
            context['vinyls'] = Vinyl.objects.order_by('release_date')
        elif context['date_added_new'] == '':
            context['vinyls'] = Vinyl.objects.order_by('-added_on')
        elif context['date_added_old'] == '':
            context['vinyls'] = Vinyl.objects.order_by('added_on')
        else:
            context['vinyls'] = Vinyl.objects.filter(
                Q(genre__name__icontains=q) |
                Q(style__name__icontains=q) |
                Q(artist__name__icontains=q) |
                Q(record_label__name__icontains=q) |
                Q(title__icontains=q)
            )

        context['genres'] = Genre.objects.order_by('name')
        context['styles'] = Style.objects.order_by('name')
        context['record_labels'] = RecordLabel.objects.order_by('name')
        context['artists'] = Artist.objects.order_by('name')
        return context


class VinylSellView(LoginRequiredMixin, views.CreateView):
    template_name = 'sell.html'
    form_class = VinylAddForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vinyls')


class VinylEditView(LoginRequiredMixin, views.UpdateView):
    template_name = 'vinyl-edit.html'
    form_class = VinylAddForm
    queryset = Vinyl.objects.all()

    def get_success_url(self):
        return reverse_lazy('vinyl page', kwargs={
            'pk': self.object.pk,
        })

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class VinylDetailsView(views.DetailView):
    model = Vinyl
    template_name = 'vinyl-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class VinylDeleteView(views.DeleteView):
    pass


class ExploreView(views.TemplateView):
    template_name = 'explore.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artists'] = Artist.objects.all()
        context['styles'] = Style.objects.all()
        context['genres'] = Genre.objects.all()
        return context


class BookingAgencyView(views.TemplateView):
    template_name = 'booking-agency.html'


class ArtistsAddView(LoginRequiredMixin, views.CreateView):
    template_name = 'add_artist.html'
    form_class = ArtistAddForm

    def get_success_url(self):
        return reverse_lazy('sell')


class ArtistsDetailView(views.DetailView):
    model = Artist
    template_name = 'artist_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['releases'] = Vinyl.objects.filter(artist__name=self.object)
        return context
    # template_name =
    # context_object_name =  #`object` or the name that we provide here
    # def get_context_data(self, **kwargs):


class ArtistsEditView(views.UpdateView):
    pass


class ArtistsDeleteView(views.DeleteView):
    pass


class ArtistsListView(views.ListView):
    model = Artist
    # template_name =
    # context_object_name = #`object_list` or the name that we provide here
    # paginate_by =
    # {% if page_obj.has_previous %}
    # <a href="?page=1">&laquo; first</a>
    # <a href="?page={{ page_obj.previous_page_number }}">previous</a>
    # {% endif %}
    # <span class "current">
    #   Page {{ page_obj.number }} of {{ page.obj.paginator_num_pages }}.
    # </span>
    # {% if page_obj.has_next %}
    # <a href="?page={{ page_obj.next_page_number }}">next</a>
    # <a href="?page={{ page_obj.paginator_num_pages }}">last &raquo;</a>
    # {% endif %}


class LabelAddView(LoginRequiredMixin, views.CreateView):
    template_name = 'add-label.html'
    form_class = LabelAddForm

    def get_success_url(self):
        return reverse_lazy('sell')


class LabelDetailView(views.DetailView):
    model = RecordLabel
    template_name = 'record_label.html'


class LabelEditView(views.UpdateView):
    pass


class LabelDeleteView(views.DeleteView):
    pass


class LabelListView(views.ListView):
    pass


class StylesListView(views.ListView):
    pass


class StylesDetailView(views.DetailView):
    model = Style
    template_name = 'style.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vinyl_same_style'] = Vinyl.objects.filter(style__name=self.object)
        return context


class GenresListView(views.ListView):
    pass


class GenresDetailView(views.DetailView):
    model = Genre
    template_name = 'genre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vinyl_same_genre'] = Vinyl.objects.filter(genre__name=self.object)
        return context


class TestView(views.TemplateView):
    template_name = 'test.html'


class CartView(views.TemplateView):
    template_name = 'cart.html'


class CheckOutView(views.TemplateView):
    template_name = 'checkout.html'


class BlogView(views.TemplateView):
    template_name = 'blog.html'


class ArticleView(views.TemplateView):
    template_name = 'article.html'


class ArticleDetailView(views.DetailView):
    model = Article
    template_name = 'article.html'


# class NotFoundView(views.TemplateView):
#     template_name = "404.html"
#
#     @classmethod
#     def get_rendered_view(cls):
#         as_view_fn = cls.as_view()
#
#         def view_fn(request):
#             response = as_view_fn(request)
#             # this is what was missing before
#             response.status_code = 404
#             response.render()
#             return response
#
#         return view_fn


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.profile
    vinyl = Vinyl.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(user=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, vinyl=vinyl)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                user=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in...')

    return JsonResponse('Payment submitted..', safe=False)
