from django.shortcuts import render
from .models import Profile, Shipping
from .forms import ProfileForm, ShippingForm
from django.views.generic import UpdateView, TemplateView, CreateView
from django.shortcuts import get_object_or_404

# Create your views here.


class UserProfile(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, slug=slug)
        context = {"profile": profile}
        return context


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = "accounts/profile-update.html"
    form_class = ProfileForm


class ShippingCreateView(CreateView):
    model = Shipping
    template_name = "accounts/add-shipping.html"
    form_class = ShippingForm
    success_url = "products"

    # if is_valid(form,self):
    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return super(ShippingCreateView, self).form_valid(form)
